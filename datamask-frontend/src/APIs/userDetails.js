import apiClient from './apiClient';

export const getUserDetails = async () => {
  const response = await apiClient.get('/users/me/');
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await apiClient.post('/auth/login/', credentials);
  if (response.data.token) {
    localStorage.setItem('token', response.data.token);
  }
  return response.data;
};

export const registerUser = async (userData) => {
  const response = await apiClient.post('/auth/register/', userData);
  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem('token');
};
