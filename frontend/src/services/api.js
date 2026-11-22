import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token if available in localStorage
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('mediscan_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle 401 unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // If unauthorized and not on login/register/landing, clear token
      const isAuthRoute = window.location.pathname.startsWith('/login') || window.location.pathname.startsWith('/register') || window.location.pathname === '/';
      if (!isAuthRoute) {
        localStorage.removeItem('mediscan_token');
        localStorage.removeItem('mediscan_user');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
