from fastapi import APIRouter

from src.service.chat_service import ChatService

router = APIRouter(
  prefix="/chat",
  tags=["Chat"]
)

@router.get("/{message}", status_code=200)
def get_response(message: str):
  _chat_service = ChatService()
  return _chat_service.generate_response(message)