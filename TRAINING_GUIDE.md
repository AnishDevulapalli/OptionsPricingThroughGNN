# Complete Training Guide

## Overview

This guide walks you through training the HTGNN model and setting up the complete system.

## Prerequisites

1. **Google Colab Account** (free tier works)
2. **Ngrok Account** (free tier works) - Get token from https://dashboard.ngrok.com/get-started/your-authtoken
3. **Gauss314 Dataset** (optional) - If you have it, great! Otherwise, we'll use the data scraper

## Step-by-Step Instructions

### Step 1: Open the Notebook

1. Go to Google Colab: https://colab.research.google.com/
2. Upload `colab/HTGNN_Model_Training.ipynb`
3. Or upload `colab/data_scraper.py` first if you want to use the scraper

### Step 2: Install Dependencies

Run the first cell to install all required packages. This will take a few minutes.

### Step 3: Load Data

**Option A: Use Gauss314 Dataset (if you have it)**
```python
# In cell 6, uncomment:
df = pd.read_csv('gauss314_dataset.csv')
```

**Option B: Use Data Scraper (Recommended for testing)**
- The notebook will automatically use the data scraper
- It fetches real market data from yfinance
- Takes 5-10 minutes for ~10 tickers

### Step 4: Train the Model

1. Run all cells sequentially
2. The training will:
   - Build hypergraph structure from sector data
   - Prepare features and targets
   - Train for up to 100 epochs with early stopping
   - Save the best model automatically

**Expected Training Time:**
- Small dataset (10 tickers): 5-15 minutes
- Medium dataset (50 tickers): 15-30 minutes
- Large dataset (Gauss314): 1-3 hours

### Step 5: Set Up Inference Server

1. **Get Ngrok Token:**
   - Sign up at https://dashboard.ngrok.com
   - Copy your authtoken

2. **In the notebook, before running the FastAPI cell:**
   ```python
   ngrok.set_auth_token("YOUR_NGROK_TOKEN_HERE")
   ```

3. **Run the FastAPI cell** - This will:
   - Load your trained model
   - Start the FastAPI server
   - Expose it via Ngrok
   - Print the public URL

4. **Copy the Ngrok URL** (e.g., `https://abc123.ngrok.io`)

### Step 6: Connect Backend

1. **Create `backend/.env` file:**
   ```env
   HTGNN_ENDPOINT=https://your-ngrok-url.ngrok.io
   ```

2. **Start your local backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Start your frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Step 7: Test the System

1. Open http://localhost:5173
2. Upload `example_options.csv` or enter options manually
3. The system will:
   - Call your HTGNN model via Ngrok
   - Get predicted volatility
   - Calculate option prices using Black-Scholes/Binomial
   - Display results with Greeks

## Troubleshooting

### Model Training Issues

**Problem:** "CUDA out of memory"
- **Solution:** Reduce batch size or use fewer nodes

**Problem:** "No module named 'data_scraper'"
- **Solution:** Upload `data_scraper.py` to Colab first

**Problem:** Training loss not decreasing
- **Solution:** 
  - Check data quality
  - Adjust learning rate
  - Increase model capacity

### Ngrok Issues

**Problem:** "Ngrok connection failed"
- **Solution:** 
  - Check your auth token
  - Make sure you set it before running the server cell
  - Free tier has connection limits

**Problem:** "HTGNN endpoint unavailable"
- **Solution:**
  - Check Ngrok URL is correct in backend/.env
  - Make sure Colab notebook is still running
  - Ngrok free tier URLs change on restart

### API Issues

**Problem:** "Could not fetch price for TICKER"
- **Solution:** 
  - Check internet connection
  - yfinance may be rate-limited, wait a moment

## Model Performance Tips

1. **More Data = Better Model:**
   - Use Gauss314 if available (3.5M rows)
   - Or scrape more tickers (50-100+)

2. **Feature Engineering:**
   - Add more features in `prepare_features()`
   - Include technical indicators
   - Add market regime indicators

3. **Hyperparameter Tuning:**
   - Adjust `hidden_dim` (32, 64, 128)
   - Adjust `num_layers` (2, 3, 4)
   - Adjust learning rate (0.001, 0.0005, 0.0001)

4. **Training Strategy:**
   - Use time-based train/val split for time series
   - Add data augmentation
   - Use ensemble methods

## Production Deployment

For production, consider:

1. **Model Serving:**
   - Deploy model to cloud (AWS, GCP, Azure)
   - Use proper API gateway
   - Add authentication

2. **Monitoring:**
   - Track prediction accuracy
   - Monitor API latency
   - Set up alerts

3. **Scalability:**
   - Use model serving frameworks (TorchServe, TensorFlow Serving)
   - Add caching layer
   - Use load balancers

## Next Steps

- [ ] Train on full Gauss314 dataset
- [ ] Fine-tune hyperparameters
- [ ] Add more features
- [ ] Deploy to production
- [ ] Set up monitoring

## Support

If you encounter issues:
1. Check the error messages carefully
2. Review the notebook cells
3. Check Ngrok/Colab connectivity
4. Verify all dependencies are installed

Good luck with your training! 🚀
