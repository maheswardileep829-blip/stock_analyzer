# Stock Market Analyzer

A Python tool that downloads recent stock data and runs basic technical + performance analysis across multiple tickers.

## Features
- Analyze up to 10 stocks at once
- Pulls data from Yahoo Finance (via `yfinance`)
- Computes:
  - 1-year return
  - Volatility (std. dev. of daily returns)
  - Price range
  - 50-day & 200-day moving averages
- Simple trend signal (Bullish / Neutral / Bearish)
- Identifies best & worst performer
- Exports results to CSV (`stock_analysis_results.csv`)

## Installation
```bash
py -3 -m pip install -r requirements.txt
