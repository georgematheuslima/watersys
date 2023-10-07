import axios from "axios"
export const axiosInstance = axios.create({
  baseURL: 'http://localhost:3333',
//   withCredentials: true, // Habilita o envio e recebimento de cookies
});