
import os
import tempfile
from typing import Dict, Any, List
import requests 

# Import moviepy components
try:
    from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: MoviePy not available. Video processing will be limited. Error: {e}")
    MOVIEPY_AVAILABLE = False
    VideoFileClip = None
    TextClip = None
    CompositeVideoClip = None
    concatenate_videoclips = None


from app.utils.config import PIXABAY_API_KEY, PEXELS_API_KEY

async def process_video(input_path: str, instructions: Dict[str, Any]) -> str:
    """
    Process video based on instructions
    """
    if not MOVIEPY_AVAILABLE:
        # Return original file if MoviePy is not available
        output_path = input_path.replace('.mp4', '_processed.mp4')
        # Copy file as a placeholder
        import shutil
        shutil.copy2(input_path, output_path)
        return output_path
    
    try:
        video = VideoFileClip(input_path)
        operation = instructions.get('operation', 'trim')
        parameters = instructions.get('parameters', {})
        
        if operation == 'trim':
            start_time = parameters.get('start_time', 0)
            end_time = parameters.get('end_time', video.duration)
            video = video.subclip(start_time, min(end_time, video.duration))
        
        elif operation == 'add_text':
            text = parameters.get('text', 'Sample Text')
            position = parameters.get('position', 'center')
            duration = parameters.get('duration', 5)
            
            txt_clip = TextClip(
                text,
                fontsize=50,
                color='white',
                font='Arial-Bold'
            ).set_position(position).set_duration(min(duration, video.duration))
            
            video = CompositeVideoClip([video, txt_clip])
        
        elif operation == 'speed_change':
            speed = parameters.get('speed', 1.0)
            video = video.speedx(speed)
        
        # Generate output file
        output_path = tempfile.mktemp(suffix='.mp4')
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        video.close()
        
        return output_path
        
    except Exception as e:
        print(f"Error processing video: {e}")
        # Return original file on error
        output_path = input_path.replace('.mp4', '_processed.mp4')
        import shutil
        shutil.copy2(input_path, output_path)
        return output_path

async def search_stock_footage(query: str) -> List[Dict[str, Any]]:
    """
    Search for stock footage from APIs
    """
    results = []
    
    # Try Pixabay
    if PIXABAY_API_KEY:
        try:
            response = requests.get(
                f"https://pixabay.com/api/videos/",
                params={
                    'key': PIXABAY_API_KEY,
                    'q': query,
                    'video_type': 'film',
                    'per_page': 5
                }
            )
            if response.status_code == 200:
                data = response.json()
                for hit in data.get('hits', []):
                    results.append({
                        'source': 'pixabay',
                        'url': hit['videos']['medium']['url'],
                        'thumbnail': hit['userImageURL']
                    })
        except Exception as e:
            print(f"Pixabay search error: {e}")
    
    return results

def download_stock_footage(url: str) -> str:
    """
    Download stock footage from URL
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            output_path = tempfile.mktemp(suffix='.mp4')
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return output_path
    except Exception as e:
        print(f"Download error: {e}")
    
    return None
