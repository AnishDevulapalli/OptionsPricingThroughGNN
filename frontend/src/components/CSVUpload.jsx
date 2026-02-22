import React, { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { pricingAPI } from '../services/api'
import './CSVUpload.css'

const CSVUpload = ({ onResults, onError, onLoading }) => {
  const [style, setStyle] = useState('european')
  const [useHTGNN, setUseHTGNN] = useState(true)

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    onLoading(true)
    onError(null)

    try {
      const response = await pricingAPI.priceFromCSV(file, style, useHTGNN)
      
      if (response.data.results && response.data.results.length > 0) {
        onResults(response.data.results)
      } else {
        onError('No results returned. Please check your CSV format.')
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to process CSV file'
      onError(errorMsg)
    } finally {
      onLoading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv']
    },
    multiple: false
  })

  return (
    <div className="csv-upload">
      <h3>📁 Upload CSV File</h3>
      <p className="section-description">
        Upload a CSV file with option parameters. Required columns: underlying, strike, expiration_days, option_type
      </p>

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

      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="dropzone-content">
          {isDragActive ? (
            <p>Drop the CSV file here...</p>
          ) : (
            <>
              <div className="upload-icon">📤</div>
              <p>Drag & drop a CSV file here, or click to select</p>
              <p className="hint">CSV format: underlying, strike, expiration_days, option_type (call/put)</p>
            </>
          )}
        </div>
      </div>

      <div className="csv-example">
        <strong>Example CSV format:</strong>
        <pre>
{`underlying,strike,expiration_days,option_type
AAPL,150,30,call
TSLA,200,45,put
MSFT,350,60,call`}
        </pre>
      </div>
    </div>
  )
}

export default CSVUpload
