"""
Conversation Routes
Rutas para gestión de conversaciones y mensajes
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from application.services.conversation_service import ConversationService
from presentation.dto.conversation_dto import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)

router = APIRouter(prefix="/conversations", tags=["Conversations"])


def get_conversation_service() -> ConversationService:
    """Crea instancia del servicio de conversaciones"""
    return ConversationService()


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(user_id: str = Query(...)):
    """Obtiene todas las conversaciones de un usuario"""
    try:
        service = get_conversation_service()
        conversations = await service.get_conversations(user_id)
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ConversationResponse)
async def create_conversation(data: ConversationCreate):
    """Crea una nueva conversación"""
    try:
        service = get_conversation_service()
        conversation = await service.create_conversation(data.user_id, data.title)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str):
    """Obtiene todos los mensajes de una conversación"""
    try:
        service = get_conversation_service()
        messages = await service.get_messages(conversation_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def save_message(conversation_id: str, data: MessageCreate):
    """Guarda un mensaje en una conversación"""
    try:
        service = get_conversation_service()
        message = await service.save_message(conversation_id, data.role, data.content)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
