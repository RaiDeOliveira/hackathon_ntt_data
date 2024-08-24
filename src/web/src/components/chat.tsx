import React, { useState, useRef, useEffect } from 'react';
import { ChatResponse } from '../services/api';
import { Message } from './message';

export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'bot' }[]>([]);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    // Adiciona a mensagem do usuário
    const userMessage = { text: input, sender: 'user' as const };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');

    try {
      // Aguarda a resposta do backend
      const botResponse = await ChatResponse(input);

      // Adiciona a mensagem do bot
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: botResponse, sender: 'bot' as const },
      ]);
    } catch (error) {
      console.error('Error fetching chat response:', error);
    }
  };

  // Auto-scroll para o fim do chat quando uma nova mensagem for adicionada
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-[600px] max-w-[500px] w-full mx-auto bg-white shadow-lg rounded-lg">
      <div
        ref={chatContainerRef}
        className="flex-grow p-4 overflow-auto"
      >
        {messages.map((msg, idx) => (
          <Message key={idx} text={msg.text} sender={msg.sender} />
        ))}
      </div>
      <div className="p-4 border-t border-gray-200">
        <input
          type="text"
          className="w-full p-2 border text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
        />
      </div>
    </div>
  );
};
