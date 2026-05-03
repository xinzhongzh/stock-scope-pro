import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

def fetch_stock_data(ticker_symbol, period='5y', start_date=None, end_date=None):
    """Fetch stock data for any ticker"""
    from datetime import datetime as dt_mod
    ticker = yf.Ticker(ticker_symbol)
    if start_date is not None and end_date is not None:
        hist = ticker.history(start=start_date, end=end_date)
    elif start_date is not None:
        hist = ticker.history(start=start_date, end=dt_mod.now())
    elif end_date is not None:
        hist = ticker.history(end=end_date)
    else:
        hist = ticker.history(period=period)
    return hist

def calculate_indicators(data):
    """Calculate technical indicators"""
    # Moving Averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal']
    
    # Bollinger Bands
    data['BB_Middle'] = data['Close'].rolling(window=20).mean()
    data['BB_Std'] = data['Close'].rolling(window=20).std()
    data['BB_Upper'] = data['BB_Middle'] + (data['BB_Std'] * 2)
    data['BB_Lower'] = data['BB_Middle'] - (data['BB_Std'] * 2)
    
    return data

def analyze_signals(data):
    """Analyze technical signals"""
    current = data.iloc[-1]
    
    signals = {
        'price': current['Close'],
        'rsi': current['RSI'],
        'macd': current['MACD'],
        'signal_line': current['Signal'],
        'price_vs_ma20': current['Close'] - current['MA20'],
        'price_vs_ma50': current['Close'] - current['MA50'],
        'price_vs_ma200': current['Close'] - current['MA200'],
        'ma20_vs_ma50': current['MA20'] - current['MA50'],
        'ma50_vs_ma200': current['MA50'] - current['MA200'],
        'bb_upper': current['BB_Upper'],
        'bb_lower': current['BB_Lower'],
        'bb_middle': current['BB_Middle'],
    }
    
    return signals

def generate_recommendation(signals):
    """Generate buy/sell recommendation"""
    buy_signals = 0
    sell_signals = 0
    
    if signals['rsi'] < 30:
        buy_signals += 2
    elif signals['rsi'] < 40:
        buy_signals += 1
    elif signals['rsi'] > 70:
        sell_signals += 2
    elif signals['rsi'] > 60:
        sell_signals += 1
    
    if signals['price_vs_ma20'] > 0 and signals['price_vs_ma50'] > 0 and signals['price_vs_ma200'] > 0:
        buy_signals += 1
    elif signals['price_vs_ma20'] < 0 and signals['price_vs_ma50'] < 0 and signals['price_vs_ma200'] < 0:
        sell_signals += 1
    
    if signals['ma20_vs_ma50'] > 0 and signals['ma50_vs_ma200'] > 0:
        buy_signals += 1
    elif signals['ma20_vs_ma50'] < 0 and signals['ma50_vs_ma200'] < 0:
        sell_signals += 1
    
    if signals['macd'] > signals['signal_line']:
        buy_signals += 1
    else:
        sell_signals += 1
    
    net_score = buy_signals - sell_signals
    
    if net_score >= 2:
        recommendation = "STRONG BUY"
        color = "#00CC00"
    elif net_score > 0:
        recommendation = "BUY"
        color = "#66FF66"
    elif net_score <= -2:
        recommendation = "STRONG SELL"
        color = "#FF0000"
    elif net_score < 0:
        recommendation = "SELL"
        color = "#FF6666"
    else:
        recommendation = "NEUTRAL / HOLD"
        color = "#FFD700"
    
    return buy_signals, sell_signals, recommendation, color

