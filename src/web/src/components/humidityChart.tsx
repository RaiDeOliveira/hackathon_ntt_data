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

export const HumidityChart: React.FC = () => {
  const [data, setData] = useState<SensorData[]>([]);
  const [chartData, setChartData] = useState<ChartData<'line'>>({
    labels: [],
    datasets: [
      {
        label: 'Humidity (%)',
        data: [],
        borderColor: '#60a5fa', // Tailwind blue-400
        backgroundColor: 'rgba(96, 165, 250, 0.2)',
        fill: true,
        borderWidth: 2, // Make the border a bit thicker for clarity
        pointRadius: 0, // Hide the points for a cleaner look
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
          text: 'Hora',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Humidity (%)',
        },
        min: 0, // Ajuste conforme o seu caso
        max: 100, 
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
          labels: newData.map(item => {
            const date = new Date(item.timestamp);
            return date.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit'
            });
          }),
          datasets: prevChartData.datasets.map((dataset) => ({
            ...dataset,
            data: newData.map(item => item.humidity),
          })),
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
