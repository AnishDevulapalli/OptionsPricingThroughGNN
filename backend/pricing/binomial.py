"""
Binomial Tree Option Pricing Model
For American-style options with early exercise
"""

import numpy as np
from typing import Literal


class BinomialPricer:
    """Binomial tree pricing engine for American options"""
    
    def __init__(self):
        pass
    
    def price(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: Literal["call", "put"],
        n_steps: int = 100
    ) -> dict:
        """
        Calculate option price using binomial tree method
        
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
        n_steps : int
            Number of time steps in the tree
        
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
                intrinsic = max(S - K, 0)
            else:
                intrinsic = max(K - S, 0)
            
            return {
                "price": intrinsic,
                "delta": 1.0 if (option_type == "call" and S > K) or (option_type == "put" and S < K) else 0.0,
                "gamma": 0.0,
                "theta": 0.0,
                "vega": 0.0
            }
        
        dt = T / n_steps
        u = np.exp(sigma * np.sqrt(dt))  # Up factor
        d = 1 / u  # Down factor
        p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
        discount = np.exp(-r * dt)
        
        # Initialize stock price tree
        stock_prices = np.zeros((n_steps + 1, n_steps + 1))
        for i in range(n_steps + 1):
            for j in range(i + 1):
                stock_prices[j, i] = S * (u ** (i - j)) * (d ** j)
        
        # Initialize option value tree
        option_values = np.zeros((n_steps + 1, n_steps + 1))
        
        # Calculate terminal option values
        for j in range(n_steps + 1):
            if option_type.lower() == "call":
                option_values[j, n_steps] = max(stock_prices[j, n_steps] - K, 0)
            else:  # put
                option_values[j, n_steps] = max(K - stock_prices[j, n_steps], 0)
        
        # Backward induction with early exercise check
        for i in range(n_steps - 1, -1, -1):
            for j in range(i + 1):
                # Expected value from continuation
                continuation_value = discount * (
                    p * option_values[j, i + 1] + (1 - p) * option_values[j + 1, i + 1]
                )
                
                # Intrinsic value (early exercise)
                if option_type.lower() == "call":
                    intrinsic_value = max(stock_prices[j, i] - K, 0)
                else:  # put
                    intrinsic_value = max(K - stock_prices[j, i], 0)
                
                # American option: take max of continuation and intrinsic
                option_values[j, i] = max(continuation_value, intrinsic_value)
        
        option_price = option_values[0, 0]
        
        # Calculate Greeks using finite differences
        delta = self._calculate_delta(S, K, T, r, sigma, option_type, n_steps)
        gamma = self._calculate_gamma(S, K, T, r, sigma, option_type, n_steps)
        theta = self._calculate_theta(S, K, T, r, sigma, option_type, n_steps)
        vega = self._calculate_vega(S, K, T, r, sigma, option_type, n_steps)
        
        return {
            "price": float(option_price),
            "delta": float(delta),
            "gamma": float(gamma),
            "theta": float(theta),
            "vega": float(vega)
        }
    
    def _calculate_delta(
        self, S: float, K: float, T: float, r: float, sigma: float,
        option_type: str, n_steps: int, dS: float = 0.01
    ) -> float:
        """Calculate delta using finite differences"""
        price_up = self.price(S + dS, K, T, r, sigma, option_type, n_steps)["price"]
        price_down = self.price(S - dS, K, T, r, sigma, option_type, n_steps)["price"]
        return (price_up - price_down) / (2 * dS)
    
    def _calculate_gamma(
        self, S: float, K: float, T: float, r: float, sigma: float,
        option_type: str, n_steps: int, dS: float = 0.01
    ) -> float:
        """Calculate gamma using finite differences"""
        price_up = self.price(S + dS, K, T, r, sigma, option_type, n_steps)["price"]
        price_center = self.price(S, K, T, r, sigma, option_type, n_steps)["price"]
        price_down = self.price(S - dS, K, T, r, sigma, option_type, n_steps)["price"]
        return (price_up - 2 * price_center + price_down) / (dS ** 2)
    
    def _calculate_theta(
        self, S: float, K: float, T: float, r: float, sigma: float,
        option_type: str, n_steps: int, dT: float = 1/365
    ) -> float:
        """Calculate theta using finite differences (per day)"""
        if T - dT <= 0:
            return 0.0
        price_future = self.price(S, K, T - dT, r, sigma, option_type, n_steps)["price"]
        price_now = self.price(S, K, T, r, sigma, option_type, n_steps)["price"]
        return (price_future - price_now) / dT
    
    def _calculate_vega(
        self, S: float, K: float, T: float, r: float, sigma: float,
        option_type: str, n_steps: int, dSigma: float = 0.01
    ) -> float:
        """Calculate vega using finite differences (per 1% change)"""
        price_up = self.price(S, K, T, r, sigma + dSigma, option_type, n_steps)["price"]
        price_down = self.price(S, K, T, r, sigma - dSigma, option_type, n_steps)["price"]
        return (price_up - price_down) / (2 * dSigma) / 100.0  # Per 1%
