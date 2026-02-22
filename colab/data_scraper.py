"""
Data Scraper for Options Market Data
Fetches real-time data using yfinance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time


def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical stock data for a ticker
    
    Args:
        ticker: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        DataFrame with OHLCV data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()


def calculate_historical_volatility(prices: pd.Series, window: int = 30) -> float:
    """
    Calculate historical volatility from price series
    
    Args:
        prices: Series of closing prices
        window: Rolling window size in days
    
    Returns:
        Annualized volatility
    """
    returns = prices.pct_change().dropna()
    if len(returns) < window:
        return returns.std() * np.sqrt(252)  # Annualized
    rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)
    return rolling_vol.iloc[-1] if not rolling_vol.empty else 0.2


def fetch_option_data(
    tickers: List[str],
    days: int = 365,
    include_options: bool = False
) -> pd.DataFrame:
    """
    Fetch comprehensive market data for multiple tickers
    
    Args:
        tickers: List of stock ticker symbols
        days: Number of days of historical data
        include_options: Whether to fetch option chain data (slower)
    
    Returns:
        DataFrame with market data
    """
    all_data = []
    
    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}...")
            
            # Fetch stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period=f"{days}d")
            
            if hist.empty:
                continue
            
            # Calculate features
            current_price = hist['Close'].iloc[-1]
            historical_vol = calculate_historical_volatility(hist['Close'])
            
            # Get company info
            info = stock.info
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            
            # Create feature row
            row = {
                'ticker': ticker,
                'date': hist.index[-1],
                'current_price': current_price,
                'historical_volatility': historical_vol,
                'sector': sector,
                'industry': industry,
                'volume': hist['Volume'].iloc[-1],
                'high_52w': hist['High'].max(),
                'low_52w': hist['Low'].min(),
            }
            
            # Add option data if requested
            if include_options:
                try:
                    opt = stock.option_chain()
                    if opt.calls is not None and not opt.calls.empty:
                        # Get ATM call option
                        atm_call = opt.calls.iloc[len(opt.calls) // 2]
                        row['atm_strike'] = atm_call['strike']
                        row['atm_call_iv'] = atm_call.get('impliedVolatility', np.nan)
                except:
                    pass
            
            all_data.append(row)
            
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue
    
    return pd.DataFrame(all_data)


def create_training_dataset(
    tickers: List[str],
    output_file: str = "training_data.csv"
) -> pd.DataFrame:
    """
    Create a training dataset for HTGNN model
    
    Args:
        tickers: List of stock tickers
        output_file: Output CSV file path
    
    Returns:
        DataFrame with training data
    """
    print("Fetching market data...")
    df = fetch_option_data(tickers, days=365, include_options=True)
    
    if df.empty:
        print("No data fetched!")
        return df
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Training data saved to {output_file}")
    print(f"Total rows: {len(df)}")
    
    return df


if __name__ == "__main__":
    # Example usage
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'META', 'NVDA']
    df = create_training_dataset(tickers, "gauss314_sample.csv")
    print(df.head())
