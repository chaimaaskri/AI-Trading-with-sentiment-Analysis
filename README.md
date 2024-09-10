# AI Trading with Sentiment Analysis

Welcome to the Trading Bot with Sentiment Analysis project! 🚀 This project leverages sentiment analysis from financial news and trading strategies to make informed trading decisions.

## Overview

Our trading bot analyzes live financial news and historical stock data to make trading recommendations based on sentiment analysis and technical indicators. The bot uses advanced natural language processing and financial analysis techniques to guide trading decisions.

## Features

- **Sentiment Analysis:** Analyze the sentiment of top financial news articles using FinBERT.
- **Technical Analysis:** Calculate moving averages and plot them alongside historical stock prices.
- **Trade Recommendations:** Generate trading recommendations based on sentiment and moving averages.

## Live Demo

Check out the live demo [here](#).

## Getting Started

To get started with this project, follow the instructions below:

### Prerequisites

- Python 3.10 or later
- Virtual environment manager (e.g., conda or venv)

### Setup
**Create a Virtual Environment**

```bash
conda create -n trading_bot python=3.10
conda activate trading_bot

Install Dependencies

Install the required packages using pip:

bash
Copier le code
pip install flask plotly yfinance torch transformers requests
Configuration
Update the API_KEY in the trading_bot.py file with your NewsAPI key.

Run the Application
Start the Flask application:

bash
Copier le code
python app.py
Visit http://127.0.0.1:5000/ in your web browser to see the trading bot in action.

Usage
Accessing the Dashboard

The web interface allows you to:

Enter Stock Symbol: View data for different stocks by changing the symbol in the URL query parameters.
Select Date Range: Customize the start and end dates to see data for specific periods.
Viewing Results

Plotly Graph: Visualize historical stock prices and moving averages.
Sentiment Analysis Results: See the sentiment analysis of the latest financial news.
Trade Recommendations: Get trading advice based on sentiment and technical indicators.
Development
To contribute or modify the project:

Clone the Repository

bash
Copier le code
git clone https://github.com/your-username/trading-bot.git
cd trading-bot
Make Changes

Edit the files as needed. Update the trading_bot.py and app.py files to improve functionality or add features.

Test Changes

Run tests to ensure your modifications work as expected.

Push Changes

bash
Copier le code
git add .
git commit -m "Describe your changes"
git push origin main
References
Flask: Web framework used to create the dashboard.
Plotly: Library for creating interactive charts.
yFinance: For fetching historical stock data.
Transformers: For sentiment analysis using FinBERT.
Author
👨‍💻 Chaima Askri

📅 Version 1.0

