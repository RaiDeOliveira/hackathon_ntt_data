import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageProps {
  text: string;
  sender: 'user' | 'bot';
}

export const Message: React.FC<MessageProps> = ({ text, sender }) => {
  const isUser = sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
      <div
        className={`p-3 rounded-lg max-w-xs break-words shadow-md ${
          isUser ? 'bg-zinc-600 text-white' : 'bg-gray-200 text-gray-800'
        }`}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
      </div>
    </div>
  );
};
