# Project Structure

## Complete File Tree

```
HTGNN-Pricing-Engine/
├── backend/                          # FastAPI Backend
│   ├── main.py                      # Main API server with endpoints
│   ├── pricing/                     # Pricing engines
│   │   ├── __init__.py
│   │   ├── black_scholes.py         # European options pricing
│   │   └── binomial.py              # American options pricing
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # React Frontend (Vite)
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── Dashboard.jsx        # Main dashboard
│   │   │   ├── CSVUpload.jsx        # CSV file upload
│   │   │   ├── ManualInput.jsx      # Manual option input
│   │   │   └── ResultsTable.jsx     # Results display
│   │   ├── services/
│   │   │   └── api.js                # API client
│   │   ├── utils/                    # Pricing calculators
│   │   │   ├── blackScholes.js      # Client-side BS calculator
│   │   │   └── binomial.js           # Client-side binomial calculator
│   │   ├── App.jsx                   # Root component
│   │   ├── main.jsx                  # Entry point
│   │   └── index.css                # Global styles
│   ├── index.html                    # HTML template
│   ├── package.json                  # Node dependencies
│   └── vite.config.js                # Vite configuration
│
├── colab/                            # Google Colab Notebooks
│   ├── HTGNN_Model_Training.ipynb      # Model training notebook
│   └── data_scraper.py               # Market data scraper
│
├── example_options.csv               # Example CSV for testing
├── README.md                         # Project documentation
├── SETUP.md                          # Setup instructions
├── LICENSE                           # MIT License
└── .gitignore                        # Git ignore rules
```

## Key Features Implemented

### Backend (FastAPI)
- ✅ RESTful API endpoints for option pricing
- ✅ Single option pricing endpoint
- ✅ Batch pricing endpoint
- ✅ CSV file upload and processing
- ✅ Black-Scholes pricing engine (European options)
- ✅ Binomial tree pricing engine (American options)
- ✅ Greeks calculation (Delta, Gamma, Theta, Vega)
- ✅ HTGNN volatility integration (with fallback)
- ✅ yfinance integration for current prices
- ✅ CORS middleware for frontend communication

### Frontend (React + Vite)
- ✅ Modern, responsive dashboard UI
- ✅ CSV file upload with drag-and-drop
- ✅ Manual option input form
- ✅ Results table with Greeks
- ✅ Real-time API integration
- ✅ Error handling and loading states
- ✅ Client-side pricing calculators (jStat)

### Colab Integration
- ✅ Notebook structure for HTGNN training
- ✅ Data scraper for market data
- ✅ FastAPI server setup for inference
- ✅ Ngrok integration guide

## API Endpoints

### GET `/`
Health check endpoint

### GET `/health`
Detailed health check with HTGNN endpoint status

### POST `/price`
Price a single option
- Query params: `style` (european/american), `use_htgnn` (bool)
- Body: OptionParams JSON

### POST `/price/batch`
Price multiple options
- Body: PricingRequest with list of options

### POST `/price/csv`
Price options from CSV file
- Query params: `style`, `use_htgnn`
- Body: multipart/form-data with CSV file

### GET `/volatility/{ticker}`
Get predicted volatility for a ticker
- Query params: `strike`, `expiration_days`

## Next Steps

1. **Train HTGNN Model**: Use the Colab notebook to train on Gauss314 dataset
2. **Deploy Model**: Set up FastAPI server in Colab with Ngrok
3. **Configure Endpoint**: Update `HTGNN_ENDPOINT` in backend `.env`
4. **Test**: Use example CSV or manual input to test pricing
5. **Deploy**: Deploy backend and frontend to production servers
