
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import tempfile
import os

from app.services.video_edit import process_video

router = APIRouter()

class EditRequest(BaseModel):
    instructions: Dict[str, Any]

@router.post("/edit")
async def edit_video(
    video: UploadFile = File(...),
    instructions: str = Form(...)
):
    """
    Process video based on AI-generated instructions
    """
    try:
        # Parse instructions JSON
        import json
        instructions_dict = json.loads(instructions)
        
        # Save uploaded video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
            content = await video.read()
            tmp_input.write(content)
            input_path = tmp_input.name
        
        # Process video
        output_path = await process_video(input_path, instructions_dict)
        
        # Clean up input file
        os.unlink(input_path)
        
        # Return processed video
        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=f"edited_{video.filename}",
            background=lambda: os.unlink(output_path) if os.path.exists(output_path) else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
