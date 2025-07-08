# 📈 AI-Powered Stock Market Dashboard

An interactive, enterprise-grade stock dashboard that visualizes historical trends, forecasts future prices using machine learning, and provides real-time metadata — all powered by open-source tools.

---


## 🧠 Features

- 📊 **Candlestick Charts** – Interactive price visualization using Plotly
- 💹 **Technical Indicators** – Built-in SMA, RSI, MACD
- 🤖 **AI Forecasting** – 30-day prediction with Facebook Prophet
- 🏢 **Company Info Panel** – Displays sector, logo, summary using Yahoo Finance
- 🎨 **Modern UI** – Custom Streamlit theme, layout, and styling
- 🔗 **Fully Open-Source** – Easy to fork, extend, and customize

---

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Data Source**: yfinance (Yahoo Finance API)
- **Forecasting**: Facebook Prophet
- **Charting**: Plotly
- **Styling**: Custom `.streamlit/config.toml`

---

## 📂 Folder Structure

stock-dashboard/
├── app/
│   └── dashboard.py            # Main Streamlit App
├── utils/
│   ├── data_loader.py          # Stock data + metadata
│   ├── forecast.py             # Prophet ML model
│   └── indicators.py           # RSI, SMA, MACD calculations
├── requirements.txt
└── .streamlit/
    └── config.toml             # Theme and UI settings

---

## 📦 How to Run Locally

```bash
git clone https://github.com/your-username/stock-dashboard.git
cd stock-dashboard
pip install -r requirements.txt
streamlit run app/dashboard.py
