import axios, { AxiosInstance } from 'axios';

const axiosInstance: AxiosInstance = axios.create({
  baseURL: '',
  timeout: 1000, 
  headers: { 'Content-Type': 'application/json' },
});

export default axiosInstance;
