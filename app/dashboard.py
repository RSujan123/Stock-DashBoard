# ✅ app/dashboard.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import fetch_stock_data, get_company_info
from utils.indicators import calculate_sma, calculate_rsi, calculate_macd
from utils.forecast import make_forecast

st.set_page_config(page_title="📈 AI Stock Dashboard", layout="wide")

# Custom CSS styles for fonts and themes
st.markdown("""
    <style>
        .big-font {
            font-size: 32px !important;
            font-weight: bold;
            color: #FFD700;
        }
        .sub-font {
            font-size: 16px !important;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-font'>📈 AI-Powered Stock Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-font'>Built with Streamlit, Plotly, and Prophet</div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA)", "AAPL")
with col2:
    range_option = st.selectbox("Select Time Range", ["1mo", "3mo", "6mo", "1y"], index=2)

# 🏢 Company Info Panel
company = get_company_info(ticker)

st.markdown("### 🏢 Company Info")
col_info, col_logo = st.columns([5, 1])
with col_info:
    st.markdown(f"**Name:** {company['name']}")
    st.markdown(f"**Sector:** {company['sector']}")
    st.markdown(f"**Industry:** {company['industry']}")
    st.markdown(f"**Summary:** {company['summary'][:300]}...")

with col_logo:
    if company["logo_url"]:
        st.image(company["logo_url"], width=80)

# Sidebar settings
st.sidebar.markdown("## ⚙️ Settings")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Indicators")
show_sma = st.sidebar.checkbox("SMA (14-day)", value=True)
show_rsi = st.sidebar.checkbox("RSI", value=True)
show_macd = st.sidebar.checkbox("MACD")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 ML Forecast")
enable_forecast = st.sidebar.checkbox("Show 30-Day Forecast", value=True)

if ticker:
    data = fetch_stock_data(ticker, period=range_option)

    if show_sma:
        data = calculate_sma(data, window=14)
    if show_rsi:
        data = calculate_rsi(data, window=14)
    if show_macd:
        data = calculate_macd(data)

    tabs = st.tabs(["📈 Chart", "📉 Indicators", "🤖 Forecast"])

    with tabs[0]:
        st.subheader(f"{ticker} Historical Stock Price")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data["Date"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candlestick"
        ))
        if show_sma and "SMA_14" in data:
            fig.add_trace(go.Scatter(
                x=data["Date"],
                y=data["SMA_14"],
                line=dict(color='blue', width=1),
                name="SMA (14)"
            ))
        fig.update_layout(title=f"{ticker} Price Chart", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Trading Volume")
        st.bar_chart(data.set_index("Date")["Volume"])

    with tabs[1]:
        if show_rsi:
            st.subheader("RSI (Relative Strength Index)")
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(
                x=data["Date"],
                y=data["RSI"],
                line=dict(color='purple'),
                name="RSI"
            ))
            fig_rsi.update_layout(yaxis=dict(range=[0, 100]), xaxis_title="Date", yaxis_title="RSI")
            st.plotly_chart(fig_rsi, use_container_width=True)

        if show_macd:
            st.subheader("MACD (Moving Average Convergence Divergence)")
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=data["Date"], y=data["MACD"], name="MACD"))
            fig_macd.add_trace(go.Scatter(x=data["Date"], y=data["Signal"], name="Signal"))
            fig_macd.update_layout(xaxis_title="Date", yaxis_title="MACD")
            st.plotly_chart(fig_macd, use_container_width=True)

    with tabs[2]:
        if enable_forecast:
            st.subheader(f"{ticker} Price Forecast (Next 30 Days)")
            forecast, model = make_forecast(data)

            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="Forecast"))
            fig_forecast.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], name="Upper Bound", line=dict(dash='dot')))
            fig_forecast.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], name="Lower Bound", line=dict(dash='dot')))
            fig_forecast.update_layout(title="30-Day Forecast", xaxis_title="Date", yaxis_title="Predicted Price")
            st.plotly_chart(fig_forecast, use_container_width=True)
