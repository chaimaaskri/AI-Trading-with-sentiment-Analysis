import requests
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from rich.console import Console
from rich.table import Table
from transformers import BertTokenizer, BertForSequenceClassification
import torch

console = Console()

# Load pre-trained FinBERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = BertForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

# Function to fetch financial news using NewsAPI
def fetch_news(company):
    api_key = "4df25fcb4chai99maa8c431c861be2dfbebf1434"
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            try:
                data = response.json()  # Parse the response to JSON
                if "articles" in data:
                    return data["articles"][:5]  # Get the top 5 news articles
                else:
                    console.print("No articles found for this company.")
                    return []
            except ValueError:
                console.print("Error: Response is not valid JSON")
                return []
        else:
            console.print(f"Error fetching news: {response.status_code}")
            return []
    except Exception as e:
        console.print(f"[bold red]Error fetching news: {e}[/bold red]")
        return []

# Advanced sentiment analysis using FinBERT
def get_advanced_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment = torch.argmax(probabilities, dim=-1).item()

    if sentiment == 0:
        return "Negative", probabilities[0][0].item()
    elif sentiment == 1:
        return "Neutral", probabilities[0][1].item()
    else:
        return "Positive", probabilities[0][2].item()

# Function to fetch historical stock data using yfinance
def get_historical_data(symbol, period='1y', interval='1d'):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period, interval=interval)
    hist['Date'] = hist.index
    return hist

# Function to calculate moving averages
def add_moving_averages(dataframe):
    dataframe['SMA_50'] = dataframe['Close'].rolling(window=50).mean()
    dataframe['SMA_200'] = dataframe['Close'].rolling(window=200).mean()
    return dataframe

# Fancy output using Rich
def display_fancy_table(dataframe):
    console.print("\n[bold yellow]### Historical Stock Data ###\n")
    table = Table(show_header=True, header_style="bold magenta")

    # Add columns
    table.add_column("Date", style="dim", width=12)
    table.add_column("Open", justify="right")
    table.add_column("High", justify="right")
    table.add_column("Low", justify="right")
    table.add_column("Close", justify="right")
    table.add_column("SMA_50", justify="right")
    table.add_column("SMA_200", justify="right")
    table.add_column("Volume", justify="right")

    # Add rows from DataFrame
    for _, row in dataframe.head(10).iterrows():
        table.add_row(str(row['Date'].date()), f"{row['Open']:.2f}", f"{row['High']:.2f}",
                      f"{row['Low']:.2f}", f"{row['Close']:.2f}", 
                      f"{row['SMA_50']:.2f}" if pd.notnull(row['SMA_50']) else "-", 
                      f"{row['SMA_200']:.2f}" if pd.notnull(row['SMA_200']) else "-", 
                      f"{row['Volume']:.2f}")
    
    console.print(table)

# Function to plot the closing price using Plotly with moving averages
def plot_closing_price_with_ma(dataframe, symbol):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', name='Close Price',
                             line=dict(color='royalblue', width=2)))
    
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines', name='SMA 50',
                             line=dict(color='orange', width=2, dash='dot')))
    
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_200'],
                             mode='lines', name='SMA 200',
                             line=dict(color='green', width=2, dash='dot')))

    fig.update_layout(title=f"{symbol} Closing Price with Moving Averages",
                      xaxis_title='Date', yaxis_title='Price',
                      plot_bgcolor='rgba(0,0,0,0)',
                      yaxis=dict(gridcolor='lightgrey'))

    fig.show()

# Function for backtesting strategy with Moving Averages
def backtest_strategy(symbol, start_date, end_date):
    console.print(f"\n[bold green]Backtesting for {symbol} from {start_date} to {end_date}[/bold green]\n")
    historical_data = get_historical_data(symbol, period='1y')
    historical_data = add_moving_averages(historical_data)
    display_fancy_table(historical_data)
    
    # Visualize closing price with moving averages
    plot_closing_price_with_ma(historical_data, symbol)

    for index, row in historical_data.iterrows():
        last_price = row['Close']
        cash = 10000  # Example starting cash
        console.print(f"Date: [blue]{row['Date'].strftime('%Y-%m-%d')}[/blue], Closing Price: [cyan]${last_price:.2f}[/cyan]")
        decision = trade_decision(symbol, cash, last_price, row['SMA_50'], row['SMA_200'])
        console.print(f"[bold yellow]Trade Decision:[/bold yellow] {decision}\n")

# Trade decision based on sentiment and moving averages
def trade_decision(symbol, cash, last_price, sma_50, sma_200):
    news_articles = fetch_news(symbol)
    
    if not news_articles:
        return f"HOLD {symbol} at ${last_price:.2f} (No news available)"
    
    # Analyze sentiment of the top news article
    top_news_title = news_articles[0]['title']
    sentiment, confidence = get_advanced_sentiment(top_news_title)

    # Basic trading strategy with Moving Averages and sentiment
    if sentiment == "Positive" and confidence > 0.9 and sma_50 > sma_200:
        return f"BUY {symbol} at ${last_price:.2f} (Positive Sentiment + SMA Crossover)"
    elif sentiment == "Negative" and confidence > 0.9 and sma_50 < sma_200:
        return f"SELL {symbol} at ${last_price:.2f} (Negative Sentiment + SMA Crossover)"
    else:
        return f"HOLD {symbol} at ${last_price:.2f} (Neutral Sentiment or No SMA Crossover)"
    

def analyze_news_sentiment(symbol):
    news_articles = fetch_news(symbol)
    results = []
    
    for article in news_articles:
        title = article['title']
        sentiment, confidence = get_advanced_sentiment(title)
        results.append({
            'title': title,
            'sentiment': sentiment,
            'confidence': confidence
        })
        
    return results

def generate_trade_recommendations(symbol, start_date, end_date):
    historical_data = get_historical_data(symbol, period='1y')
    historical_data = add_moving_averages(historical_data)
    
    recommendations = []
    
    for index, row in historical_data.iterrows():
        last_price = row['Close']
        cash = 10000  # Example starting cash
        decision = trade_decision(symbol, cash, last_price, row['SMA_50'], row['SMA_200'])
        recommendations.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'price': last_price,
            'decision': decision
        })
    
    return recommendations


# Example usage
symbol = 'AAPL'
start_date = '2023-01-01'
end_date = '2023-12-31'

backtest_strategy(symbol, start_date, end_date)
