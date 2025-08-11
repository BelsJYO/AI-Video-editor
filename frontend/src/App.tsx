
import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import ChatInterface from './components/ChatInterface';
import VideoPreview from './components/VideoPreview';
import { VideoData } from './types';

function App() {
  const [videoData, setVideoData] = useState<VideoData | null>(null);
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);

  const handleVideoUploaded = (data: VideoData) => {
    setVideoData(data);
    setProcessedVideoUrl(null);
  };

  const handleVideoProcessed = (videoUrl: string) => {
    setProcessedVideoUrl(videoUrl);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">AI Video Editor</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <VideoUpload onVideoUploaded={handleVideoUploaded} />
            {videoData && (
              <ChatInterface 
                videoData={videoData} 
                onVideoProcessed={handleVideoProcessed} 
              />
            )}
          </div>
          
          <div>
            <VideoPreview 
              originalVideo={videoData} 
              processedVideoUrl={processedVideoUrl} 
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
