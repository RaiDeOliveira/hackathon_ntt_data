import React from 'react';
import { ChatToggleButton } from './chatToggleButton';

interface HeaderProps {
  toggleChat: () => void;
}

export const Header: React.FC<HeaderProps> = ({ toggleChat }) => {
  return (
    <header className="w-full bg-zinc-800 p-4 flex justify-between items-center shadow-md fixed top-0 left-0 z-40">
      {/* Logo à esquerda */}
      <div className="flex-shrink-0">
        <img src="/icon.jpg" alt="Logo" className="h-16 w-auto" />
      </div>

      {/* Texto central */}
      <div className="text-white text-center font-medium text-3xl flex-grow">
        Lion Guardians
      </div>

      {/* Botão do Chat à direita */}
      <div className="flex-shrink-0">
        <ChatToggleButton toggleChat={toggleChat} />
      </div>
    </header>
  );
};
