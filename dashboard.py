import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Trend Analyzer", layout="centered")

st.title("📈 Stock Trend Analyzer")
st.write("Enter a stock ticker below to see its weekly trend.")

# User input
ticker = st.text_input("Stock Ticker Symbol", "AAPL").upper()

@st.cache_data
def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="7d", interval="1d")
    return df

def analyze_trend(df):
    df['Change'] = df['Close'].diff()
    df['Trend'] = df['Change'].apply(lambda x: '↑' if x > 0 else '↓' if x < 0 else '-')
    avg_change = df['Change'].mean()
    return df[['Close', 'Change', 'Trend']], avg_change

if ticker:
    df = fetch_data(ticker)

    if df.empty:
        st.error("No data found. Please check the ticker symbol.")
    else:
        trend_df, avg_change = analyze_trend(df)

        st.subheader(f"🔍 Weekly Trend for {ticker}")
        st.dataframe(trend_df)

        # Plot
        st.subheader("📊 Closing Prices")
        st.line_chart(trend_df['Close'])

        # Summary
        trend_dir = "📈 Upward" if avg_change > 0 else "📉 Downward" if avg_change < 0 else "➖ Stable"
        st.markdown(f"**Average Daily Change:** `{avg_change:.2f} USD`")
        st.markdown(f"**Overall Trend:** {trend_dir}")
