import React, { useState, useEffect } from "react";
import { Chat } from "../components/chat";
import { Header } from "../components/header";
import { Temperature } from "../components/temperature";
import Chart from "../components/chart";
import useWebSocket from "react-use-websocket";
import io from "socket.io-client";
import { SingleValueChart } from "../components/singleValueChart";

export type SensorData = {
  timestamp: string;
  temperature: number;
  humidity: number;
  lux: number;
  noise: number;
};

export const Home: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [videoSrc, setVideoSrc] = useState(''); // Para armazenar o vídeo
  const [peopleCount, setPeopleCount] = useState(0); // Para armazenar a contagem de pessoas
  const [postureValue, setPosture] = useState(0); // Para armazenar a postura

  useWebSocket("ws://localhost:8000/api/ws/sensor", {
    onOpen: () => console.log("WebSocket connection opened"),
    onClose: () => console.log("WebSocket connection closed"),
    onMessage: (event) => {
      try {
        const receivedData: SensorData[] = JSON.parse(event.data);
        if (Array.isArray(receivedData)) {
          console.log("Received WebSocket message:", receivedData);
          setSensorData(receivedData);
        } else {
          console.error("Received data is not an array:", receivedData);
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    },
    onError: (error) => console.error("WebSocket error:", error),
    shouldReconnect: () => true, // Reconnect on close
  });


  useWebSocket('ws://localhost:8007/ws', {
    onOpen: () => console.log("WebSocket connection opened"),
    onClose: () => console.log("WebSocket connection closed"),
    onMessage: (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log(data.num_people);
        // Atualiza o vídeo com o frame recebido
        setVideoSrc(`data:image/jpeg;base64,${data.frame}`);
        // Atualiza a contagem de pessoas
        setPeopleCount(data.num_people);

        const posture = data.posture;
        setPosture(posture);

      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    },
    onError: (error) => console.error("WebSocket error:", error),
    shouldReconnect: () => true, // Reconnect on close
  });

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const processChartData = (variable: keyof SensorData, color: string) => {
    const data = (sensorData || [])
      .map((item) => item[variable])
      .filter((value) => typeof value === "number") as number[];

    const labels = (sensorData || []).map((item) => {
      if (typeof item.timestamp === "string") {
        return new Date(item.timestamp).toLocaleTimeString().slice(0, -3);
      }
      return "";
    });

    return {
      data,
      labels,
      label: variable.charAt(0).toUpperCase() + variable.slice(1),
      color,
    };
  };

  return (
    <div className="relative min-h-screen pt-12">
      <Header toggleChat={toggleChat} />

      {isChatOpen && (
        <div className="fixed top-16 right-4 z-50 pt-4">
          <Chat />
        </div>
      )}

      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <div className="flex flex-row gap-6 items-center justify-center w-full">
          <div className="relative w-4/5 p-4 border border-gray-500 rounded-lg shadow-md">
            <img src={videoSrc} alt="Video feed" className="rounded-lg shadow-lg w-full" />
          </div>
          <div className="flex flex-col justify-center p-4 border border-gray-500 rounded-lg shadow-md w-1/5">
            <div className="flex flex-col gap-5">
              <SingleValueChart title={"Pessoas Detectadas"} value={peopleCount} />
              
              <div className="p-4 border rounded-lg shadow-md bg-white text-black">
                <h2 className="text-lg font-bold">Postura</h2>
                <div className="text-4xl font-bold">
                  {postureValue !== null ? `${postureValue}` : 'Loading...'}
                </div>
              </div>

              <SingleValueChart title={"Qualidade do Escritório"} value={0} />
            </div>
          </div>
        </div>
      </div>

      <div className="pt-16 px-4 flex items-start">
        {/* Dados de temperatura ocupando 20% da tela */}
        <div className="w-1/5 p-4 border border-gray-500 rounded-lg shadow-md">
          <Temperature />
        </div>

        {/* Gráficos 2x2 ocupando o restante da tela */}
        <div className="w-4/5 grid grid-cols-2 grid-rows-2 gap-4 px-4">
          <div className="p-4 border border-gray-500 rounded-lg shadow-md">
            <Chart {...processChartData("humidity", "#FF6384")} />
          </div>
          <div className="p-4 border border-gray-500 rounded-lg shadow-md">
            <Chart {...processChartData("temperature", "#36A2EB")} />
          </div>
          <div className="p-4 border border-gray-500 rounded-lg shadow-md">
            <Chart {...processChartData("lux", "#FFCE56")} />
          </div>
          <div className="p-4 border border-gray-500 rounded-lg shadow-md">
            <Chart {...processChartData("noise", "#4BC0C0")} />
          </div>
        </div>
      </div>
    </div>
  );
};
