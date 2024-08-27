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

export const TemperatureChart: React.FC = () => {
  const [data, setData] = useState<SensorData[]>([]);
  const [chartData, setChartData] = useState<ChartData<'line'>>({
    labels: [],
    datasets: [
      {
        label: 'Temperature (°C)',
        data: [],
        borderColor: '#f87171', // Tailwind red-400
        backgroundColor: 'rgba(248, 113, 113, 0.2)',
        borderWidth: 2, // Make the border a bit thicker for clarity
        pointRadius: 0, // Hide the points for a cleaner look
        fill: true,
      },
    ],
  });

  const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        display: true,
        grid: {
          display: false, // Hide grid lines for a cleaner look
        },
        title: {
          display: true,
          text: 'Hora',
          color: '#9ca3af', // Tailwind gray-400
        },
        ticks: {
          color: '#9ca3af', // Tailwind gray-400
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Temperature (°C)',
          color: '#9ca3af', // Tailwind gray-400
        },
        ticks: {
          color: '#9ca3af', // Tailwind gray-400
        },
      },
    },
    plugins: {
      legend: {
        display: true,
        labels: {
          color: '#9ca3af', // Tailwind gray-400
        },
      },
      tooltip: {
        backgroundColor: '#f9fafb', // Tailwind gray-50 for tooltip background
        titleColor: '#374151', // Tailwind gray-700 for tooltip text
        bodyColor: '#6b7280', // Tailwind gray-600 for tooltip body
        borderColor: '#e5e7eb', // Tailwind gray-200 for tooltip border
        borderWidth: 1, // Border width for tooltip
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
            data: newData.map(item => item.temperature),
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
