import re
from typing import Dict, List

from opik import track

from components.llm_client import AzureLLM
from components.utils import convert_message_history_to_text


class OrderIdExtractor:
    def __init__(self) -> None:
        with open('./components/resources/order_extraction_prompt.txt', 'r') as f:
            self.order_extraction_prompt = f.read()
        self.client = AzureLLM()
        self.order_id_pattern = r'\b\d{5}\b'

    @track(name="order_extraction")
    async def __call__(self, chat_history: List[Dict]) -> str:
        chat_history = convert_message_history_to_text(chat_history)
        updated_prompt = self.order_extraction_prompt.format(conversation=chat_history)
        order_id = await self.client(updated_prompt)
        match = re.search(self.order_id_pattern, order_id)
        return match.group() if match else ""