# Stock Market Analyzer

A Python-based stock market analysis tool that downloads real-time data and performs technical analysis on multiple stocks.

## Features

- ✅ Multi-stock analysis (analyze up to 10 stocks at once)
- ✅ Real-time data from Yahoo Finance API
- ✅ Financial metrics: 1-year returns, volatility, price ranges
- ✅ Technical indicators: 50-day & 200-day moving averages
- ✅ Trend analysis (Bullish/Bearish/Neutral signals)
- ✅ Comparison table showing all stocks side-by-side
- ✅ Automatic best/worst performer detection
- ✅ CSV export for Excel analysis

## Installation
```bash
pip install yfinance pandas
```

## Usage
```bash
python stock_analyzer.py
```

Enter stock tickers when prompted (e.g., `AAPL TSLA MSFT NVDA`)

## Example Output
```
🏆 BEST PERFORMER: GOOGL (+74.88%)
📉 WORST PERFORMER: NFLX (-18.93%)
```

Results are automatically saved to `stock_analysis_results.csv`

## Technical Details

**Metrics Calculated:**
- Latest price vs 1-year ago price
- Volatility (standard deviation of daily returns)
- 50-day & 200-day moving averages
- Trend signals using MA crossovers

**Trend Signals:**
- 🟢 BULLISH: Price > 50-day MA > 200-day MA
- 🟡 NEUTRAL: Price > 50-day MA only
- 🔴 BEARISH: Price < 50-day MA

## What I Learned

- Working with financial APIs (yfinance)
- pandas for data manipulation
- Technical analysis calculations
- Multi-stock comparison
- CSV export functionality

## Part of AI×Economics Portfolio

**Project #10** - February 2026

Built while learning Python, pandas, and financial analysis for future economic research projects.



Add Stock Market Analyzer - Project #10

- Multi-stock analysis tool with real-time data
- Technical indicators (50-day & 200-day MA)
- Trend analysis (bullish/bearish signals)
- Comparison table and CSV export
- Built with yfinance and pandas
