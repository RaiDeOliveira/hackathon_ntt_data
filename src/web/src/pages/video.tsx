import { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { SingleValueChart } from '../components/singleValueChart';

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
    <div className='flex flex-col items-center justify-center min-h-screen p-4'>
      <h1 className='text-3xl font-bold mb-4'>Video Feed</h1>
      <div className='flex flex-col md:flex-row gap-6 items-center'>
        <SingleValueChart title={"Pessoas Detectadas"} value={peopleCount} />
        <div className='relative'>
          <img src={videoSrc} alt="Video feed" className='rounded-lg shadow-lg' />
          {/* Adicione uma borda ou sombra ao redor do vídeo, se desejar */}
        </div>
      </div>
    </div>
  );
}

export default VideoFeed;