import axiosInstance from '../../utils/axiosInstance'

import { register, login } from '../auth'
console.log(require.resolve('../../utils/axiosInstance'))

jest.mock('../../utils/axiosInstance', () => ({
  post: jest.fn(),
  get: jest.fn(),
}))

describe('Auth API', () => {
  it('should successfully register a user', async () => {
    const mockResponse = { data: { id: 1, username: 'testuser', created_at: '2025-01-10' } }
    axiosInstance.post.mockResolvedValueOnce(mockResponse)

    const response = await register({ username: 'testuser', password: 'password123' })
    expect(response).toEqual(mockResponse.data)
    expect(axiosInstance.post).toHaveBeenCalledWith('/auth/register', {
      username: 'testuser',
      password: 'password123',
    })
  })

  it('should successfully log in a user', async () => {
    const mockResponse = { data: { access_token: 'mock-jwt-token' } }
    axiosInstance.post.mockResolvedValueOnce(mockResponse)

    const response = await login({ username: 'testuser', password: 'password123' })
    expect(response).toEqual(mockResponse.data)
    expect(axiosInstance.post).toHaveBeenCalledWith('/auth/login', {
      username: 'testuser',
      password: 'password123',
    })
  })
})
