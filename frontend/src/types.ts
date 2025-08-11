export interface VideoData {
  file: File;
  metadata: {
    duration?: number;
    width?: number;
    height?: number;
    size: number;
    type: string;
  };
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface EditInstructions {
  operation: string;
  parameters: {
    start_time?: number;
    end_time?: number;
    text?: string;
    position?: string;
    music_genre?: string;
    search_terms?: string;
  };
}