import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period='7d', interval='1d'):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

def analyze_trend(df):
    df['Change'] = df['Close'].diff()
    df['Trend'] = df['Change'].apply(lambda x: '↑' if x > 0 else '↓' if x < 0 else '-')
    avg_change = df['Change'].mean()
    return df[['Close', 'Change', 'Trend']], avg_change

def generate_report(ticker, df, avg_change):
    report = f"\nStock Weekly Trend Report for {ticker.upper()}\n"
    report += "=" * 40 + "\n"
    report += df.to_string(index=True)
    report += f"\n\nAverage Daily Change: {avg_change:.2f} USD\n"
    trend_direction = "Upward 📈" if avg_change > 0 else "Downward 📉" if avg_change < 0 else "Stable ➖"
    report += f"Overall Trend: {trend_direction}\n"
    print(report)

def plot_trend(df, ticker):
    plt.figure(figsize=(8, 4))
    plt.plot(df.index, df['Close'], marker='o', linestyle='-')
    plt.title(f'{ticker.upper()} Closing Prices - Last 7 Days')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ticker = input("Enter a stock ticker symbol (e.g., AAPL): ").strip()
    data = fetch_stock_data(ticker)
    if data.empty:
        print("No data found. Check ticker symbol.")
    else:
        trend_data, avg_change = analyze_trend(data)
        generate_report(ticker, trend_data, avg_change)
        plot_trend(data, ticker)
