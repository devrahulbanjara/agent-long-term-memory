from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq


class LLMService:
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.history: list[BaseMessage] = [
            SystemMessage(content="You are a helpful AI assistant, answer concisely to the user.")
        ]

    async def generate_response(self, user_input: str) -> str:
        self.history.append(HumanMessage(content=user_input))
        response = await self.llm.ainvoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content
