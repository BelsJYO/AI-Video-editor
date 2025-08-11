
import React, { useState } from 'react';
import { Send, MessageCircle, Loader } from 'lucide-react';
import { VideoData, ChatMessage, EditInstructions } from '../types';
import axios from 'axios';

interface ChatInterfaceProps {
  videoData: VideoData;
  onVideoProcessed: (videoUrl: string) => void;
}

export default function ChatInterface({ videoData, onVideoProcessed }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const addMessage = (role: 'user' | 'assistant', content: string) => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    addMessage('user', userMessage);
    setIsProcessing(true);

    try {
      // Parse command
      const chatResponse = await axios.post('/api/chat', {
        command: userMessage,
        video_metadata: videoData.metadata
      });

      const instructions = chatResponse.data.instructions;
      addMessage('assistant', `I'll ${instructions.operation} your video. Processing...`);

      // Process video
      const formData = new FormData();
      formData.append('video', videoData.file);
      formData.append('instructions', JSON.stringify(instructions));

      const editResponse = await axios.post('/api/edit', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      });

      const videoBlob = new Blob([editResponse.data], { type: 'video/mp4' });
      const videoUrl = URL.createObjectURL(videoBlob);
      
      onVideoProcessed(videoUrl);
      addMessage('assistant', 'Video processing complete! You can preview and download it.');

    } catch (error) {
      console.error('Error processing video:', error);
      addMessage('assistant', 'Sorry, there was an error processing your video. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 flex items-center">
        <MessageCircle className="mr-2" />
        AI Video Editor
      </h2>

      <div className="h-64 overflow-y-auto border border-gray-200 rounded-lg p-4 mb-4 space-y-3">
        {messages.length === 0 ? (
          <div className="text-gray-500 text-center">
            <p>Tell me what you'd like to do with your video!</p>
            <p className="text-sm mt-2">Try: "Trim the first 10 seconds" or "Add text saying 'Hello World'"</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs mt-1 opacity-70">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Describe what you want to do..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isProcessing}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isProcessing}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {isProcessing ? (
            <Loader className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </button>
      </form>
    </div>
  );
}
