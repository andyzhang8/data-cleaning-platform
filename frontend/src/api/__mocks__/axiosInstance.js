import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // Update to match your API URL
  headers: {
    'Content-Type': 'application/json',
  },
})

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken') // Retrieve token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export default axiosInstance
