import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});


export async function getYoloInfo() {
  try {
    const response = await api.get('/getInfo');
    return response.data;
  } catch (error) {
    console.error('Error fetching YOLO data:', error);
    return null;
  }
}