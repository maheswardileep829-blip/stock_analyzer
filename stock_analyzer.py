import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def safe_download(ticker: str, period: str = "1y") -> pd.DataFrame:
    df = yf.download(tickers=ticker, period=period, progress=False)

    # Flatten columns if yfinance returns MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df is None or df.empty:
        raise ValueError("No data returned (invalid ticker or no recent trading data).")

    df = df.dropna(subset=["Close"])
    if df.empty:
        raise ValueError("Data returned but missing Close prices.")

    return df


def plot_vs_spy(ticker: str, period: str = "1y") -> None:
    stock = safe_download(ticker, period=period)
    spy = safe_download("SPY", period=period)

    stock_norm = stock["Close"] / stock["Close"].iloc[0] * 100
    spy_norm = spy["Close"] / spy["Close"].iloc[0] * 100

    plt.figure(figsize=(10, 5))
    plt.plot(stock_norm, label=ticker)
    plt.plot(spy_norm, label="S&P 500 (SPY)")
    plt.title(f"{ticker} vs S&P 500 (1-Year Performance)")
    plt.xlabel("Date")
    plt.ylabel("Normalized Price (Start = 100)")
    plt.legend()
    plt.grid(True)
    plt.show()


def analyze_ticker(ticker: str) -> dict:
    df = safe_download(ticker)

    latest_price = float(df["Close"].iloc[-1])
    start_price = float(df["Close"].iloc[0])
    highest_price = float(df["High"].max())
    lowest_price = float(df["Low"].min())

    return_rate = ((latest_price - start_price) / start_price) * 100
    daily_returns = df["Close"].pct_change()
    volatility = float(daily_returns.std() * 100)

    ma_50 = float(df["Close"].rolling(window=50).mean().iloc[-1]) if len(df) >= 50 else float("nan")
    ma_200 = float(df["Close"].rolling(window=200).mean().iloc[-1]) if len(df) >= 200 else float("nan")

    if pd.notna(ma_50) and pd.notna(ma_200):
        if latest_price > ma_50 and ma_50 > ma_200:
            trend = "BULLISH"
            trend_detail = "🟢 BULLISH (Strong uptrend)"
        elif latest_price > ma_50:
            trend = "NEUTRAL"
            trend_detail = "🟡 NEUTRAL (Mixed signals)"
        else:
            trend = "BEARISH"
            trend_detail = "🔴 BEARISH (Downtrend)"
    elif pd.notna(ma_50):
        trend = "INSUFFICIENT_DATA"
        trend_detail = "⚪ INSUFFICIENT DATA (need 200 days)"
    else:
        trend = "INSUFFICIENT_DATA"
        trend_detail = "⚪ INSUFFICIENT DATA (need 50+ days)"

    price_range = highest_price - lowest_price

    print(f"\n{'='*60}")
    print(f"ANALYZING: {ticker}")
    print("=" * 60)
    print(f"Highest price: ${highest_price:.2f}")
    print(f"Lowest price:  ${lowest_price:.2f}")
    print(f"Start price:   ${start_price:.2f}")
    print(f"Latest price:  ${latest_price:.2f}")
    print(f"1Y Return:     {return_rate:+.2f}%")
    print(f"Volatility:    {volatility:.4f}%")
    print(f"Price Range:   ${price_range:.2f}")
    if pd.notna(ma_50):
        print(f"50-Day MA:     ${ma_50:.2f}")
    if pd.notna(ma_200):
        print(f"200-Day MA:    ${ma_200:.2f}")
    print(f"Trend:         {trend_detail}")

    return {
        "Ticker": ticker,
        "Latest Price": latest_price,
        "1Y Return %": return_rate,
        "Volatility %": volatility,
        "Price Range": price_range,
        "50D MA": ma_50 if pd.notna(ma_50) else None,
        "200D MA": ma_200 if pd.notna(ma_200) else None,
        "Trend": trend,
    }


def main():
    print("=" * 60)
    print("Stock Analyzer")
    print("=" * 60)

    raw = input("Enter stock tickers (separated by spaces): ").strip()
    if not raw:
        print("No tickers entered. Exiting.")
        return

    tickers = list(dict.fromkeys(raw.upper().split()))
    results = []
    failed = []

    for ticker in tickers:
        try:
            results.append(analyze_ticker(ticker))
            plot_vs_spy(ticker)  # <-- plot vs SPY after analyzing
        except Exception as e:
            failed.append((ticker, str(e)))
            print(f"❌ Skipped {ticker}: {e}")

    if not results:
        print("\nNo valid tickers to analyze.")
        return

    df = pd.DataFrame(results)

    print("\n" + "=" * 60)
    print("COMPARISON TABLE")
    print("=" * 60)
    display_cols = ["Ticker", "Latest Price", "1Y Return %", "Volatility %", "Price Range", "Trend"]
    print(df[display_cols].to_string(index=False))

    best_stock = df.loc[df["1Y Return %"].idxmax()]
    worst_stock = df.loc[df["1Y Return %"].idxmin()]

    print("\n" + "=" * 60)
    print(f"🏆 BEST PERFORMER: {best_stock['Ticker']} ({best_stock['1Y Return %']:+.2f}%)")
    print(f"📉 WORST PERFORMER: {worst_stock['Ticker']} ({worst_stock['1Y Return %']:+.2f}%)")
    print("=" * 60)

    filename = "stock_analysis_results.csv"
    df.to_csv(filename, index=False)
    print(f"\n💾 Results saved to: {filename}")

    if failed:
        print("\n" + "=" * 60)
        print("TICKERS SKIPPED")
        print("=" * 60)
        for t, msg in failed:
            print(f"- {t}: {msg}")


if __name__ == "__main__":
    main()
