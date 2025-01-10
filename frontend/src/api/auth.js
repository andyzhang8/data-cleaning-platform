import axios from '../utils/axiosInstance'

export const register = async (userData) => {
  try {
    console.log('Register function called with:', userData)
    const response = await axios.post('/auth/register', userData)
    console.log('Axios response in register:', response)
    return response.data
  } catch (error) {
    console.error('Error in register:', error.response?.data || error.message)
    throw error.response?.data || 'An error occurred during registration.'
  }
}

export const login = async (userData) => {
  try {
    console.log('Login function called with:', userData)
    const response = await axios.post('/auth/login', userData)
    console.log('Axios response in login:', response)
    return response.data
  } catch (error) {
    console.error('Error in login:', error.response?.data || error.message)
    throw error.response?.data || 'An error occurred during login.'
  }
}
