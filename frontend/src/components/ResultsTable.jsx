import React from 'react'
import './ResultsTable.css'

const ResultsTable = ({ results }) => {
  if (!results || results.length === 0) {
    return <p>No results to display</p>
  }

  return (
    <div className="results-table-container">
      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Underlying</th>
              <th>Type</th>
              <th>Strike</th>
              <th>Current Price</th>
              <th>Expiration (Days)</th>
              <th>Volatility (σ)</th>
              <th>Fair Value</th>
              <th>Delta</th>
              <th>Gamma</th>
              <th>Theta</th>
              <th>Vega</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index}>
                <td className="ticker">{result.underlying}</td>
                <td>
                  <span className={`option-type ${result.option_type}`}>
                    {result.option_type.toUpperCase()}
                  </span>
                </td>
                <td>${result.strike.toFixed(2)}</td>
                <td>${result.current_price.toFixed(2)}</td>
                <td>{result.expiration_days}</td>
                <td className="volatility">{(result.volatility * 100).toFixed(2)}%</td>
                <td className="fair-value">${result.fair_value.toFixed(2)}</td>
                <td>{result.delta !== null ? result.delta.toFixed(4) : 'N/A'}</td>
                <td>{result.gamma !== null ? result.gamma.toFixed(6) : 'N/A'}</td>
                <td>{result.theta !== null ? result.theta.toFixed(4) : 'N/A'}</td>
                <td>{result.vega !== null ? result.vega.toFixed(4) : 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="results-summary">
        <p>
          <strong>Total Options Priced:</strong> {results.length}
        </p>
        <p>
          <strong>Average Fair Value:</strong> $
          {(results.reduce((sum, r) => sum + r.fair_value, 0) / results.length).toFixed(2)}
        </p>
      </div>
    </div>
  )
}

export default ResultsTable
