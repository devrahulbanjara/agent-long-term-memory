from langchain_groq import ChatGroq
from app.core import settings
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
_memory_service = MemoryService(embeddings=_embeddings)

_llm_client = ChatGroq(
    model="llama-3.1-8b-instant", api_key=settings.GROQ_API_KEY, temperature=0.7
)
_llm_service = LLMService(llm=_llm_client, memory=_memory_service)


def get_llm_service() -> LLMService:
    return _llm_service
