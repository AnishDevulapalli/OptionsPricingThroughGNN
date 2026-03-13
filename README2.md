# 📈 HTGNN Options Pricing Engine

### *Predicting "Smart Sigma" using Hypergraph Temporal Graph Neural Networks*

This project is a full-stack options pricing application that replaces traditional Black-Scholes implied volatility with a **Hypergraph Temporal Graph Neural Network (HTGNN)**. By learning from market structure (sectors) and temporal stress (volatility clustering), the model provides a more accurate "Smart Sigma" for option valuation.

---

## 🚀 System Architecture

The project is split into three core components:
1.  **AI Research Layer (`/notebooks`):** An HTGNN model trained on the **Gauss314** dataset (3.5M rows) using PyTorch Geometric.
2.  **Inference API (`/backend`):** A FastAPI server that fetches live market data from Yahoo Finance, scales it, and provides real-time IV predictions.
3.  **Trader Interface (`/frontend`):** A React-based dashboard for uploading option chains (CSVs) and visualizing fair price vs. market price.



---

## 🛠️ Tech Stack

-   **Deep Learning:** PyTorch, PyTorch Geometric (Hypergraph Convolutions)
-   **Data Science:** Pandas, NumPy, Scikit-learn, Hugging Face Datasets
-   **Backend:** FastAPI, Uvicorn, YFinance
-   **Frontend:** React, Tailwind CSS, Recharts
-   **Infrastructure:** Ngrok (Tunneling), Google Colab (Training GPU)

---

## 📦 Getting Started

### 1. Backend Setup (API)
Navigate to the backend folder and install the dependencies:
```bash
cd backend
pip install -r requirements.txt
python main.py
