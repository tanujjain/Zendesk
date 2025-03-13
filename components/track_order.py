from typing import Dict, List

from opik import track
import pandas as pd

from components.order_extract import OrderIdExtractor
from components.llm_client import AzureLLM


class OrderTracking:
    def __init__(self) -> None:
        self.order_db = pd.read_excel('./components/resources/order_db.xlsx')
        self.client = AzureLLM()
        self.order_id_extractor = OrderIdExtractor()

    def _get_order_id_records(self, order_id: int) -> pd.DataFrame:
        return self.order_db[self.order_db['order_id'] == order_id]

    @track(name="order_tracking")
    async def __call__(self, chat_history: List[Dict]) -> str:
        order_id = await self.order_id_extractor(chat_history)
        try:
            df_order = self._get_order_id_records(int(order_id))
            order_last_status = df_order.tail(1)['order_status'].values[0]
            return f"Your order status is {order_last_status}. Can I help you with anything else?"
        except (ValueError, IndexError):
            return "Sorry, I could not find the order number. Please provide the order number."
