from enum import Enum
from pathlib import Path
import re

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from opik import track, Opik

from components.next_action_classification import GetNextStep
from components.other_intent import OtherIntent
from components.evaluation import EvaluateAppropriateness
from components.utils import log_intent, send_post_request
from config import MAX_TURNS, ENDPOINT_ORDER_TRACKING, ENDPOINT_ORDER_CANCELLATION


app = FastAPI()

# Frontend
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(static_dir / "index.html")

# Some intializations
client = Opik()
get_next_step = GetNextStep()
evaluate = EvaluateAppropriateness()
handle_other_intent = OtherIntent()


@track(name="cant_understand")
async def cant_understand(x) -> str:
    return "Sorry, I could not understand your request. Can you please rephrase it?"

@track(name="end_conversation")
async def end_conversation(x) -> str:
    return "Thank you for using our service. Have a great day!"

class NextSteps(Enum):
    TRACK = "track_order"
    CANCEL = "cancel_order"
    OTHER = "Other"
    END = "end_conversation"

next_steps = {
    NextSteps.TRACK.value: ENDPOINT_ORDER_TRACKING,
    NextSteps.CANCEL.value: ENDPOINT_ORDER_CANCELLATION,
    NextSteps.OTHER.value: handle_other_intent,
    NextSteps.END.value: end_conversation
}


@app.websocket("/ws")
async def converse(websocket: WebSocket) -> None:
    await websocket.accept()
    conversation_history = [{"role": "system",
                             "content": "You are a helpful ecommerce assistant. Be helpful and give only polite responses."},
                            {"role": "assistant", "content": "How can I help you today?"}]
    await websocket.send_text("How can I help you today?")
    turn_counter = 0

    while True:
        user_input = await websocket.receive_text()
        conversation_history.append({"role": "user", "content": user_input})
        next_action = await get_next_step(conversation_history)
        next_action = re.sub(r'[^\w\s]', '', next_action)
        # log_intent(user_input, next_action)

        if next_action == NextSteps.END.value or turn_counter == MAX_TURNS:
            trace = client.trace(name="eval_trace")
            evaluation = await evaluate(conversation_history)
            client.log_traces_feedback_scores(
                scores=[
                    {"id": trace.id, "name": "overall_quality", "value": 1 if evaluation.lower() == "appropriate" else 0},
                ]
            )
            client.log_traces_feedback_scores(
                scores=[
                    {"id": trace.id, "name": "turn_counter", "value": turn_counter},
                ]
            )
            turn_counter = 0
            conversation_history = [{"role": "system",
                                     "content": "You are a helpful ecommerce assistant. Be helpful and give only polite responses."},
                                    {"role": "assistant", "content": "How can I help you today?"}]
            response = await end_conversation(conversation_history)
        if next_action in [NextSteps.TRACK.value, NextSteps.CANCEL.value]:
            response = await send_post_request(next_steps[next_action], conversation_history)
            response = response.json()['response']
            conversation_history.append({"role": "assistant", "content": response})
            turn_counter+=1
        else:
            next_action_fn = next_steps.get(next_action, cant_understand)
            response = await next_action_fn(conversation_history)
            conversation_history.append({"role": "assistant", "content": response})
            turn_counter+=1
        await websocket.send_text(response)
