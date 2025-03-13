import os
from typing import Dict, List

import pandas as pd
import requests

def convert_message_history_to_text(chat_history: List[Dict]) -> str:
    """Convert historical conversation to a form acceptable by the prep_context function prompt"""
    conv_history = ""

    for msg in chat_history:
        if msg['role'] == 'assistant':
            conv_history += f"Bot: {msg['content']}\n"
        else:
            conv_history += f"User: {msg['content']}\n"
    return conv_history


def log_intent(conv_input: str, intent: str) -> None:
    new_entry = pd.DataFrame([[pd.Timestamp.now(), conv_input, intent]],
                             columns=["Timestamp", "dialogues", "predicted_intent"])
    log_file_name = "log_intents.xlsx"
    if os.path.exists(log_file_name):
        existing_data = pd.read_excel(log_file_name)
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
    else:
        updated_data = new_entry

    updated_data.to_excel(log_file_name, index=False)

async def send_post_request(url: str, data: List[Dict]) -> requests.Response:
    return requests.post(url, json=    {"message_history": data})

if __name__ == '__main__':
    chat_history = [{"role": "assistant", "content": "How can I help you today?"},
                    {"role": "user", "content": "Can you tell me the status of my order?"},
                    {"role": "assistant", "content": "Of course! Could you please provide your order number?"},
                    {"role": "user", "content": "My order number is 44444."},
                    {"role": "assistant", "content": "Thank you! Your order is currently Shipped and is on its way. You can track its delivery using the link in your confirmation email. Is there anything else I can help you with?"},
                    {"role": "user", "content": "No, that’s all. Thanks!"},
                    {"role": "assistant", "content": "You’re welcome! Have a great day!"}]
    print(convert_message_history_to_text(chat_history))