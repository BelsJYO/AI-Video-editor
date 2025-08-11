
import React from 'react';
import { Play, Download } from 'lucide-react';
import { VideoData } from '../types';

interface VideoPreviewProps {
  originalVideo: VideoData | null;
  processedVideoUrl: string | null;
}

export default function VideoPreview({ originalVideo, processedVideoUrl }: VideoPreviewProps) {
  if (!originalVideo) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Video Preview</h2>
        <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
          <p className="text-gray-500">Upload a video to see preview</p>
        </div>
      </div>
    );
  }

  const videoUrl = URL.createObjectURL(originalVideo.file);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Video Preview</h2>
      
      <div className="space-y-4">
        <div>
          <h3 className="font-medium mb-2">Original Video</h3>
          <video
            src={videoUrl}
            controls
            className="w-full aspect-video rounded-lg"
          />
          <div className="mt-2 text-sm text-gray-600">
            <p>Duration: {Math.round(originalVideo.metadata.duration)}s</p>
            <p>Resolution: {originalVideo.metadata.width}x{originalVideo.metadata.height}</p>
            <p>Size: {(originalVideo.metadata.size / 1024 / 1024).toFixed(1)} MB</p>
          </div>
        </div>

        {processedVideoUrl && (
          <div>
            <h3 className="font-medium mb-2">Processed Video</h3>
            <video
              src={processedVideoUrl}
              controls
              className="w-full aspect-video rounded-lg"
            />
            <div className="mt-2 flex space-x-2">
              <button
                onClick={() => {
                  const a = document.createElement('a');
                  a.href = processedVideoUrl;
                  a.download = 'processed_video.mp4';
                  a.click();
                }}
                className="flex items-center px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                <Download className="mr-2 h-4 w-4" />
                Download
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
