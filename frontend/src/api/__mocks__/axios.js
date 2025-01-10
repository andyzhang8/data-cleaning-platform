const mockAxios = jest.createMockFromModule('axios')

mockAxios.create = jest.fn(() => ({
  interceptors: {
    request: {
      use: jest.fn(),
    },
  },
  get: jest.fn(),
  post: jest.fn(),
}))

export default mockAxios
