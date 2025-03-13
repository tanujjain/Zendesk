from typing import List, Dict

from opik import track

from components.llm_client import AzureLLM
from components.utils import convert_message_history_to_text


class OtherIntent:
    def __init__(self):
        with open('./components/resources/other_intent_prompt.txt', 'r') as f:
            self.other_intent_prompt = f.read()
        self.client = AzureLLM()

    @track(name="other_intent")
    async def __call__(self, chat_history_openai_format: List[Dict]) -> str:
        chat_history = convert_message_history_to_text(chat_history_openai_format)
        updated_prompt = self.other_intent_prompt.format(conversation=chat_history)
        return await self.client(updated_prompt)