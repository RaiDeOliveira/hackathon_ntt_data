import React from 'react';

interface SingleValueChartProps {
  title: string;
  value: number;
}

export const SingleValueChart: React.FC<SingleValueChartProps> = ({ title, value }) => {
  return (
    <div className="p-4 border rounded-lg shadow-md bg-white text-black">
      <h2 className="text-lg font-bold">{title}</h2>
      <div className="text-4xl font-bold">
        {value !== null ? `${value.toFixed(2)}` : 'Loading...'}
      </div>
    </div>
  );
};
