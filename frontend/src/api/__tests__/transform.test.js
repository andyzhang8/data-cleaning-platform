import axiosInstance from '../../utils/axiosInstance'
import { startTransformation, checkStatus } from '../transform'

console.log(require.resolve('../../utils/axiosInstance'))

jest.mock('../../utils/axiosInstance', () => ({
  post: jest.fn(),
  get: jest.fn(),
}))

describe('Transform API', () => {
  it('should start a transformation task', async () => {
    const mockResponse = { data: { task_id: 'abc123', message: 'Dataset transformation started.' } }
    axiosInstance.post.mockResolvedValueOnce(mockResponse)

    const response = await startTransformation(1, { drop_columns: ['col1'] })
    expect(response).toEqual(mockResponse.data)
    expect(axiosInstance.post).toHaveBeenCalledWith('/transform/1', { drop_columns: ['col1'] })
  })

  it('should check the status of a transformation task', async () => {
    const mockResponse = { data: { task_id: 'abc123', status: 'Task completed', result: '/path/to/result.csv' } }
    axiosInstance.get.mockResolvedValueOnce(mockResponse)

    const response = await checkStatus('abc123')
    expect(response).toEqual(mockResponse.data)
    expect(axiosInstance.get).toHaveBeenCalledWith('/transform/status/abc123')
  })
})
