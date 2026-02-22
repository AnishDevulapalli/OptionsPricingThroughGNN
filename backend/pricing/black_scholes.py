"""
Black-Scholes Option Pricing Model
For European-style options
"""

import numpy as np
from scipy.stats import norm
from typing import Literal


class BlackScholesPricer:
    """Black-Scholes pricing engine for European options"""
    
    def __init__(self):
        pass
    
    def d1_d2(self, S: float, K: float, T: float, r: float, sigma: float) -> tuple:
        """
        Calculate d1 and d2 for Black-Scholes formula
        
        Parameters:
        -----------
        S : float
            Current stock price
        K : float
            Strike price
        T : float
            Time to expiration (in years)
        r : float
            Risk-free interest rate
        sigma : float
            Volatility (annualized)
        
        Returns:
        --------
        tuple : (d1, d2)
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2
    
    def price(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: Literal["call", "put"]
    ) -> dict:
        """
        Calculate Black-Scholes option price
        
        Parameters:
        -----------
        S : float
            Current stock price
        K : float
            Strike price
        T : float
            Time to expiration (in years)
        r : float
            Risk-free interest rate
        sigma : float
            Volatility (annualized)
        option_type : str
            "call" or "put"
        
        Returns:
        --------
        dict : {
            "price": float,
            "delta": float,
            "gamma": float,
            "theta": float,
            "vega": float
        }
        """
        if T <= 0:
            # Option expired
            if option_type == "call":
                return {
                    "price": max(S - K, 0),
                    "delta": 1.0 if S > K else 0.0,
                    "gamma": 0.0,
                    "theta": 0.0,
                    "vega": 0.0
                }
            else:
                return {
                    "price": max(K - S, 0),
                    "delta": -1.0 if S < K else 0.0,
                    "gamma": 0.0,
                    "theta": 0.0,
                    "vega": 0.0
                }
        
        d1, d2 = self.d1_d2(S, K, T, r, sigma)
        
        if option_type.lower() == "call":
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            delta = norm.cdf(d1)
        else:  # put
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            delta = -norm.cdf(-d1)
        
        # Greeks
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        
        if option_type.lower() == "call":
            theta = (
                -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                - r * K * np.exp(-r * T) * norm.cdf(d2)
            ) / 365.0  # Per day
        else:  # put
            theta = (
                -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                + r * K * np.exp(-r * T) * norm.cdf(-d2)
            ) / 365.0  # Per day
        
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100.0  # Per 1% change in volatility
        
        return {
            "price": float(price),
            "delta": float(delta),
            "gamma": float(gamma),
            "theta": float(theta),
            "vega": float(vega)
        }
    
    def implied_volatility(
        self,
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: Literal["call", "put"],
        max_iterations: int = 100,
        tolerance: float = 1e-6
    ) -> float:
        """
        Calculate implied volatility using Newton-Raphson method
        
        Parameters:
        -----------
        market_price : float
            Observed market price of the option
        S, K, T, r : float
            Standard Black-Scholes parameters
        option_type : str
            "call" or "put"
        max_iterations : int
            Maximum iterations for convergence
        tolerance : float
            Convergence tolerance
        
        Returns:
        --------
        float : Implied volatility
        """
        # Initial guess
        sigma = 0.2
        
        for _ in range(max_iterations):
            result = self.price(S, K, T, r, sigma, option_type)
            price = result["price"]
            vega = result["vega"]
            
            # Check convergence
            error = price - market_price
            if abs(error) < tolerance:
                return sigma
            
            # Newton-Raphson update
            if vega < 1e-10:  # Avoid division by zero
                sigma += 0.01
            else:
                sigma = sigma - error / (vega * 100)  # vega is per 1%, so multiply by 100
            
            # Bounds check
            sigma = max(0.001, min(5.0, sigma))
        
        return sigma
