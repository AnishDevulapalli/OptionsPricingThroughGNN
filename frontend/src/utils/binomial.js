/**
 * Binomial Tree Option Pricing (Client-side)
 * For American options with early exercise
 */

/**
 * Calculate option price using binomial tree
 * @param {number} S - Current stock price
 * @param {number} K - Strike price
 * @param {number} T - Time to expiration (years)
 * @param {number} r - Risk-free rate
 * @param {number} sigma - Volatility
 * @param {string} optionType - 'call' or 'put'
 * @param {number} nSteps - Number of time steps (default 100)
 * @returns {object} Pricing result with Greeks
 */
export function binomialTree(S, K, T, r, sigma, optionType, nSteps = 100) {
  if (T <= 0) {
    const intrinsic = optionType === 'call' 
      ? Math.max(S - K, 0) 
      : Math.max(K - S, 0)
    
    return {
      price: intrinsic,
      delta: optionType === 'call' ? (S > K ? 1 : 0) : (S < K ? -1 : 0),
      gamma: 0,
      theta: 0,
      vega: 0,
    }
  }

  const dt = T / nSteps
  const u = Math.exp(sigma * Math.sqrt(dt))
  const d = 1 / u
  const p = (Math.exp(r * dt) - d) / (u - d)
  const discount = Math.exp(-r * dt)

  // Initialize option value tree
  const optionValues = []
  const stockPrices = []

  // Calculate terminal stock prices and option values
  for (let i = 0; i <= nSteps; i++) {
    stockPrices[i] = S * Math.pow(u, nSteps - i) * Math.pow(d, i)
    
    if (optionType.toLowerCase() === 'call') {
      optionValues[i] = Math.max(stockPrices[i] - K, 0)
    } else {
      optionValues[i] = Math.max(K - stockPrices[i], 0)
    }
  }

  // Backward induction with early exercise
  for (let step = nSteps - 1; step >= 0; step--) {
    for (let i = 0; i <= step; i++) {
      const stockPrice = S * Math.pow(u, step - i) * Math.pow(d, i)
      
      // Expected value from continuation
      const continuationValue = discount * (
        p * optionValues[i] + (1 - p) * optionValues[i + 1]
      )
      
      // Intrinsic value (early exercise)
      const intrinsicValue = optionType.toLowerCase() === 'call'
        ? Math.max(stockPrice - K, 0)
        : Math.max(K - stockPrice, 0)
      
      // American option: take max of continuation and intrinsic
      optionValues[i] = Math.max(continuationValue, intrinsicValue)
    }
  }

  const optionPrice = optionValues[0]

  // Calculate Greeks using finite differences
  const dS = 0.01
  const priceUp = binomialTree(S + dS, K, T, r, sigma, optionType, nSteps).price
  const priceDown = binomialTree(S - dS, K, T, r, sigma, optionType, nSteps).price
  
  const delta = (priceUp - priceDown) / (2 * dS)
  
  const priceCenter = optionPrice
  const gamma = (priceUp - 2 * priceCenter + priceDown) / (dS * dS)
  
  const dT = 1 / 365
  const priceFuture = T - dT > 0 
    ? binomialTree(S, K, T - dT, r, sigma, optionType, nSteps).price 
    : optionPrice
  const theta = (priceFuture - optionPrice) / dT
  
  const dSigma = 0.01
  const priceVolUp = binomialTree(S, K, T, r, sigma + dSigma, optionType, nSteps).price
  const priceVolDown = binomialTree(S, K, T, r, sigma - dSigma, optionType, nSteps).price
  const vega = (priceVolUp - priceVolDown) / (2 * dSigma) / 100.0

  return {
    price: optionPrice,
    delta,
    gamma,
    theta,
    vega,
  }
}
