import React from 'react';
import { ChatBubbleBottomCenterIcon } from '@heroicons/react/24/solid';

interface ChatToggleButtonProps {
  toggleChat: () => void;
}

export const ChatToggleButton: React.FC<ChatToggleButtonProps> = ({ toggleChat }) => {
  return (
    <button
      className="top-4 right-4 p-2 bg-gray-500 text-white rounded-lg z-50 focus:outline-none"
      onClick={toggleChat}
    >
      <ChatBubbleBottomCenterIcon className="h-8 w-8 text-white" />
    </button>
  );
};
