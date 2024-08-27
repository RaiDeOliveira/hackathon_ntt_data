import React, { useState } from 'react';
import { Chat } from '../components/chat';
import { Header } from '../components/header'; 
import { TemperatureChart } from '../components/temperatureChart';
import { Chart } from '../components/chart'; // Importa o outro gráfico

export const Home: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="relative min-h-screen pt-16 ove">
      <Header toggleChat={toggleChat} />

      {isChatOpen && (
        <div className="fixed top-16 right-4 z-50 pt-4">
          <Chat />
        </div>
      )}

      <div className="flex justify-between items-center h-screen p-8">
        {/* Gráfico de temperatura */}
        <div className="w-1/2">
          <TemperatureChart />
        </div>

        {/* Outro gráfico */}
        <div className="w-1/2">
          <Chart />
        </div>
      </div>
    </div>
  );
};
