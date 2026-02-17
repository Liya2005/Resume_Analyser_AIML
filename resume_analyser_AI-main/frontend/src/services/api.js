import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadResume = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const analyzeLinkedInUrl = (url) => {
  return api.post('/analyze-linkedin-url', { url });
};

export const getAnalyses = () => api.get('/analyses');

export const getAnalysis = (id) => api.get(`/analysis/${id}`);