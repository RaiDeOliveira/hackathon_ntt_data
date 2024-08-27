import { useEffect, useState } from 'react';
import io from 'socket.io-client';
import

function VideoFeed() {
  const [videoSrc, setVideoSrc] = useState(''); // Para armazenar o vídeo
  const [peopleCount, setPeopleCount] = useState(0); // Para armazenar a contagem de pessoas

  useEffect(() => {
    // Conectar ao WebSocket do backend Flask
    const socket = io('http://localhost:5000');

    socket.on('video_feed', data => {
      console.log(data.num_people);
      // Atualiza o vídeo com o frame recebido
      setVideoSrc(`data:image/jpeg;base64,${data.frame}`);
      // Atualiza a contagem de pessoas
      setPeopleCount(data.num_people);
    });

    // Limpeza ao desmontar o componente
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div>
      <h1>Video Feed</h1>
      {/* Exibe a contagem de pessoas na tela */}
      <p>Number of people detected: {peopleCount}</p>
      {/* Exibe o feed de vídeo */}
      <img src={videoSrc} alt="Video feed" />
    </div>
  );
}

export default VideoFeed;