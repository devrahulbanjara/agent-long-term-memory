from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas import ChatRequest, ChatResponse
from app.core import logger
from app.core.dependencies import get_llm_service
from app.services.llm_service import LLMService

chat_router = APIRouter()


@chat_router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest, llm_service: LLMService = Depends(get_llm_service)
):
    try:
        logger.debug(f"Processing message: {request.message}")

        ai_message = await llm_service.generate_response(request.message)

        return ChatResponse(message=ai_message)

    except Exception as e:
        logger.error(f"Error in chat route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
