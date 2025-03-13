from abc import ABC, abstractmethod
import asyncio
import os

from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import opik
from opik.integrations.openai import track_openai

opik.configure(use_local=True)

load_dotenv()

class LLMClient(ABC):
    @abstractmethod
    async def __call__(self, query: str) -> None:
        raise NotImplementedError()


class AzureLLM(LLMClient):
    def __init__(self) -> None:
        self.client = track_openai(AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
        ))

    async def __call__(self, query: str) -> str:
        chat_completion = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "assistant",
                    "content": query,
                }
            ],
            model="gpt-4o",
            temperature=0
        )
        content = chat_completion.choices[0].message.content
        return content

if __name__ == '__main__':
    print(asyncio.run(AzureLLM()("Hello")))
