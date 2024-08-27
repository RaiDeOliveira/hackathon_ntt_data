const WS_URL = 'ws://localhost:8000/api/ws/';

export const createWebSocketConnection = () => {
  const ws = new WebSocket(WS_URL);

  return new Promise((resolve, reject) => {
    ws.onopen = () => {
      console.log('WebSocket connection established.');
      resolve(ws);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      reject(new Error('WebSocket connection failed'));
    };
  });
};

export const receiveMessage = (ws) => {
  return new Promise((resolve, reject) => {
    ws.onmessage = (event) => {
      resolve(event.data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      reject(new Error('WebSocket error'));
    };
  });
};
