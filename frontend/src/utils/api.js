import axios from 'axios';

export const API_BASE_URL = "https://probable-pancake-9v5r57qxr7xf6xp-8000.app.github.dev/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function testBackend() {
  try {
    const res = await axios.get('https://probable-pancake-9v5r57qxr7xf6xp-8000.app.github.dev/hello');
    console.log('Backend /hello response:', res.data);
  } catch (err) {
    console.error('Error calling backend /hello:', err);
  }
}

