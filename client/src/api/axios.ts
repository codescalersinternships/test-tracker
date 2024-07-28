import axios, { AxiosInstance } from 'axios';

const axiosInstanceWithAuth: AxiosInstance = axios.create({
  baseURL: 'https://your-api-base-url.com', 
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ', 
  },
});

const axiosInstanceWithoutAuth: AxiosInstance = axios.create({
  baseURL: 'https://your-api-base-url.com',
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export { axiosInstanceWithAuth, axiosInstanceWithoutAuth };
