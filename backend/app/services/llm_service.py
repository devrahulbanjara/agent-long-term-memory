from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from app.services.memory_service import MemoryService
from app.schemas.memory_schemas import ExtractedMemory
from app.prompts import MEMORY_EXTRACTION_PROMPT, SYSTEM_PROMPT
import asyncio
from app.core import logger


class LLMService:
    def __init__(self, llm: ChatGroq, memory: MemoryService):
        self.llm = llm
        self.memory = memory
        self.history: list[BaseMessage] = [
            SystemMessage(content=SYSTEM_PROMPT)
        ]

    async def generate_response(self, user_input: str) -> str:
        relevant_memories = self.memory.search_memory(user_input)
        
        # Build context from memories
        context_str = ""
        if relevant_memories:
            context_str = "What you know about the user:\n" + "\n".join([f"• {m}" for m in relevant_memories])

        # Prepare conversation with context
        current_prompt = []
        if context_str:
            current_prompt.append(SystemMessage(content=context_str))
        
        current_prompt.extend([*self.history, HumanMessage(content=user_input)])

        # Generate response
        response = await self.llm.ainvoke(current_prompt)

        # Update history
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=response.content))

        # Extract and save memories asynchronously
        asyncio.create_task(self._extract_and_save_memory(user_input, response.content))

        return response.content

    async def _extract_and_save_memory(self, user_msg: str, ai_msg: str):
        """Extract memories using structured output"""
        try:
            # Create extraction prompt
            extraction_prompt = MEMORY_EXTRACTION_PROMPT.format(
                user_msg=user_msg, 
                ai_msg=ai_msg
            )
            
            # Use structured output with LangChain
            structured_llm = self.llm.with_structured_output(ExtractedMemory)
            result: ExtractedMemory = await structured_llm.ainvoke(
                [HumanMessage(content=extraction_prompt)]
            )
            
            # Save each extracted fact
            for fact in result.facts:
                if fact.strip():
                    self.memory.save_memory(fact.strip())
                    
        except Exception as e:
            logger.error(f"Memory extraction failed: {e}")
