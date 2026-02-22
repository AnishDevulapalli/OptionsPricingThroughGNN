/**
 * Black-Scholes Option Pricing (Client-side)
 * Uses jStat for statistical functions
 */

import jStat from 'jstat'

/**
 * Calculate Black-Scholes option price
 * @param {number} S - Current stock price
 * @param {number} K - Strike price
 * @param {number} T - Time to expiration (years)
 * @param {number} r - Risk-free rate
 * @param {number} sigma - Volatility
 * @param {string} optionType - 'call' or 'put'
 * @returns {object} Pricing result with Greeks
 */
export function blackScholes(S, K, T, r, sigma, optionType) {
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

  const d1 = (Math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * Math.sqrt(T))
  const d2 = d1 - sigma * Math.sqrt(T)

  let price, delta

  if (optionType.toLowerCase() === 'call') {
    price = S * jStat.normal.cdf(d1, 0, 1) - K * Math.exp(-r * T) * jStat.normal.cdf(d2, 0, 1)
    delta = jStat.normal.cdf(d1, 0, 1)
  } else {
    price = K * Math.exp(-r * T) * jStat.normal.cdf(-d2, 0, 1) - S * jStat.normal.cdf(-d1, 0, 1)
    delta = -jStat.normal.cdf(-d1, 0, 1)
  }

  // Greeks
  const gamma = jStat.normal.pdf(d1, 0, 1) / (S * sigma * Math.sqrt(T))

  let theta
  if (optionType.toLowerCase() === 'call') {
    theta = (
      -(S * jStat.normal.pdf(d1, 0, 1) * sigma) / (2 * Math.sqrt(T))
      - r * K * Math.exp(-r * T) * jStat.normal.cdf(d2, 0, 1)
    ) / 365.0
  } else {
    theta = (
      -(S * jStat.normal.pdf(d1, 0, 1) * sigma) / (2 * Math.sqrt(T))
      + r * K * Math.exp(-r * T) * jStat.normal.cdf(-d2, 0, 1)
    ) / 365.0
  }

  const vega = (S * jStat.normal.pdf(d1, 0, 1) * Math.sqrt(T)) / 100.0

  return {
    price,
    delta,
    gamma,
    theta,
    vega,
  }
}

/**
 * Calculate implied volatility using binary search
 * @param {number} marketPrice - Observed market price
 * @param {number} S - Current stock price
 * @param {number} K - Strike price
 * @param {number} T - Time to expiration (years)
 * @param {number} r - Risk-free rate
 * @param {string} optionType - 'call' or 'put'
 * @returns {number} Implied volatility
 */
export function impliedVolatility(marketPrice, S, K, T, r, optionType) {
  let low = 0.001
  let high = 5.0
  let mid
  const tolerance = 1e-6
  const maxIterations = 100

  for (let i = 0; i < maxIterations; i++) {
    mid = (low + high) / 2
    const price = blackScholes(S, K, T, r, mid, optionType).price
    const error = price - marketPrice

    if (Math.abs(error) < tolerance) {
      return mid
    }

    if (error > 0) {
      high = mid
    } else {
      low = mid
    }
  }

  return mid
}
