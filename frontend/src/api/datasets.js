import axios from '../utils/axiosInstance'


export const uploadDataset = async (name, file) => {
  try {
    const formData = new FormData()
    formData.append('name', name)
    formData.append('file', file)

    const response = await axios.post('/datasets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw error.response?.data || 'An error occurred during dataset upload.'
  }
}

export const getDataset = async (datasetId) => {
  try {
    const response = await axios.get(`/datasets/${datasetId}`)
    return response.data
  } catch (error) {
    throw error.response?.data || 'An error occurred while fetching the dataset.'
  }
}
