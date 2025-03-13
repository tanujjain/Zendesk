import asyncio
from typing import List, Dict

from opik import track

from components.llm_client import AzureLLM
from components.utils import convert_message_history_to_text

class GetNextStep:
    def __init__(self) -> None:
        with open('./components/resources/next_step_prompt.txt', 'r') as f:
            self.next_step_prompt = f.read()
        self.client = AzureLLM()

    @track(name="next_action")
    async def __call__(self, chat_history_openai_format: List[Dict]) -> str:
        chat_history = convert_message_history_to_text(chat_history_openai_format)
        updated_prompt = self.next_step_prompt.format(conversation=chat_history)
        return await self.client(updated_prompt)


if __name__ == '__main__':
    conv = [{"role": "user", "content": "I wanna cancel my order"}]
    print(asyncio.run(GetNextStep()(conv)))