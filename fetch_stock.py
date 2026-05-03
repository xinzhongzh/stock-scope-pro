import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def fetch_and_analyze_stock(ticker_symbol, start_date=None, end_date=None, period='5y'):
    """Fetch and analyze stock data for any ticker"""
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1825)
    
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(start=start_date, end=end_date)
    
    # Calculate moving averages
    hist['MA20'] = hist['Close'].rolling(window=20).mean()
    hist['MA50'] = hist['Close'].rolling(window=50).mean()
    
    return hist

def plot_advanced(data, ticker_symbol):
    """Advanced plotting with moving averages using Plotly"""
    fig = go.Figure()
    
    # Add Close Price line
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        name='Close Price',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Add 20-day MA
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA20'],
        name='20-Day MA',
        line=dict(color='#ff7f0e', width=1.5, dash='dash')
    ))
    
    # Add 50-day MA
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MA50'],
        name='50-Day MA',
        line=dict(color='#2ca02c', width=1.5, dash='dash')
    ))
    
    fig.update_layout(
        title=f'{ticker_symbol} Stock Price with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        template='plotly_white',
        height=600,
        width=1200
    )
    
    # Save as HTML with ticker-prefixed filename
    output_file = f'{ticker_symbol.lower()}_stock_chart.html'
    fig.write_html(output_file)
    print(f"\n✅ Interactive chart saved as: {output_file}")
    print(f"📊 Open it in your browser to explore the data interactively!")

def run_analysis(ticker_symbol, output_dir='.', start_date=None, end_date=None):
    """Run analysis and return output file path (for use as importable module)"""
    import os
    from datetime import datetime, timedelta
    
    # Convert string dates to datetime if provided
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            start_date = None
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            end_date = None
    
    data = fetch_and_analyze_stock(ticker_symbol, start_date=start_date, end_date=end_date)
    
    # Override output file location for web app
    output_file = os.path.join(output_dir, f'{ticker_symbol.lower()}_stock_chart.html')
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Close'],
        name='Close Price', line=dict(color='#1f77b4', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=data.index, y=data['MA20'],
        name='20-Day MA', line=dict(color='#ff7f0e', width=1.5, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=data.index, y=data['MA50'],
        name='50-Day MA', line=dict(color='#2ca02c', width=1.5, dash='dash')
    ))
    
    fig.update_layout(
        title=f'{ticker_symbol} Stock Price with Moving Averages',
        xaxis_title='Date', yaxis_title='Price ($)',
        hovermode='x unified', template='plotly_white',
        height=600, width=1200
    )
    
    fig.write_html(output_file)
    return {'chart_file': output_file, 'data': data}


if __name__ == "__main__":
    ticker_input = input("Enter stock ticker (e.g., JPM, AAPL, MSFT): ").strip().upper() or "JPM"
    result = run_analysis(ticker_input)
    print(f"\n{ticker_input} Stock Data:")
    print(result['data'].tail(10))
    print(f"\n✅ Interactive chart saved as: {result['chart_file']}")
