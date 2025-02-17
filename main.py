from fastapi import FastAPI
import yfinance as yf
import openai
import os

app = FastAPI()

# Read OpenAI API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    return {"message": "Welcome to StockFocus API"}

@app.get("/stock/{ticker}")
def get_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "dividend_yield": info.get("dividendYield"),
    }

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    prompt = f"""
    Analyze {ticker} stock. Here is some key financial information:
    - Company Name: {info.get('longName')}
    - Sector: {info.get('sector')}
    - Market Cap: {info.get('marketCap')}
    - P/E Ratio: {info.get('trailingPE')}
    - Dividend Yield: {info.get('dividendYield')}

    Based on this data, what are the investment risks and potential opportunities?
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return {"analysis": response["choices"][0]["message"]["content"]}

