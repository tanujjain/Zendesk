from typing import List, Dict

from opik import track

from components.llm_client import AzureLLM
from components.utils import convert_message_history_to_text


class EvaluateAppropriateness:
    def __init__(self) -> None:
        with open('./components/resources/conv_evaluation_prompt.txt', 'r') as f:
            self.conv_eval_prompt = f.read()
        self.client = AzureLLM()

    @track(name="evaluate")
    async def __call__(self, chat_history_openai_format: List[Dict]) -> str:
        chat_history = convert_message_history_to_text(chat_history_openai_format)
        updated_prompt = self.conv_eval_prompt.format(conversation=chat_history)
        return await self.client(updated_prompt)