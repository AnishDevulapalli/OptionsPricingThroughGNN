import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const pricingAPI = {
  /**
   * Price a single option
   */
  async priceOption(optionParams, style = 'european', useHTGNN = true) {
    const params = new URLSearchParams({
      style,
      use_htgnn: useHTGNN.toString(),
    })
    
    return apiClient.post(`/price?${params}`, optionParams)
  },

  /**
   * Price multiple options in batch
   */
  async priceBatch(options, style = 'european', useHTGNN = true) {
    return apiClient.post('/price/batch', {
      options,
      style,
      use_htgnn_volatility: useHTGNN,
    })
  },

  /**
   * Price options from CSV file
   */
  async priceFromCSV(file, style = 'european', useHTGNN = true) {
    const formData = new FormData()
    formData.append('file', file)
    
    const params = new URLSearchParams({
      style,
      use_htgnn: useHTGNN.toString(),
    })

    return apiClient.post(`/price/csv?${params}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  /**
   * Get predicted volatility for a ticker
   */
  async getVolatility(ticker, strike, expirationDays) {
    return apiClient.get(`/volatility/${ticker}`, {
      params: {
        strike,
        expiration_days: expirationDays,
      },
    })
  },

  /**
   * Health check
   */
  async healthCheck() {
    return apiClient.get('/health')
  },
}

export default apiClient
