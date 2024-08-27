import React from 'react';

interface SingleValueChartProps {
  title: string;
  value: number;
}

const ibutgMax = 23.2;

export const SingleValueChart: React.FC<SingleValueChartProps> = ({ title, value }) => {
    
    const isIbutgExceeded = value >= ibutgMax;
    let containerClassName;

    if (title === 'IBUTG') {
        containerClassName = isIbutgExceeded
        ? 'p-4 border rounded-lg shadow-md bg-red-400 text-black'
        : 'p-4 border rounded-lg shadow-md bg-green-400 text-black';
    } else {
        containerClassName = 'p-4 border rounded-lg shadow-md bg-white text-black';
    }

  return (
    <div className={containerClassName}>
      <h2 className="text-lg font-bold">{title}</h2>
      <div className="text-4xl font-bold">
        {value !== null ? `${value.toFixed(2)}` : 'Loading...'}
      </div>
    </div>
  );
};
