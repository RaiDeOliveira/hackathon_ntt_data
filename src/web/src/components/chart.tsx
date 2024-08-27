import React from 'react';
import { Line } from 'react-chartjs-2';
import { ChartOptions, ChartData } from 'chart.js';
import 'chart.js/auto';

type ChartProps = {
  data: number[];
  labels: string[];
  label: string;
  color: string;
  limit?: number;
};

const Chart: React.FC<ChartProps> = ({ data, labels, label, color, limit = 20 }) => {

  const truncatedData = data.slice(-limit);
  const truncatedLabels = labels.slice(-limit);

  const chartData: ChartData<'line'> = {
    labels: truncatedLabels,
    datasets: [
      {
        label,
        data: truncatedData,
        borderColor: color,
        backgroundColor: `${color}33`, 
        fill: true,
        pointBorderWidth: 0
      },
    ],
  };

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
          text: 'Value',
        },
      },
    },
  };

  return (
    <div className="w-full h-56">
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default Chart;
