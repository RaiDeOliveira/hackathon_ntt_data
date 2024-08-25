import React from 'react';
import { TemperatureChart } from '../components/temperatureChart';

export const Temperature: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
        <TemperatureChart />
    </div>
  );
};