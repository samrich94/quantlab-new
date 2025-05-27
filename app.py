import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_fetch import fetch_s3_data, fetch_fmp_data, fetch_polygon_data

st.title("QuantLab Dashboard - Highlights")

# Fetch data
s3_data = fetch_s3_data('quantlab-bucket', 'breadth_data.json')
api_key_fmp = "dFuiULd9WoGFngH1eB4fMn2qfjd6bxYI"  # Replace with your FMP API key
api_key_polygon = "FoBd11YK9pgozZs2p7KSO88CNpLMIhh5"  # Replace with your Polygon API key
end_date = datetime(2025, 5, 27)
start_date = end_date - timedelta(days=365)

# Fetch sample data (SPY for now)
spy_data = fetch_fmp_data("SPY", start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), api_key_fmp)

# Display overview
st.header("Overview")
st.write(f"Last Updated: {s3_data.get('timestamp', 'N/A')}")

# Indexes Highlights
st.subheader("Indexes")
if not spy_data.empty:
    latest_spy_close = spy_data['close'].iloc[-1]
    st.write(f"SPY Latest Close: {latest_spy_close}")
st.write("Explore more: [Indexes](?page=Indexes)")

# Placeholder for other sections
st.subheader("Currencies")
st.write("Coming soon.")
st.write("Explore more: [Currencies](?page=Currencies)")

st.subheader("Bonds")
st.write("Coming soon.")
st.write("Explore more: [Bonds](?page=Bonds)")

st.subheader("Volatility")
st.write("Coming soon.")
st.write("Explore more: [Volatility](?page=Volatility)")

st.subheader("Breadth")
st.write("Coming soon.")
st.write("Explore more: [Breadth](?page=Breadth)")

st.subheader("Stocks")
st.write("Coming soon.")
st.write("Explore more: [Stocks](?page=Stocks)")

st.subheader("Commodities")
st.write("Coming soon.")
st.write("Explore more: [Commodities](?page=Commodities)")

st.subheader("Correlation Matrix")
st.write("Coming soon.")
st.write("Explore more: [Correlation Matrix](?page=CorrelationMatrix)")
