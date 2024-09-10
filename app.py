from flask import Flask, render_template, request
import plotly.graph_objects as go
from plotly.io import to_html
from trading_bot import (add_moving_averages, get_historical_data, 
                         fetch_news, get_advanced_sentiment, trade_decision,
                         analyze_news_sentiment, generate_trade_recommendations)

app = Flask(__name__)

@app.route('/')
def index():
    # Get query parameters or use default values
    symbol = request.args.get('symbol', 'AAPL')
    start_date = request.args.get('start_date', '2023-01-01')
    end_date = request.args.get('end_date', '2023-12-31')

    # Generate trade recommendations
    recommendations = generate_trade_recommendations(symbol, start_date, end_date)
    
    # Create Plotly figure
    historical_data = get_historical_data(symbol, period='1y')
    historical_data = add_moving_averages(historical_data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['Close'],
                             mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['SMA_50'],
                             mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=historical_data['Date'], y=historical_data['SMA_200'],
                             mode='lines', name='SMA 200'))
    fig.update_layout(title=f"{symbol} Closing Price with Moving Averages",
                      xaxis_title='Date', yaxis_title='Price')
    
    # Convert Plotly figure to HTML
    graph_html = to_html(fig, full_html=False)
    
    # Analyze news sentiment
    results = analyze_news_sentiment(symbol)
    
    # Render the template with Plotly graph, sentiment results, and trade recommendations
    return render_template('index.html', plot=graph_html, recommendations=recommendations, results=results)

if __name__ == '__main__':
    app.run(debug=True)



