"""
FastAPI Backend for HTGNN Options Pricing Engine
Serves as the API gateway between frontend and HTGNN model
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import numpy as np
from io import StringIO
import os
from dotenv import load_dotenv
import httpx

from pricing.black_scholes import BlackScholesPricer
from pricing.binomial import BinomialPricer

load_dotenv()

app = FastAPI(
    title="HTGNN Pricing Engine API",
    description="API for options pricing using HTGNN-predicted volatility",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pricers
bs_pricer = BlackScholesPricer()
binomial_pricer = BinomialPricer()

# HTGNN Model endpoint (to be connected to Colab/Ngrok)
HTGNN_ENDPOINT = os.getenv("HTGNN_ENDPOINT", "http://localhost:8001")


class OptionParams(BaseModel):
    """Single option contract parameters"""
    underlying: str = Field(..., description="Stock ticker symbol")
    strike: float = Field(..., gt=0, description="Strike price")
    expiration_days: int = Field(..., gt=0, description="Days to expiration")
    option_type: str = Field(..., pattern="^(call|put)$", description="call or put")
    current_price: Optional[float] = Field(None, gt=0, description="Current stock price (optional)")
    risk_free_rate: Optional[float] = Field(0.05, ge=0, le=1, description="Risk-free rate (default 0.05)")


class PricingRequest(BaseModel):
    """Batch pricing request"""
    options: List[OptionParams]
    style: str = Field(..., pattern="^(european|american)$", description="european or american")
    use_htgnn_volatility: bool = Field(True, description="Use HTGNN predicted volatility")


class PricingResponse(BaseModel):
    """Pricing result for a single option"""
    underlying: str
    strike: float
    expiration_days: int
    option_type: str
    current_price: float
    volatility: float
    fair_value: float
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None


class BatchPricingResponse(BaseModel):
    """Batch pricing results"""
    results: List[PricingResponse]
    total_processed: int
    errors: List[str] = []


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "HTGNN Pricing Engine API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "htgnn_endpoint": HTGNN_ENDPOINT,
        "pricers_loaded": True
    }


async def get_htgnn_volatility(underlying: str, strike: float, expiration_days: int) -> float:
    """
    Fetch predicted volatility from HTGNN model
    Falls back to historical volatility if HTGNN unavailable
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{HTGNN_ENDPOINT}/predict",
                json={
                    "underlying": underlying,
                    "strike": strike,
                    "expiration_days": expiration_days
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("volatility", 0.2)  # Default fallback
    except Exception as e:
        print(f"HTGNN endpoint unavailable: {e}")
    
    # Fallback: return a default volatility (in production, use historical)
    return 0.2


async def get_current_price(ticker: str) -> float:
    """Fetch current stock price from yfinance"""
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
    return None


@app.post("/price", response_model=PricingResponse)
async def price_single_option(request: OptionParams, style: str = "european", use_htgnn: bool = True):
    """
    Price a single option contract
    """
    # Get current price if not provided
    current_price = request.current_price
    if current_price is None:
        current_price = await get_current_price(request.underlying)
        if current_price is None:
            raise HTTPException(status_code=400, detail=f"Could not fetch price for {request.underlying}")
    
    # Get volatility
    if use_htgnn:
        volatility = await get_htgnn_volatility(
            request.underlying,
            request.strike,
            request.expiration_days
        )
    else:
        volatility = 0.2  # Default
    
    # Price the option
    if style.lower() == "european":
        result = bs_pricer.price(
            S=current_price,
            K=request.strike,
            T=request.expiration_days / 365.0,
            r=request.risk_free_rate,
            sigma=volatility,
            option_type=request.option_type
        )
    else:  # american
        result = binomial_pricer.price(
            S=current_price,
            K=request.strike,
            T=request.expiration_days / 365.0,
            r=request.risk_free_rate,
            sigma=volatility,
            option_type=request.option_type
        )
    
    return PricingResponse(
        underlying=request.underlying,
        strike=request.strike,
        expiration_days=request.expiration_days,
        option_type=request.option_type,
        current_price=current_price,
        volatility=volatility,
        fair_value=result["price"],
        delta=result.get("delta"),
        gamma=result.get("gamma"),
        theta=result.get("theta"),
        vega=result.get("vega")
    )


@app.post("/price/batch", response_model=BatchPricingResponse)
async def price_batch_options(request: PricingRequest):
    """
    Price multiple options from a batch request
    """
    results = []
    errors = []
    
    for option in request.options:
        try:
            result = await price_single_option(
                option,
                style=request.style,
                use_htgnn=request.use_htgnn_volatility
            )
            results.append(result)
        except Exception as e:
            errors.append(f"{option.underlying} {option.option_type}: {str(e)}")
    
    return BatchPricingResponse(
        results=results,
        total_processed=len(results),
        errors=errors
    )


@app.post("/price/csv", response_model=BatchPricingResponse)
async def price_from_csv(
    file: UploadFile = File(...),
    style: str = "european",
    use_htgnn: bool = True
):
    """
    Price options from uploaded CSV file
    Expected columns: underlying, strike, expiration_days, option_type, [current_price], [risk_free_rate]
    """
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        required_cols = ['underlying', 'strike', 'expiration_days', 'option_type']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_cols)}"
            )
        
        # Convert to OptionParams list
        options = []
        for _, row in df.iterrows():
            options.append(OptionParams(
                underlying=str(row['underlying']),
                strike=float(row['strike']),
                expiration_days=int(row['expiration_days']),
                option_type=str(row['option_type']).lower(),
                current_price=float(row['current_price']) if 'current_price' in df.columns and pd.notna(row.get('current_price')) else None,
                risk_free_rate=float(row['risk_free_rate']) if 'risk_free_rate' in df.columns and pd.notna(row.get('risk_free_rate')) else 0.05
            ))
        
        # Price all options
        pricing_request = PricingRequest(
            options=options,
            style=style,
            use_htgnn_volatility=use_htgnn
        )
        
        return await price_batch_options(pricing_request)
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


@app.get("/volatility/{ticker}")
async def get_volatility(ticker: str, strike: float, expiration_days: int):
    """
    Get predicted volatility for a ticker
    """
    volatility = await get_htgnn_volatility(ticker, strike, expiration_days)
    return {
        "underlying": ticker,
        "strike": strike,
        "expiration_days": expiration_days,
        "volatility": volatility
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
