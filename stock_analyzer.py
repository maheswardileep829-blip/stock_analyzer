import yfinance as yf
import pandas as pd

print ("=" * 60)
print ("Stock Analyzer")
print ("=" * 60)

stocks = input("Enter stock tickers (Separated by spaces): ").upper().split()
results = []
for ticker in stocks:
    print(f"\n{'='*60}")
    print(f"ANALYZING: {ticker}")
    print('='*60)

    stock = yf.download(tickers=ticker, period="1y", progress=False)
    
    latest_price = stock['Close'].iloc[-1].values[0]
    highest_price = stock['High'].max().values[0]
    lowest_price = stock['Low'].min().values[0]

    print(f"Highest price: ${highest_price:.2f} ")
    print(f"Lowest price: ${lowest_price:.2f}")
    print(f"Latest price: ${latest_price:.2f}")

    start_price = stock['Close'].iloc[0].values[0]
    return_rate =  (( latest_price - start_price ) / start_price)  * 100
    daily_returns = stock['Close'].pct_change()
    volatility = daily_returns.std().values[0] * 100
    ma_50 = stock['Close'].rolling(window=50).mean().iloc[-1].values[0]
    ma_200 = stock['Close'].rolling(window=200).mean().iloc[-1].values[0]

    if pd.notna(ma_50) and pd.notna(ma_200):
        if latest_price > ma_50 and ma_50 > ma_200:
            trend = "🟢 BULLISH (Strong uptrend)"
        elif latest_price > ma_50:
            trend = "🟡 NEUTRAL (Mixed signals)"
        else:
            trend = "🔴 BEARISH (Downtrend)"
    else:
        trend = "⚪ INSUFFICIENT DATA (need 200 days)"
    print (f"Start price: ${start_price:.2f}")
    print(f"Return rate: {return_rate:.2f}%")
    print(f"Volatility: {volatility:.4f}%")
    price_range = highest_price - lowest_price
    print (f"Price Range: ${price_range:.2f}")
    if pd.notna(ma_50):
        print(f"50-Day MA: ${ma_50:.2f}")
    if pd.notna(ma_200):
        print(f"200-Day MA: ${ma_200:.2f}")
    print(f"Trend: {trend}")

    results.append({
    'Ticker': ticker,
    'Latest Price': latest_price,
    '1Y Return %': return_rate,
    'Volatility %': volatility,
    'Price Range': price_range,
    'Trend': trend  
    })


print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)

print("\n" + "=" * 60)
print("COMPARISON TABLE")
print("=" * 60)

df = pd.DataFrame(results)

print("\n" + df.to_string(index=False))

best_stock = df.loc[df['1Y Return %'].idxmax()]
worst_stock = df.loc[df['1Y Return %'].idxmin()]

print("\n" + "=" * 60)
print(f"🏆 BEST PERFORMER: {best_stock['Ticker']} ({best_stock['1Y Return %']:+.2f}%)")
print(f"📉 WORST PERFORMER: {worst_stock['Ticker']} ({worst_stock['1Y Return %']:+.2f}%)")
print("=" * 60)

filename = 'stock_analysis_results.csv'
df.to_csv(filename, index=False)
print(f"\n💾 Results saved to: {filename}")