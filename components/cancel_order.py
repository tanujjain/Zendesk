from typing import List, Dict

from opik import track
import pandas as pd

from components.order_extract import OrderIdExtractor
from components.llm_client import AzureLLM
from components.db_models import OrderStatus, ForbiddenCancellationItems


class OrderCancellation:
    def __init__(self) -> None:
        self.order_db = pd.read_excel('./components/resources/order_db.xlsx')
        self.client = AzureLLM()
        self.order_id_extractor = OrderIdExtractor()


    async def _obtain_order_records(self, chat_history: List[Dict]) -> pd.DataFrame:
        order_id = await self.order_id_extractor(chat_history)
        order_id = int(order_id)
        return self.order_db[self.order_db['order_id'] == order_id]

    @track(name="order_cancellation")
    async def __call__(self, chat_history: List[Dict]) -> str:
        try:
            # import pdb;pdb.set_trace()
            df_order = await self._obtain_order_records(chat_history)
            last_status = df_order.tail(1)['order_status'].values[0]
            item_type = df_order['item_type'].values[0]
            days_since_ordered = (pd.Timestamp.now() - df_order.tail(1)['order_date'].values[0]).days
        except (ValueError, IndexError):
            return "Sorry, I could not find the order number. Please provide the order number."

        if last_status == OrderStatus.PENDING.value and days_since_ordered < 10 and item_type not in ForbiddenCancellationItems:
            return "The order has been successfully cancelled. Can I help you with anything else?"
        elif last_status != OrderStatus.PENDING.value:
            return "Sorry, the order has already been processed. As per Policy, it can't be cancelled."
        elif days_since_ordered >= 10:
            return "Sorry, the order has been processed for more than 10 days. As per Policy, it can't be cancelled."
        elif item_type in ForbiddenCancellationItems:
            return f"Sorry, the order contains {item_type} items. As per Policy, it can't be cancelled."
