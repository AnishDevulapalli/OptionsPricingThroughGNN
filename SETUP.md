# Setup Guide

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Google Colab Setup

1. Open `colab/HTGNN_Model_Training.ipynb` in Google Colab
2. Run the cells to install dependencies
3. Load your training data (Gauss314 dataset or use data_scraper.py)
4. Train the HTGNN model
5. Set up FastAPI server with Ngrok:
   ```python
   from pyngrok import ngrok
   public_url = ngrok.connect(8001)
   print(f"HTGNN endpoint: {public_url}")
   ```
6. Update `HTGNN_ENDPOINT` in `backend/.env` with the Ngrok URL

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
HTGNN_ENDPOINT=http://your-ngrok-url.ngrok.io
```

## Testing

### Test Backend API

```bash
curl http://localhost:8000/health
```

### Test Single Option Pricing

```bash
curl -X POST "http://localhost:8000/price?style=european&use_htgnn=true" \
  -H "Content-Type: application/json" \
  -d '{
    "underlying": "AAPL",
    "strike": 150,
    "expiration_days": 30,
    "option_type": "call"
  }'
```

## CSV Format

For batch pricing, use CSV files with the following columns:

```csv
underlying,strike,expiration_days,option_type,current_price,risk_free_rate
AAPL,150,30,call,,
TSLA,200,45,put,,
MSFT,350,60,call,,
```

Required columns: `underlying`, `strike`, `expiration_days`, `option_type`
Optional columns: `current_price`, `risk_free_rate`
