import streamlit as st
import pandas as pd
import requests
import boto3
from datetime import datetime, timedelta

@st.cache_data
def fetch_s3_data(bucket, key):
    s3 = boto3.client('s3', region_name='eu-west-2')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        st.error(f"Error fetching data from S3: {e}")
        return "{}"

@st.cache_data
def fetch_fmp_data(symbol, start_date, end_date, api_key):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start_date}&to={end_date}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'historical' not in data or not data['historical']:
            st.warning(f"No historical data for {symbol}. Check symbol or API limits.")
            return pd.DataFrame()
        df = pd.DataFrame(data['historical'])
        df['date'] = pd.to_datetime(df['date'])
        return df.set_index('date')
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching FMP data for {symbol}: {e}")
        return pd.DataFrame()

@st.cache_data
def fetch_polygon_data(symbol, api_key, multiplier=1, timespan='day', from_date=None, to_date=None):
    if from_date is None:
        from_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    if to_date is None:
        to_date = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}?apiKey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'results' not in data or not data['results']:
            st.warning(f"No data for {symbol} from Polygon.")
            return pd.DataFrame()
        df = pd.DataFrame(data['results'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.rename(columns={'c': 'close', 'h': 'high', 'l': 'low', 'o': 'open', 'v': 'volume'})
        return df.set_index('timestamp')
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Polygon data for {symbol}: {e}")
        return pd.DataFrame()

@st.cache_data
def trigger_lambda_alert(message):
    lambda_client = boto3.client('lambda', region_name='eu-west-2')
    try:
        lambda_client.invoke(
            FunctionName='breadth_lambda',
            InvocationType='RequestResponse',
            Payload=message.encode()
        )
        return True
    except Exception as e:
        st.error(f"Error triggering alert: {e}")
        return False