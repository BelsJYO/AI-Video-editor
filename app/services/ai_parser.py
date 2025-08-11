
import json
from typing import Dict, Any
from app.utils.config import GROQ_API_KEY
import httpx

async def parse_video_command(command: str, video_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse natural language video editing commands using Groq API
    """
    if not GROQ_API_KEY:
        # Fallback to basic parsing without AI
        return parse_command_fallback(command)
    
    try:
        prompt = f"""
        You are a video editing assistant. Parse this command into structured instructions:
        
        Command: "{command}"
        Video metadata: {json.dumps(video_metadata)}
        
        Return ONLY a JSON object with this structure:
        {{
            "operation": "trim|crop|add_text|add_music|speed_change|filter",
            "parameters": {{
                "start_time": 0,
                "end_time": 10,
                "text": "example text",
                "position": "center",
                "speed": 1.5
            }}
        }}
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1
                }
            )
            
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
        else:
            return parse_command_fallback(command)
            
    except Exception as e:
        print(f"AI parsing failed: {e}")
        return parse_command_fallback(command)

def parse_command_fallback(command: str) -> Dict[str, Any]:
    """
    Fallback parser for when AI is not available
    """
    command_lower = command.lower()
    
    if "trim" in command_lower or "cut" in command_lower:
        return {
            "operation": "trim",
            "parameters": {
                "start_time": 0,
                "end_time": 30
            }
        }
    elif "text" in command_lower or "title" in command_lower:
        return {
            "operation": "add_text",
            "parameters": {
                "text": "Sample Text",
                "position": "center",
                "duration": 5
            }
        }
    elif "speed" in command_lower:
        return {
            "operation": "speed_change",
            "parameters": {
                "speed": 2.0 if "fast" in command_lower else 0.5
            }
        }
    else:
        return {
            "operation": "trim",
            "parameters": {
                "start_time": 0,
                "end_time": 10
            }
        }
