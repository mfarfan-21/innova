"""
Rutas de Chatbot - Simple
"""
from fastapi import APIRouter
from application.services.chatbot_service import ChatbotService
from presentation.dto.chatbot_dto import ChatRequest, ChatResponse

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Instancia del servicio
chatbot_service = ChatbotService()


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Envía un mensaje al chatbot y recibe una respuesta
    """
    response = chatbot_service.get_response(request.message, request.language)
    
    return ChatResponse(
        response=response,
        language=request.language
    )
