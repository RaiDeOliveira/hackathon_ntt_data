import React, { useState } from 'react';
import { Chat } from '../components/chat';
import { Header } from '../components/header'; 

export const Home: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="relative min-h-screen pt-16"> 
      <Header
        toggleChat={toggleChat}
      />

      {isChatOpen && (
        <div className="fixed top-16 right-4 z-50 pt-4">
          <Chat />
        </div>
      )}
    </div>
  );
};
