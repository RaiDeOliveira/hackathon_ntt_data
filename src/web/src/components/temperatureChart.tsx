import React, { useState, useEffect } from 'react';
import { SingleValueChart } from './singleValueChart';
import { createWebSocketConnection, receiveMessage } from '../services/webSocket';

export const TemperatureChart: React.FC = () => {
    const [temperature, setTemperature] = useState<number | null>(null);
    const [humidity, setHumidity] = useState<number | null>(null);

    useEffect(() => {
        const initWebSocket = async () => {
            try {
            const ws = await createWebSocketConnection();
            console.log('WebSocket connected');

            while (true) {
                try {
                const message = await receiveMessage(ws);
                
                // Processar a mensagem recebida
                const jsonString = message.replace(/.*?b'/, '').replace(/'$/, '');
                const data = JSON.parse(jsonString);

                setTemperature(data.temperature);
                setHumidity(data.humidity);
                } catch (error) {
                console.error('Error processing WebSocket message:', error);
                }
            }
            } catch (error) {
            console.error('Failed to connect to WebSocket:', error);
            }
        };

        initWebSocket();
    }, []);

    const calculateWetBulb = () => {
        if (temperature !== null && humidity !== null) {
            const arctan = (x) => Math.atan(x);
            return (
                temperature * arctan(0.151977 * Math.sqrt(humidity + 8.313659)) + 0.00391838 * Math.sqrt(Math.pow(humidity,3)) * arctan(0.023101 * humidity) - arctan(humidity - 1.676331) + arctan(temperature + humidity) - 4.686035
            );
        }
        return null;
    };

    const calculateGlobeTemperature = () => {
        if (temperature !== null) {
            return (
                0.456 + 1.0335 * temperature
            );
        }
        return null;
    };

    const calculateIBUTG = () => {
        if (temperature !== null && humidity !== null) {
            return (
                0.7 * calculateWetBulb() + 0.3 * calculateGlobeTemperature()
            );
        }
        return null;
    }

    return (
        <div className="flex flex-col gap-4">
            <SingleValueChart title="Bulbo Seco" value={temperature || 0} />
            <SingleValueChart title="Bulbo Úmido" value={calculateWetBulb() || 0} />
            <SingleValueChart title="Termômetro de Globo" value={calculateGlobeTemperature() || 0} />
            <SingleValueChart title="IBUTG" value={calculateIBUTG() || 0} />
        </div>
    );
};
