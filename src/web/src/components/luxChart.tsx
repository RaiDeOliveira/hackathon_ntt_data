import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import { ChartOptions, ChartData } from 'chart.js';
import 'chart.js/auto';
import useWebSocket from 'react-use-websocket';

type SensorData = {
  id: number;
  temperature: number;
  humidity: number;
  lux: number;
  noise: number;
  timestamp: string;
};

export const LuxChart: React.FC = () => {
  const [data, setData] = useState<SensorData[]>([]);
  const [chartData, setChartData] = useState<ChartData<'line'>>({
    labels: [],
    datasets: [
      {
        label: 'Lux (lx)',
        data: [],
        borderColor: '#f59e0b', // Tailwind yellow-400
        backgroundColor: 'rgba(245, 158, 11, 0.2)',
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
        title: {
          display: true,
          text: 'Timestamp',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Lux',
        },
        min: 0,
      },
    },
  };

  useWebSocket('ws://localhost:8000/api/ws/sensor', {
    onMessage: (event) => {
      const receivedData: SensorData[] = JSON.parse(event.data);
      console.log('Received WebSocket message:', ...receivedData);

      setData((prevData) => {
        const newData = [...prevData, ...receivedData].slice(-25);

        setChartData((prevChartData) => ({
          ...prevChartData,
          labels: newData.map(item => new Date(item.timestamp).toLocaleTimeString().slice(0, -3)),
          datasets: [{
            ...prevChartData.datasets[0],
            data: newData.map(item => item.lux),
          }],
        }));

        return newData;
      });
    },
  });

  return (
    <div className="flex-1 p-4 border border-gray-500 rounded-lg shadow-md bg-white">
      {data.length > 0 ? (
        <Line data={chartData} options={chartOptions} />
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
};
