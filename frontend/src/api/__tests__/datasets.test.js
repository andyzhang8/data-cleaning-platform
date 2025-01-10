import axiosInstance from '../../utils/axiosInstance'
import { uploadDataset, getDataset } from '../datasets'

console.log(require.resolve('../../utils/axiosInstance'))

jest.mock('../../utils/axiosInstance', () => ({
  post: jest.fn(),
  get: jest.fn(),
}))

describe('Datasets API', () => {
  it('should successfully upload a dataset', async () => {
    const mockResponse = { data: { id: 1, name: 'test.csv', file_path: '/uploads/test.csv' } }
    axiosInstance.post.mockResolvedValueOnce(mockResponse)

    const mockFile = new File(['content'], 'test.csv', { type: 'text/csv' })
    const response = await uploadDataset('test.csv', mockFile)

    expect(response).toEqual(mockResponse.data)
    expect(axiosInstance.post).toHaveBeenCalledWith(
      '/datasets/upload',
      expect.any(FormData),
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
  })

  it('should fetch dataset metadata by ID', async () => {
    const mockResponse = { data: { id: 1, name: 'test.csv', file_path: '/uploads/test.csv' } }
    axiosInstance.get.mockResolvedValueOnce(mockResponse)

    const response = await getDataset(1)
    expect(response).toEqual(mockResponse.data)
    expect(axiosInstance.get).toHaveBeenCalledWith('/datasets/1')
  })
})
