import React, { useState, useCallback } from 'react';
import { SingleValueChart } from './singleValueChart';
import useWebSocket from 'react-use-websocket';

export const Temperature: React.FC = () => {
    const [temperature, setTemperature] = useState<number | null>(null);
    const [humidity, setHumidity] = useState<number | null>(null);

    useWebSocket('ws://localhost:8000/api/ws/', {
        onMessage: (event) => {
            const message = event.data;
            // Processar a mensagem recebida
            try {
                const data = JSON.parse(message);
                console.log('Parsed data:', data);

                setTemperature(data.temperature);
                setHumidity(data.humidity);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        },
        onError: (error) => {
            console.error('Error processing WebSocket message:', error);
        },
    });

    const calculateWetBulb = useCallback(() => {
        if (temperature !== null && humidity !== null) {
            const arctan = (x) => Math.atan(x);
            return (
                temperature * arctan(0.151977 * Math.sqrt(humidity + 8.313659)) + 0.00391838 * Math.sqrt(Math.pow(humidity, 3)) * arctan(0.023101 * humidity) - arctan(humidity - 1.676331) + arctan(temperature + humidity) - 4.686035
            );
        }
        return null;
    }, [temperature, humidity]);

    const calculateGlobeTemperature = useCallback(() => {
        if (temperature !== null) {
            return (
                0.456 + 1.0335 * temperature
            );
        }
        return null;
    }, [temperature]);

    const calculateIBUTG = useCallback(() => {
        if (temperature !== null && humidity !== null) {
            return (
                0.7 * calculateWetBulb() + 0.3 * calculateGlobeTemperature()
            );
        }
        return null;
    }, [temperature, humidity, calculateWetBulb, calculateGlobeTemperature]);

    return (
        <div className="flex flex-col gap-5">
            <SingleValueChart title="Bulbo Seco" value={temperature || 0} />
            <SingleValueChart title="Bulbo Úmido" value={calculateWetBulb() || 0} />
            <SingleValueChart title="Termômetro de Globo" value={calculateGlobeTemperature() || 0} />
            <SingleValueChart title="IBUTG" value={calculateIBUTG() || 0} />
        </div>
    );
};
