import asyncio
import time

import pandas as pd
import websockets

async def send_message(message: str) -> None:
    uri = "ws://127.0.0.1:8001/ws"
    async with websockets.connect(uri) as websocket:

        await websocket.send(message)

        response = await websocket.recv()

df = pd.read_excel('/Users/tjain1/Desktop/sides/test_intent_correctness/intent_dialogues.xlsx')

for row in df.iterrows():
    conv = row[1]['dialogues']
    asyncio.run(send_message(conv))
    time.sleep(1)
