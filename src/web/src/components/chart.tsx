import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import { ChartOptions, ChartData } from 'chart.js';
import 'chart.js/auto';
import useWebSocket from 'react-use-websocket';

type SensorData = {
  id: number;
  temperature: number;
  humidity: number;
  lux: number;  // Ainda está no tipo, mas não será usado no gráfico
  noise: number;
  timestamp: string;
};

export const Chart: React.FC = () => {
  const [data, setData] = useState<SensorData[]>([]);
  const [chartData, setChartData] = useState<ChartData<'line'>>({
    labels: [],
    datasets: [
      {
        label: 'Temperature (°C)',
        data: [],
        borderColor: '#f87171', // Tailwind red-400
        backgroundColor: 'rgba(248, 113, 113, 0.2)',
        fill: true,
      },
      {
        label: 'Humidity (%)',
        data: [],
        borderColor: '#60a5fa', // Tailwind blue-400
        backgroundColor: 'rgba(96, 165, 250, 0.2)',
        fill: true,
      },
      {
        label: 'Noise (dB)',
        data: [],
        borderColor: '#34d399', // Tailwind green-400
        backgroundColor: 'rgba(52, 211, 153, 0.2)',
        fill: true,
      },
    ],
  });

  const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false, // Para evitar redimensionamento excessivo
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Timestamp',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Values',
        },
        min: 0, // Ajuste conforme o seu caso
        max: 100, // Defina o valor máximo esperado para estabilizar a escala
      },
    },
  };

  useWebSocket('ws://localhost:8000/api/ws/sensor', {
    onMessage: (event) => {
      const receivedData: SensorData[] = JSON.parse(event.data);
      console.log('Received WebSocket message:', ...receivedData);

      // Atualize o estado dos dados
      setData((prevData) => {
        const newData = [...prevData, ...receivedData].slice(-25); // Mantém apenas os últimos 25 pontos de dados

        // Atualiza o gráfico diretamente
        setChartData((prevChartData) => ({
          ...prevChartData,
          labels: newData.map(item => new Date(item.timestamp).toLocaleTimeString()),
          datasets: prevChartData.datasets.map((dataset, index) => {
            if (index === 0) {
              return {
                ...dataset,
                data: newData.map(item => item.temperature),
              };
            } else if (index === 1) {
              return {
                ...dataset,
                data: newData.map(item => item.humidity),
              };
            } else if (index === 2) {
              return {
                ...dataset,
                data: newData.map(item => item.noise),
              };
            }
            return dataset;
          }),
        }));

        return newData;
      });
    },
  });

  return (
    <div className="max-w-4xl mx-auto p-4 h-96"> {/* Adicione uma altura fixa */}
      {data.length > 0 ? (
        <Line data={chartData} options={chartOptions} />
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
};