def create_dashboard(data, signals, recommendation, color, ticker_symbol):
    """Create interactive dashboard with subplots"""
    
    # Use all fetched data for the visualization
    recent_data = data
    # Limit to at most 5 years (1258 trading days) for chart readability
    if len(recent_data) > 1258:
        recent_data = recent_data.tail(1258)
    
    # Create subplots
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(f'{ticker_symbol} Stock Price & Moving Averages', 'RSI (14)', 'MACD', 'Volume'),
        row_heights=[0.4, 0.2, 0.2, 0.2],
        specs=[[{"secondary_y": False}],
               [{"secondary_y": False}],
               [{"secondary_y": False}],
               [{"secondary_y": False}]]
    )
    
    # Row 1: Price and Moving Averages
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['Close'], 
                   name='Close Price', line=dict(color='#1f77b4', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['BB_Upper'],
                   name='Bollinger Upper', line=dict(color='rgba(200,200,200,0.5)', dash='dot'),
                   showlegend=True),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['BB_Lower'],
                   name='Bollinger Lower', line=dict(color='rgba(200,200,200,0.5)', dash='dot'),
                   fill='tonexty', fillcolor='rgba(200,200,200,0.1)',
                   showlegend=True),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['MA20'],
                   name='MA20', line=dict(color='#ff7f0e', width=1.5)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['MA50'],
                   name='MA50', line=dict(color='#2ca02c', width=1.5)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['MA200'],
                   name='MA200', line=dict(color='#d62728', width=1.5)),
        row=1, col=1
    )
    
    # Row 2: RSI
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['RSI'],
                   name='RSI', line=dict(color='#9467bd', width=2)),
        row=2, col=1
    )
    
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold", row=2, col=1)
    
    # Row 3: MACD
    colors = ['green' if x > 0 else 'red' for x in recent_data['MACD_Histogram']]
    fig.add_trace(
        go.Bar(x=recent_data.index, y=recent_data['MACD_Histogram'],
               name='MACD Histogram', marker=dict(color=colors), showlegend=True),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['MACD'],
                   name='MACD', line=dict(color='#1f77b4', width=2)),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=recent_data.index, y=recent_data['Signal'],
                   name='Signal Line', line=dict(color='#ff7f0e', width=2)),
        row=3, col=1
    )
    
    # Row 4: Volume
    colors_vol = ['green' if data['Close'].iloc[i] > data['Close'].iloc[i-1] else 'red' 
                  for i in range(1, len(recent_data))]
    colors_vol.insert(0, 'gray')
    
    fig.add_trace(
        go.Bar(x=recent_data.index, y=recent_data['Volume'],
               name='Volume', marker=dict(color=colors_vol)),
        row=4, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"{ticker_symbol} Stock Technical Analysis Dashboard<br><sub>Recommendation: <span style='color:{color}; font-weight:bold'>{recommendation}</span></sub>",
        height=1200,
        hovermode='x unified',
        template='plotly_white',
        font=dict(size=11)
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Date", row=4, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    fig.update_yaxes(title_text="Volume", row=4, col=1)
    
    return fig

def create_summary_html(signals, buy_signals, sell_signals, recommendation, color):
    """Create summary metrics HTML"""
    current_price = signals['price']
    rsi = signals['rsi']
    
    # Color coding for metrics
    if rsi > 70:
        rsi_status = "Overbought ⚠️"
    elif rsi < 30:
        rsi_status = "Oversold ✅"
    else:
        rsi_status = "Neutral"
    
    macd_trend = "Bullish 📈" if signals['macd'] > signals['signal_line'] else "Bearish 📉"
    
    summary_html = f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h2 style="color: #333; text-align: center;">📊 TECHNICAL ANALYSIS SUMMARY</h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
            <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0;">💰 Price Metrics</h3>
                <p><strong>Current Price:</strong> ${current_price:.2f}</p>
                <p><strong>Distance from MA20:</strong> ${signals['price_vs_ma20']:.2f}</p>
                <p><strong>Distance from MA50:</strong> ${signals['price_vs_ma50']:.2f}</p>
                <p><strong>Distance from MA200:</strong> ${signals['price_vs_ma200']:.2f}</p>
            </div>
            
            <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0;">📈 Indicators</h3>
                <p><strong>RSI (14):</strong> {rsi:.2f} - {rsi_status}</p>
                <p><strong>MACD:</strong> {signals['macd']:.4f}</p>
                <p><strong>Signal Line:</strong> {signals['signal_line']:.4f}</p>
                <p><strong>Trend:</strong> {macd_trend}</p>
            </div>
        </div>
        
        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0;">
            <h3 style="margin-top: 0;">🎯 Signal Analysis</h3>
            <p>🟢 <strong>Buy Signals:</strong> {buy_signals}</p>
            <p>🔴 <strong>Sell Signals:</strong> {sell_signals}</p>
            <p><strong>Net Score:</strong> {buy_signals - sell_signals}</p>
        </div>
        
        <div style="background: {color}20; padding: 20px; border-radius: 8px; border-left: 5px solid {color}; margin: 20px 0;">
            <h2 style="color: {color}; margin-top: 0; text-align: center;">📌 VERDICT: {recommendation}</h2>
            <p style="font-size: 14px; line-height: 1.6;">
                {"The stock shows multiple bullish indicators with price above all major moving averages and strong technical momentum." if "BUY" in recommendation else "The stock shows mixed signals with consolidation patterns. Wait for clearer direction before committing capital." if "NEUTRAL" in recommendation else "The stock shows multiple bearish indicators with price below key moving averages and weakening momentum."}
            </p>
        </div>
    </div>
    """
    
    return summary_html

def run_analysis(ticker_symbol, output_dir='.', start_date=None, end_date=None):
    """Run analysis and return output file paths (for use as importable module)"""
    import os
    from datetime import datetime
    
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
    
    print(f"📊 Fetching {ticker_symbol} data...")
    data = fetch_stock_data(ticker_symbol, start_date=start_date, end_date=end_date)
    
    print("📈 Calculating technical indicators...")
    data = calculate_indicators(data)
    
    print("🔍 Analyzing signals...")
    signals = analyze_signals(data)
    buy_signals, sell_signals, recommendation, color = generate_recommendation(signals)
    
    print("🎨 Creating dashboard...")
    fig = create_dashboard(data, signals, recommendation, color, ticker_symbol)
    
    # Define output filenames
    dashboard_file = os.path.join(output_dir, f'{ticker_symbol.lower()}_technical_analysis_dashboard.html')
    chart_data_file = os.path.join(output_dir, f'{ticker_symbol.lower()}_stock_chart_data.html')
    
    # Save the dashboard chart as standalone
    fig.write_html(os.path.join(output_dir, f'{ticker_symbol.lower()}_technical_analysis.html'))
    
    # Create summary
    summary = create_summary_html(signals, buy_signals, sell_signals, recommendation, color)
    
    # Create full HTML page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{ticker_symbol} Stock Technical Analysis</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }}
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .content {{
                padding: 40px;
            }}
            .chart-container {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
                border-top: 1px solid #e0e0e0;
            }}
            .metric-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 {ticker_symbol} Stock Technical Analysis</h1>
                <p>Interactive Dashboard with Multiple Technical Indicators</p>
                <p>Data as of: {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="content">
                {summary}
                
                <div class="chart-container">
                    <h2 style="margin-bottom: 20px;">📈 Technical Indicators Chart</h2>
                    <iframe src="{chart_data_file.split('/')[-1]}" width="100%" height="1250" frameborder="0" style="border-radius: 8px;"></iframe>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>⚠️ Disclaimer:</strong> This analysis is for educational purposes only and should not be considered financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(dashboard_file, 'w') as f:
        f.write(html_content)
    
    # Save chart data separately
    with open(chart_data_file, 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn'))
    
    return {
        'dashboard_file': dashboard_file,
        'chart_data_file': chart_data_file,
        'recommendation': recommendation,
        'color': color,
        'signals': signals,
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }


def main():
    # Get ticker from user or use default
    ticker_symbol = input("Enter stock ticker (e.g., JPM, AAPL, MSFT): ").strip().upper() or "JPM"
    
    print(f"📊 Fetching {ticker_symbol} data...")
    data = fetch_stock_data(ticker_symbol, period='5y')
    
    print("📈 Calculating technical indicators...")
    data = calculate_indicators(data)
    
    print("🔍 Analyzing signals...")
    signals = analyze_signals(data)
    buy_signals, sell_signals, recommendation, color = generate_recommendation(signals)
    
    print("🎨 Creating dashboard...")
    fig = create_dashboard(data, signals, recommendation, color, ticker_symbol)
    
    # Define output filenames
    chart_file = f'{ticker_symbol.lower()}_technical_analysis.html'
    dashboard_file = f'{ticker_symbol.lower()}_technical_analysis_dashboard.html'
    chart_data_file = f'{ticker_symbol.lower()}_stock_chart_data.html'
    
    # Save the chart
    fig.write_html(chart_file)
    
    # Create summary
    summary = create_summary_html(signals, buy_signals, sell_signals, recommendation, color)
    
    # Create full HTML page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{ticker_symbol} Stock Technical Analysis</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }}
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            .content {{
                padding: 40px;
            }}
            .chart-container {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
                border-top: 1px solid #e0e0e0;
            }}
            .metric-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 {ticker_symbol} Stock Technical Analysis</h1>
                <p>Interactive Dashboard with Multiple Technical Indicators</p>
                <p>Data as of: {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="content">
                {summary}
                
                <div class="chart-container">
                    <h2 style="margin-bottom: 20px;">📈 Technical Indicators Chart</h2>
                    <iframe src="{chart_data_file}" width="100%" height="1250" frameborder="0" style="border-radius: 8px;"></iframe>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>⚠️ Disclaimer:</strong> This analysis is for educational purposes only and should not be considered financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(dashboard_file, 'w') as f:
        f.write(html_content)
    
    # Save chart data separately
    with open(chart_data_file, 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn'))
    
    print("\n✅ Analysis Complete!")
    print("📁 Files created:")
    print(f"   1. {dashboard_file} - Main dashboard")
    print(f"   2. {chart_data_file} - Chart data")
    print(f"\n🌐 Open '{dashboard_file}' in your browser to view the interactive dashboard!")

if __name__ == "__main__":
    main()
