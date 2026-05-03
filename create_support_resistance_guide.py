import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

def create_support_resistance_guide():
    """Create interactive visual guide for support and resistance"""
    
    # Create subplots for different scenarios
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Example 1: Buy at Support',
            'Example 2: Sell at Resistance',
            'Example 3: Breakout (Up)',
            'Example 4: Breakdown (Down)',
            'Example 5: Multiple Bounces - Support',
            'Example 6: Multiple Bounces - Resistance'
        ),
        specs=[[{"type": "scatter"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "scatter"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.12
    )
    
    # ===== EXAMPLE 1: Buy at Support =====
    dates1 = list(range(20))
    price1 = [310, 308, 306, 304, 305, 307, 309, 312, 310, 308, 
              306, 305, 304, 305, 307, 309, 311, 313, 312, 310]
    
    fig.add_trace(
        go.Scatter(x=dates1, y=price1, mode='lines+markers', 
                   line=dict(color='#1f77b4', width=2),
                   marker=dict(size=4),
                   name='Price'),
        row=1, col=1
    )
    
    # Support line
    fig.add_hline(y=304, line_dash="dash", line_color="green", 
                 annotation_text="Support = $304", 
                 annotation_position="left", row=1, col=1)
    
    # Buy signal at support
    fig.add_scatter(x=[11], y=[304], mode='markers+text',
                   marker=dict(size=15, color='green', symbol='triangle-up'),
                   text=['BUY HERE'], textposition='top center',
                   showlegend=False, row=1, col=1)
    
    fig.update_yaxes(range=[300, 315], row=1, col=1)
    fig.update_xaxes(title_text="Days", row=1, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    
    # ===== EXAMPLE 2: Sell at Resistance =====
    dates2 = list(range(20))
    price2 = [304, 306, 308, 310, 312, 311, 309, 307, 308, 310, 
              312, 313, 312, 310, 308, 310, 312, 313, 312, 310]
    
    fig.add_trace(
        go.Scatter(x=dates2, y=price2, mode='lines+markers',
                   line=dict(color='#1f77b4', width=2),
                   marker=dict(size=4),
                   name='Price'),
        row=1, col=2
    )
    
    # Resistance line
    fig.add_hline(y=313, line_dash="dash", line_color="red",
                 annotation_text="Resistance = $313",
                 annotation_position="left", row=1, col=2)
    
    # Sell signal at resistance
    fig.add_scatter(x=[11], y=[313], mode='markers+text',
                   marker=dict(size=15, color='red', symbol='triangle-down'),
                   text=['SELL HERE'], textposition='bottom center',
                   showlegend=False, row=1, col=2)
    
    fig.update_yaxes(range=[302, 315], row=1, col=2)
    fig.update_xaxes(title_text="Days", row=1, col=2)
    fig.update_yaxes(title_text="Price ($)", row=1, col=2)
    
    # ===== EXAMPLE 3: Breakout (Up) =====
    dates3 = list(range(20))
    price3 = [305, 307, 310, 308, 310, 312, 313, 313, 313, 313,
              314, 316, 318, 320, 322, 324, 325, 327, 328, 330]
    
    fig.add_trace(
        go.Scatter(x=dates3, y=price3, mode='lines+markers',
                   line=dict(color='#2ca02c', width=2),
                   marker=dict(size=4),
                   name='Price'),
        row=2, col=1
    )
    
    # Resistance line
    fig.add_hline(y=313, line_dash="dash", line_color="red",
                 annotation_text="Old Resistance",
                 annotation_position="left", row=2, col=1)
    
    # Breakout point
    fig.add_scatter(x=[10], y=[314], mode='markers+text',
                   marker=dict(size=15, color='green', symbol='diamond'),
                   text=['BREAKOUT!'], textposition='top center',
                   showlegend=False, row=2, col=1)
    
    # New resistance
    fig.add_hline(y=330, line_dash="dot", line_color="orange",
                 annotation_text="New Target",
                 annotation_position="right", row=2, col=1)
    
    fig.update_yaxes(range=[300, 335], row=2, col=1)
    fig.update_xaxes(title_text="Days", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=2, col=1)
    
    # ===== EXAMPLE 4: Breakdown (Down) =====
    dates4 = list(range(20))
    price4 = [320, 318, 316, 318, 316, 315, 314, 314, 314, 314,
              313, 311, 309, 307, 305, 303, 302, 300, 299, 297]
    
    fig.add_trace(
        go.Scatter(x=dates4, y=price4, mode='lines+markers',
                   line=dict(color='#d62728', width=2),
                   marker=dict(size=4),
                   name='Price'),
        row=2, col=2
    )
    
    # Support line
    fig.add_hline(y=314, line_dash="dash", line_color="green",
                 annotation_text="Old Support",
                 annotation_position="left", row=2, col=2)
    
    # Breakdown point
    fig.add_scatter(x=[10], y=[313], mode='markers+text',
                   marker=dict(size=15, color='red', symbol='diamond'),
                   text=['BREAKDOWN!'], textposition='bottom center',
                   showlegend=False, row=2, col=2)
    
    # New support
    fig.add_hline(y=297, line_dash="dot", line_color="orange",
                 annotation_text="New Target",
                 annotation_position="right", row=2, col=2)
    
    fig.update_yaxes(range=[290, 325], row=2, col=2)
    fig.update_xaxes(title_text="Days", row=2, col=2)
    fig.update_yaxes(title_text="Price ($)", row=2, col=2)
    
    # ===== EXAMPLE 5: Multiple Bounces - Support =====
    dates5 = list(range(25))
    price5 = [310, 308, 306, 305, 306, 308, 310,  # First bounce
              312, 310, 308, 307, 308, 310, 312,  # Second bounce
              314, 312, 310, 308, 307, 308, 310,  # Third bounce
              312, 314, 316, 318]
    
    fig.add_trace(
        go.Scatter(x=dates5, y=price5, mode='lines+markers',
                   line=dict(color='#1f77b4', width=2),
                   marker=dict(size=3),
                   name='Price'),
        row=3, col=1
    )
    
    # Support line with multiple touches
    fig.add_hline(y=305, line_dash="dash", line_color="green", annotation_text="Support",
                 annotation_position="left", row=3, col=1)
    
    # Mark bounces
    bounce_points = [3, 10, 17]
    for bp in bounce_points:
        fig.add_scatter(x=[bp], y=[305.5], mode='markers',
                       marker=dict(size=10, color='green', symbol='circle'),
                       showlegend=False, row=3, col=1)
    
    fig.update_yaxes(range=[300, 320], row=3, col=1)
    fig.update_xaxes(title_text="Days", row=3, col=1)
    fig.update_yaxes(title_text="Price ($)", row=3, col=1)
    
    # ===== EXAMPLE 6: Multiple Bounces - Resistance =====
    dates6 = list(range(25))
    price6 = [300, 302, 304, 306, 307, 305, 303,  # First bounce
              301, 303, 305, 306, 305, 303, 301,  # Second bounce
              302, 304, 306, 307, 306, 304, 302,  # Third bounce
              304, 306, 308, 310]
    
    fig.add_trace(
        go.Scatter(x=dates6, y=price6, mode='lines+markers',
                   line=dict(color='#1f77b4', width=2),
                   marker=dict(size=3),
                   name='Price'),
        row=3, col=2
    )
    
    # Resistance line with multiple touches
    fig.add_hline(y=307, line_dash="dash", line_color="red", annotation_text="Resistance",
                 annotation_position="left", row=3, col=2)
    
    # Mark rejections
    rejection_points = [3, 10, 17]
    for rp in rejection_points:
        fig.add_scatter(x=[rp], y=[306.5], mode='markers',
                       marker=dict(size=10, color='red', symbol='circle'),
                       showlegend=False, row=3, col=2)
    
    fig.update_yaxes(range=[298, 315], row=3, col=2)
    fig.update_xaxes(title_text="Days", row=3, col=2)
    fig.update_yaxes(title_text="Price ($)", row=3, col=2)
    
    # Update overall layout
    fig.update_layout(
        title_text="Support & Resistance Trading Examples",
        height=1200,
        showlegend=False,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def calculate_price_levels(ticker_symbol, start_date=None, end_date=None):
    """Fetch stock data and calculate support/resistance levels"""
    try:
        import yfinance as yf
        from datetime import datetime as dt_mod
        
        ticker = yf.Ticker(ticker_symbol)
        if start_date is not None and end_date is not None:
            hist = ticker.history(start=start_date, end=end_date)
        elif start_date is not None:
            hist = ticker.history(start=start_date, end=dt_mod.now())
        elif end_date is not None:
            hist = ticker.history(end=end_date)
        else:
            hist = ticker.history(period='1y')
        
        if hist.empty:
            # Fallback values if data can't be fetched
            return {
                'current_price': 100.00,
                'support': 90.00,
                'resistance': 110.00,
                'major_support_1': 80.00,
                'major_support_2': 70.00,
            }
        
        current_price = round(hist['Close'].iloc[-1], 2)
        
        # Support = recent 3-month low
        recent_3m = hist.tail(63)  # ~63 trading days = 3 months
        support = round(recent_3m['Low'].min(), 2)
        
        # Resistance = recent 3-month high
        resistance = round(recent_3m['High'].max(), 2)
        
        # Major support 1 = 1-year low
        major_support_1 = round(hist['Low'].min(), 2)
        
        # Major support 2 = 1-year low minus 10% buffer
        major_support_2 = round(major_support_1 * 0.90, 2)
        
        # Calculate 50-day MA
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        ma50 = round(hist['MA50'].iloc[-1], 2) if not np.isnan(hist['MA50'].iloc[-1]) else round(current_price * 0.95, 2)
        
        # Calculate 200-day MA
        hist['MA200'] = hist['Close'].rolling(window=200).mean()
        ma200 = round(hist['MA200'].iloc[-1], 2) if len(hist) >= 200 and not np.isnan(hist['MA200'].iloc[-1]) else round(current_price * 0.85, 2)
        
        return {
            'current_price': current_price,
            'support': support,
            'resistance': resistance,
            'major_support_1': major_support_1,
            'major_support_2': major_support_2,
            'ma50': ma50,
            'ma200': ma200,
        }
    except Exception as e:
        print(f"Could not fetch data for {ticker_symbol}: {e}")
        # Return safe fallback values
        return {
            'current_price': 100.00,
            'support': 90.00,
            'resistance': 110.00,
            'major_support_1': 80.00,
            'major_support_2': 70.00,
            'ma50': 95.00,
            'ma200': 85.00,
        }


def create_summary_page(ticker_symbol, levels):
    """Create summary page with real price data"""
    cp = levels['current_price']
    s = levels['support']
    r = levels['resistance']
    ms1 = levels['major_support_1']
    ms2 = levels['major_support_2']
    ma200 = levels.get('ma200', round(cp * 0.85, 2))
    
    # Calculate risk/reward numbers
    entry_buy = round(s * 1.005, 2)
    stop_loss_buy = round(s * 0.99, 2)
    risk_buy = round(entry_buy - stop_loss_buy, 2)
    reward_buy = round(r - entry_buy, 2)
    
    entry_sell = round(r * 0.995, 2)
    stop_loss_sell = round(r * 1.01, 2)
    risk_sell = round(stop_loss_sell - entry_sell, 2)
    reward_sell = round(entry_sell - s, 2)
    
    target_breakout_up = round(r * 1.08, 2)
    target_breakout_down = round(s * 0.92, 2)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{ticker_symbol} Support & Resistance Guide</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', sans-serif;
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
            .content {{
                padding: 40px;
            }}
            .section {{
                margin: 40px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 5px solid #667eea;
            }}
            .section h2 {{
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5em;
            }}
            .section p {{
                line-height: 1.8;
                color: #333;
                margin: 10px 0;
            }}
            .two-column {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                border-top: 3px solid #667eea;
            }}
            .card h3 {{
                color: #667eea;
                margin-bottom: 10px;
            }}
            .example-box {{
                background: #fff3cd;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #ffc107;
                margin: 15px 0;
                font-family: monospace;
                font-size: 0.95em;
                line-height: 1.6;
            }}
            .support-level {{
                color: #28a745;
                font-weight: bold;
            }}
            .resistance-level {{
                color: #dc3545;
                font-weight: bold;
            }}
            .buy-signal {{
                background: #d4edda;
                color: #155724;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .sell-signal {{
                background: #f8d7da;
                color: #721c24;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .chart-container {{
                margin: 30px 0;
                background: white;
                padding: 20px;
                border-radius: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background: #667eea;
                color: white;
            }}
            tr:nth-child(even) {{
                background: #f9f9f9;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
                border-top: 1px solid #e0e0e0;
            }}
            ul {{
                margin-left: 20px;
                line-height: 2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 {ticker_symbol} Support & Resistance Trading Guide</h1>
                <p>Visual Examples and Trading Strategies | Current Price: ${cp}</p>
            </div>
            
            <div class="content">
                <!-- SUPPORT SECTION -->
                <div class="section">
                    <h2>🟢 What is SUPPORT?</h2>
                    <p><strong>Support</strong> is a price level where the stock <strong>stops falling</strong> and bounces back up.</p>
                    <p style="color: #666; font-style: italic;">Think of it as a "FLOOR" - the stock struggles to fall below this level.</p>
                    
                    <h3 style="margin-top: 20px; color: #333;">Why Support Works:</h3>
                    <ul>
                        <li><strong>Buyer Interest:</strong> Investors see it as cheap and start buying</li>
                        <li><strong>Historical Memory:</strong> Previous buyers hold strong at this level</li>
                        <li><strong>Psychological:</strong> Round numbers act as support</li>
                    </ul>
                    
                    <div class="example-box">
 <strong>📈 {ticker_symbol} Key Support Level: ${s}</strong>
 This is the 3-month low for {ticker_symbol}. 
 Price has historically found buyers near this level.
 
 → ${s} is a KEY SUPPORT LEVEL for {ticker_symbol}
                    </div>
                    
                    <div class="buy-signal">
                        ✅ <strong>Trading Strategy:</strong> BUY when price approaches ${s} with volume
                    </div>
                </div>
                
                <!-- RESISTANCE SECTION -->
                <div class="section">
                    <h2>🔴 What is RESISTANCE?</h2>
                    <p><strong>Resistance</strong> is a price level where the stock <strong>stops rising</strong> and pulls back down.</p>
                    <p style="color: #666; font-style: italic;">Think of it as a "CEILING" - the stock struggles to break above this level.</p>
                    
                    <h3 style="margin-top: 20px; color: #333;">Why Resistance Works:</h3>
                    <ul>
                        <li><strong>Seller Interest:</strong> Investors take profits and sell</li>
                        <li><strong>Historical Memory:</strong> Previous sellers locked in gains here</li>
                        <li><strong>Psychological:</strong> Round numbers act as resistance</li>
                    </ul>
                    
                    <div class="example-box">
 <strong>📉 {ticker_symbol} Key Resistance Level: ${r}</strong>
 This is the 3-month high for {ticker_symbol}.
 Price has historically faced selling pressure near this level.
 
 → ${r} is a KEY RESISTANCE LEVEL for {ticker_symbol}
                    </div>
                    
                    <div class="sell-signal">
                        ❌ <strong>Trading Strategy:</strong> SELL when price approaches ${r} with volume
                    </div>
                </div>
                
                <!-- TRADING STRATEGIES SECTION -->
                <div class="section">
                    <h2>🎯 Trading Strategies</h2>
                    
                    <div class="two-column">
                        <div class="card">
                            <h3>Strategy 1: Buy at Support</h3>
                            <p><strong>Setup:</strong></p>
                            <ul style="margin-left: 15px;">
                                <li>Support Level: ${s}</li>
                                <li>Entry: ${entry_buy} (at support)</li>
                                <li>Stop Loss: ${stop_loss_buy} (below support)</li>
                                <li>Risk: ${risk_buy}</li>
                            </ul>
                            <p style="margin-top: 10px;"><strong>Profit Target: ${r} (resistance)</strong></p>
                            <p style="margin-top: 10px; color: #28a745;"><strong>Reward: ${reward_buy}</strong></p>
                            <p style="margin-top: 10px; color: #667eea;"><strong>Risk/Reward Ratio: 1:{round(reward_buy/risk_buy, 1) if risk_buy > 0 else '?'}</strong> ✅</p>
                        </div>
                        
                        <div class="card">
                            <h3>Strategy 2: Sell at Resistance</h3>
                            <p><strong>Setup:</strong></p>
                            <ul style="margin-left: 15px;">
                                <li>Resistance Level: ${r}</li>
                                <li>Entry: ${entry_sell} (at resistance)</li>
                                <li>Stop Loss: ${stop_loss_sell} (above resistance)</li>
                                <li>Risk: ${risk_sell}</li>
                            </ul>
                            <p style="margin-top: 10px;"><strong>Profit Target: ${s} (support)</strong></p>
                            <p style="margin-top: 10px; color: #28a745;"><strong>Reward: ${reward_sell}</strong></p>
                            <p style="margin-top: 10px; color: #667eea;"><strong>Risk/Reward Ratio: 1:{round(reward_sell/risk_sell, 1) if risk_sell > 0 else '?'}</strong> ✅</p>
                        </div>
                    </div>
                </div>
                
                <!-- BREAKOUT SECTION -->
                <div class="section">
                    <h2>🚀 Breakout Strategy (Most Powerful!)</h2>
                    
                    <div class="two-column">
                        <div class="card">
                            <h3>🟢 Bullish Breakout (Break UP)</h3>
                            <p><strong>Signal:</strong> Price closes ABOVE ${r} on high volume</p>
                            <p style="margin-top: 10px; color: #28a745;"><strong>Action: STRONG BUY</strong></p>
                            <p style="margin-top: 10px; font-size: 0.9em; color: #666;">Price likely to go much higher<br>Previous resistance becomes new support</p>
                            
                            <div class="example-box" style="margin-top: 15px;">
 <strong>{ticker_symbol} Scenario:</strong>
 Resistance (${r}) breaks with volume
 → BUY signal activated
 → New target: ~${target_breakout_up}
 → Stop Loss: ${s}
                            </div>
                        </div>
                        
                        <div class="card">
                            <h3>🔴 Bearish Breakdown (Break DOWN)</h3>
                            <p><strong>Signal:</strong> Price closes BELOW ${s} on high volume</p>
                            <p style="margin-top: 10px; color: #dc3545;"><strong>Action: STRONG SELL</strong></p>
                            <p style="margin-top: 10px; font-size: 0.9em; color: #666;">Price likely to go much lower<br>Previous support becomes new resistance</p>
                            
                            <div class="example-box" style="margin-top: 15px;">
 <strong>{ticker_symbol} Scenario:</strong>
 Support (${s}) breaks with volume
 → SELL signal activated
 → New target: ~${target_breakout_down}
 → Stop Loss: ${r}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- KEY RULES SECTION -->
                <div class="section">
                    <h2>✅ Do's and ❌ Don'ts</h2>
                    
                    <table>
                        <tr>
                            <th style="background: #28a745;">✅ DO's</th>
                            <th style="background: #dc3545;">❌ DON'Ts</th>
                        </tr>
                        <tr>
                            <td>Use multiple confirmations (S/R + Volume + Indicators)</td>
                            <td>Don't rely on S/R alone - use other indicators</td>
                        </tr>
                        <tr>
                            <td>Trade the bounce - best entries at S/R levels</td>
                            <td>Don't trade exactly on the line - use buffer</td>
                        </tr>
                        <tr>
                            <td>Higher timeframes matter more (daily > hourly)</td>
                            <td>Don't use too many levels - clutters chart</td>
                        </tr>
                        <tr>
                            <td>Respect strong levels (bounced many times)</td>
                            <td>Don't ignore volume - needs confirmation</td>
                        </tr>
                        <tr>
                            <td>Use wider stops beyond S/R levels</td>
                            <td>Don't trade broken levels immediately</td>
                        </tr>
                    </table>
                </div>
                
                <!-- CURRENT LEVELS -->
                <div class="section" style="border-left-color: #667eea;">
                    <h2>📍 {ticker_symbol} - Current Support & Resistance Levels (Live Data)</h2>
                    
                    <table>
                        <tr>
                            <th>Price Level</th>
                            <th>Type</th>
                            <th>Significance</th>
                            <th>Trading Action</th>
                        </tr>
                        <tr>
                            <td style="color: #dc3545;"><strong>${r}</strong></td>
                            <td style="color: #dc3545;">Resistance</td>
                            <td>3-month high, resistance zone</td>
                            <td>SELL / SHORT on touch with volume</td>
                        </tr>
                        <tr>
                            <td><strong>${cp}</strong></td>
                            <td>Current Price</td>
                            <td>Latest closing price</td>
                            <td>Wait for breakout direction</td>
                        </tr>
                        <tr>
                            <td style="color: #28a745;"><strong>${s}</strong></td>
                            <td style="color: #28a745;">Support</td>
                            <td>3-month low, key support</td>
                            <td>BUY on touch with volume</td>
                        </tr>
                        <tr>
                            <td style="color: #28a745;"><strong>${ma200}</strong></td>
                            <td style="color: #28a745;">Major Support (200-MA)</td>
                            <td>200-day moving average area</td>
                            <td>Strong support if tested</td>
                        </tr>
                        <tr>
                            <td style="color: #28a745;"><strong>${ms1}</strong></td>
                            <td style="color: #28a745;">Major Support (1Y Low)</td>
                            <td>1-year low</td>
                            <td>Last resort support level</td>
                        </tr>
                    </table>
                </div>
                
                <!-- TRADING PLAN -->
                <div class="section" style="border-left-color: #ffc107; background: #fffbea;">
                    <h2>📋 Your {ticker_symbol} Trading Plan</h2>
                    
                    <div style="margin: 15px 0;">
                        <h3 style="color: #333;">Current Situation:</h3>
                        <p>Price: ${cp} | Range: ${s} - ${r}</p>
                    </div>
                    
                    <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid #28a745;">
                        <h3 style="color: #28a745;">📈 SCENARIO 1 - Breakout Up (BUY)</h3>
                        <p><strong>Trigger:</strong> Price closes ABOVE ${r} on high volume</p>
                        <p><strong>Action:</strong> BUY at ${round(r * 1.005, 2)}</p>
                        <p><strong>Target:</strong> ${target_breakout_up} (next resistance)</p>
                        <p><strong>Stop Loss:</strong> ${s} (below breakout point)</p>
                        <p><strong>Risk/Reward:</strong> Risk ${round(r * 1.005 - s, 2)}, Gain ${round(target_breakout_up - r * 1.005, 2)}</p>
                    </div>
                    
                    <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid #dc3545;">
                        <h3 style="color: #dc3545;">📉 SCENARIO 2 - Breakdown Down (SELL)</h3>
                        <p><strong>Trigger:</strong> Price closes BELOW ${s} on high volume</p>
                        <p><strong>Action:</strong> SELL at ${round(s * 0.995, 2)}</p>
                        <p><strong>Target:</strong> ${target_breakout_down} (next support)</p>
                        <p><strong>Stop Loss:</strong> ${r} (above breakdown point)</p>
                        <p><strong>Risk/Reward:</strong> Risk ${round(r - s * 0.995, 2)}, Gain ${round(s * 0.995 - target_breakout_down, 2)}</p>
                    </div>
                    
                    <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid #ffc107;">
                        <h3 style="color: #f39c12;">⚪ SCENARIO 3 - Consolidation (HOLD)</h3>
                        <p><strong>Condition:</strong> Price stays between ${s} - ${r}</p>
                        <p><strong>Action:</strong> WAIT for clearer setup</p>
                        <p><strong>Watch:</strong> Volume, RSI, MACD signals</p>
                        <p><strong>Next Entry:</strong> When one scenario triggers</p>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2 style="margin-bottom: 20px;">📊 Interactive Support & Resistance Charts</h2>
                    <iframe src="support_resistance_charts.html" width="100%" height="1250" frameborder="0" style="border-radius: 8px;"></iframe>
                </div>
                
            </div>
            
            <div class="footer">
                <p><strong>⚠️ Disclaimer:</strong> This guide is for educational purposes only. Not financial advice. Always consult a qualified advisor. Past performance doesn't guarantee future results.</p>
                <p style="margin-top: 8px;">Data source: Yahoo Finance | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


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
    
    print("📊 Creating Support & Resistance charts...")
    fig = create_support_resistance_guide()
    
    chart_file = os.path.join(output_dir, f'{ticker_symbol.lower()}_support_resistance_charts.html')
    guide_file = os.path.join(output_dir, f'{ticker_symbol.lower()}_support_resistance_guide.html')
    
    print("💾 Saving charts...")
    with open(chart_file, 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn'))
    
    print("📄 Creating guide page...")
    # Calculate real price levels from stock data
    levels = calculate_price_levels(ticker_symbol, start_date=start_date, end_date=end_date)
    html_content = create_summary_page(ticker_symbol, levels)
    
    # Fix the iframe src to point to the ticker-specific chart file
    html_content = html_content.replace(
        'iframe src="support_resistance_charts.html"',
        f'iframe src="{chart_file.split("/")[-1]}"'
    )
    
    with open(guide_file, 'w') as f:
        f.write(html_content)
    
    return {
        'guide_file': guide_file,
        'chart_file': chart_file
    }


def main():
    ticker_symbol = input("Enter stock ticker (e.g., JPM, AAPL, MSFT): ").strip().upper() or "JPM"
    result = run_analysis(ticker_symbol)
    
    print("\n✅ Complete!")
    print("📁 Files created:")
    print(f"   1. {result['guide_file']} - Main guide (OPEN THIS)")
    print(f"   2. {result['chart_file']} - Interactive charts")
    print(f"\n🌐 Open '{result['guide_file']}' in your browser!")

if __name__ == "__main__":
    main()