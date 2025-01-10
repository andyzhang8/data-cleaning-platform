import axios from '../utils/axiosInstance'

export const startTransformation = async (datasetId, operations) => {
  try {
    const response = await axios.post(`/transform/${datasetId}`, operations)
    return response.data
  } catch (error) {
    throw error.response?.data || 'An error occurred while starting the transformation.'
  }
}

export const checkStatus = async (taskId) => {
  try {
    const response = await axios.get(`/transform/status/${taskId}`)
    return response.data
  } catch (error) {
    throw error.response?.data || 'An error occurred while checking the task status.'
  }
}
