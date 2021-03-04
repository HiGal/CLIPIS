import axios from "axios";

const api = axios.create({
    baseURL: 'https://api.clipis.co',
});

export const getImages = (text) => {
  return api.post('/text/search', {
    text
  })
}



