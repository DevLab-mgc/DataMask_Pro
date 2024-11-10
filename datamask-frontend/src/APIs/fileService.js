import apiClient from './apiClient';

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post('/files/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getFilesList = async () => {
  const response = await apiClient.get('/files/');
  return response.data;
};

export const getFileDetails = async (fileId) => {
  const response = await apiClient.get(`/files/${fileId}/`);
  return response.data;
};

export const processFile = async (fileId) => {
  const response = await apiClient.post(`/files/${fileId}/process/`);
  return response.data;
};

export const getProcessingLogs = async (fileId) => {
  const response = await apiClient.get('/logs/', {
    params: { file_upload: fileId }
  });
  return response.data;
};

export const getPIIDetections = async (fileId) => {
  const response = await apiClient.get('/detections/', {
    params: { file_upload: fileId }
  });
  return response.data;
};
