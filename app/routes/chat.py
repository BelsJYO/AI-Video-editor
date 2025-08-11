
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.services.ai_parser import parse_video_command

router = APIRouter()

class ChatRequest(BaseModel):
    command: str
    video_metadata: Dict[str, Any]

class ChatResponse(BaseModel):
    success: bool
    instructions: Dict[str, Any]
    message: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Parse natural language video editing commands using AI
    """
    try:
        instructions = await parse_video_command(request.command, request.video_metadata)
        return ChatResponse(
            success=True,
            instructions=instructions,
            message="Command parsed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse command: {str(e)}")
