import axios from 'axios';

const api = axios.create({
  baseURL: ' http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ChatResponse = async (message: string): Promise<string> => {
  try {
    const response = await api.get(`/chat/${encodeURIComponent(message)}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching chat response:', error);
    return 'Something went wrong. Please try again.';
  }
};
