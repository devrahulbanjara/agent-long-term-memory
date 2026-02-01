from langchain_groq import ChatGroq
from app.core import settings
from app.services.llm_service import LLMService

_llm_client = ChatGroq(
    model="llama-3.1-8b-instant", 
    api_key=settings.GROQ_API_KEY,
    temperature=0.7
)

_llm_service_instance = LLMService(llm=_llm_client) # Doing this so that on every request history is not wiped out

def get_llm_service() -> LLMService:
    return _llm_service_instance
