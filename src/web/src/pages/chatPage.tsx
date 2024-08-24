import React from 'react';
import { Chat } from '../components/chat';

export const ChatPage: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
        <Chat />
      {/* <div className="w-full max-w-md p-6 bg-white shadow-lg rounded-lg">
        <h1 className="text-2xl font-bold mb-4 text-center text-gray-800">Chat</h1>
      </div> */}
    </div>
  );
};

