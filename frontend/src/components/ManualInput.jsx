import React, { useState } from 'react'
import { pricingAPI } from '../services/api'
import './ManualInput.css'

const ManualInput = ({ onResults, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    underlying: '',
    strike: '',
    expiration_days: '',
    option_type: 'call',
    current_price: '',
    risk_free_rate: '0.05'
  })
  const [style, setStyle] = useState('european')
  const [useHTGNN, setUseHTGNN] = useState(true)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    onLoading(true)
    onError(null)

    try {
      const optionParams = {
        underlying: formData.underlying.toUpperCase(),
        strike: parseFloat(formData.strike),
        expiration_days: parseInt(formData.expiration_days),
        option_type: formData.option_type,
        current_price: formData.current_price ? parseFloat(formData.current_price) : null,
        risk_free_rate: parseFloat(formData.risk_free_rate)
      }

      const response = await pricingAPI.priceOption(optionParams, style, useHTGNN)
      onResults([response.data])
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to price option'
      onError(errorMsg)
    } finally {
      onLoading(false)
    }
  }

  return (
    <div className="manual-input">
      <h3>✏️ Manual Input</h3>
      <p className="section-description">
        Enter option parameters manually for single option pricing
      </p>

      <form onSubmit={handleSubmit} className="option-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="underlying">Underlying Ticker *</label>
            <input
              type="text"
              id="underlying"
              name="underlying"
              value={formData.underlying}
              onChange={handleChange}
              placeholder="AAPL"
              required
              maxLength={10}
            />
          </div>

          <div className="form-group">
            <label htmlFor="strike">Strike Price *</label>
            <input
              type="number"
              id="strike"
              name="strike"
              value={formData.strike}
              onChange={handleChange}
              placeholder="150.00"
              step="0.01"
              min="0.01"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="expiration_days">Days to Expiration *</label>
            <input
              type="number"
              id="expiration_days"
              name="expiration_days"
              value={formData.expiration_days}
              onChange={handleChange}
              placeholder="30"
              min="1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="option_type">Option Type *</label>
            <select
              id="option_type"
              name="option_type"
              value={formData.option_type}
              onChange={handleChange}
              required
            >
              <option value="call">Call</option>
              <option value="put">Put</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="current_price">Current Price (optional)</label>
            <input
              type="number"
              id="current_price"
              name="current_price"
              value={formData.current_price}
              onChange={handleChange}
              placeholder="Auto-fetch if empty"
              step="0.01"
              min="0.01"
            />
          </div>

          <div className="form-group">
            <label htmlFor="risk_free_rate">Risk-Free Rate</label>
            <input
              type="number"
              id="risk_free_rate"
              name="risk_free_rate"
              value={formData.risk_free_rate}
              onChange={handleChange}
              step="0.001"
              min="0"
              max="1"
            />
          </div>
        </div>

        <div className="options-config">
          <div className="config-group">
            <label>
              <input
                type="radio"
                value="european"
                checked={style === 'european'}
                onChange={(e) => setStyle(e.target.value)}
              />
              European Style
            </label>
            <label>
              <input
                type="radio"
                value="american"
                checked={style === 'american'}
                onChange={(e) => setStyle(e.target.value)}
              />
              American Style
            </label>
          </div>

          <div className="config-group">
            <label>
              <input
                type="checkbox"
                checked={useHTGNN}
                onChange={(e) => setUseHTGNN(e.target.checked)}
              />
              Use HTGNN Volatility
            </label>
          </div>
        </div>

        <button type="submit" className="submit-button">
          Calculate Fair Value
        </button>
      </form>
    </div>
  )
}

export default ManualInput
