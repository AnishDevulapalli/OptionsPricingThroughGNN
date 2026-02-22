import React, { useState } from 'react'
import CSVUpload from './CSVUpload'
import ManualInput from './ManualInput'
import ResultsTable from './ResultsTable'
import './Dashboard.css'

const Dashboard = () => {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleResults = (newResults) => {
    setResults(newResults)
    setError(null)
  }

  const handleError = (err) => {
    setError(err)
    setResults([])
  }

  const handleLoading = (isLoading) => {
    setLoading(isLoading)
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🚀 HTGNN Pricing Engine</h1>
        <p className="subtitle">State-of-the-Art Option Pricing via Hypergraph Temporal Graph Neural Networks</p>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <div className="input-section">
            <div className="card">
              <h2>📊 Option Pricing</h2>
              <p className="card-description">
                Upload a CSV file or enter option parameters manually to get fair value prices
                using HTGNN-predicted volatility.
              </p>
              
              <div className="input-tabs">
                <CSVUpload 
                  onResults={handleResults}
                  onError={handleError}
                  onLoading={handleLoading}
                />
                <ManualInput 
                  onResults={handleResults}
                  onError={handleError}
                  onLoading={handleLoading}
                />
              </div>
            </div>
          </div>

          {loading && (
            <div className="loading-overlay">
              <div className="spinner"></div>
              <p>Calculating option prices...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {results.length > 0 && (
            <div className="results-section">
              <div className="card">
                <h2>📈 Pricing Results</h2>
                <ResultsTable results={results} />
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="dashboard-footer">
        <p>Powered by HTGNN • Trained on Gauss314 Dataset (3.5M rows)</p>
      </footer>
    </div>
  )
}

export default Dashboard
