from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
import tempfile
import os
import json

from app.services.video_edit import process_video, MOVIEPY_AVAILABLE

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
    print("\n=== /edit endpoint called ===")
    print(f"MoviePy available: {MOVIEPY_AVAILABLE}")
    print(f"Video filename: {video.filename}")
    print(f"Instructions raw: {instructions}")

    try:
        # Parse instructions JSON
        instructions_dict = json.loads(instructions)
        print(f"Instructions parsed: {instructions_dict}")

        # Save uploaded video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
            content = await video.read()
            tmp_input.write(content)
            input_path = tmp_input.name
        print(f"Temporary input file saved at: {input_path}")

        # Process video
        print("Starting process_video()...")
        output_path = await process_video(input_path, instructions_dict)
        print(f"Video processed. Output path: {output_path}")

        # Clean up input file
        os.unlink(input_path)
        print(f"Deleted temp input file: {input_path}")

        # Return processed video
        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=f"edited_{video.filename}",
            background=lambda: os.unlink(output_path) if os.path.exists(output_path) else None
        )

    except Exception as e:
        print(f"❌ Error while processing video: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process video: {str(e)}")
