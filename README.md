# OptionsPricingThroughGNN
This project deals with the pricing of European and American style options through the estimation of volatility through graph neural networks. 

# 🚀 HTGNN-Pricing-Engine
### **State-of-the-Art Option Pricing via Hypergraph Temporal Graph Neural Networks**

![Build Status](https://img.shields.io/badge/Build-2026.1-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![React](https://img.shields.io/badge/Frontend-React%2018-cyan)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 Project Vision
Standard models like Black-Scholes fail to capture the "Volatility Smile" because they assume constant volatility. This project implements a **Hypergraph Temporal Graph Neural Network (HTGNN)** to predict dynamic, fair-value Implied Volatility ($\sigma$). 

By training on the **Gauss314** dataset (3.5M rows), our model learns structural market relationships (Sectors) and temporal patterns (Market Stress) to provide traders with a competitive edge in European and American markets.



---

## 📐 System Architecture

Our platform utilizes a hybrid environment to balance AI compute power with UI responsiveness:

1.  **The Brain (Google Colab):**
    * **HTGNN Model:** Built with `PyTorch Geometric`.
    * **Data Scraper:** Real-time extraction via `yfinance`.
    * **The Bridge:** `FastAPI` hosted via `Ngrok` to serve predictions.

2.  **The Engine (VS Code / Local):**
    * **Frontend:** React (Vite) for a professional Trader Dashboard.
    * **Math Engines:** `jStat` for European (Black-Scholes) and custom iterative trees for American (Binomial).

```mermaid
graph TD;
    A[Trader CSV Upload] --> B[React Frontend];
    B --> C{FastAPI Gateway};
    C --> D[HTGNN Volatility Predictor];
    D --> E[Smart Sigma Output];
    E --> F[Black-Scholes / Binomial Math];
    F --> G[Fair Value Result];
