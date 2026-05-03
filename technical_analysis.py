import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def fetch_stock_data(ticker_symbol, period='5y'):
    """Fetch stock data for any ticker"""
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    return hist

def calculate_indicators(data):
    """Calculate technical indicators"""
    # Moving Averages
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    
    # RSI (Relative Strength Index)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD (Moving Average Convergence Divergence)
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
    
    # Volume Moving Average
    data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
    
    return data

def analyze_signals(data):
    """Analyze technical signals"""
    current = data.iloc[-1]
    prev = data.iloc[-2]
    
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
        'price_vs_bb_upper': current['Close'] - current['BB_Upper'],
        'price_vs_bb_lower': current['Close'] - current['BB_Lower'],
        'volume_trend': 'High' if current['Volume'] > current['Volume_MA'] else 'Low'
    }
    
    return signals

def generate_recommendation(signals):
    """Generate buy/sell recommendation based on signals"""
    buy_signals = 0
    sell_signals = 0
    analysis_text = []
    
    # RSI Analysis
    if signals['rsi'] < 30:
        buy_signals += 2
        analysis_text.append(f"🟢 RSI ({signals['rsi']:.1f}) is OVERSOLD - Strong BUY signal")
    elif signals['rsi'] < 40:
        buy_signals += 1
        analysis_text.append(f"🟢 RSI ({signals['rsi']:.1f}) is near oversold - Mild BUY signal")
    elif signals['rsi'] > 70:
        sell_signals += 2
        analysis_text.append(f"🔴 RSI ({signals['rsi']:.1f}) is OVERBOUGHT - Strong SELL signal")
    elif signals['rsi'] > 60:
        sell_signals += 1
        analysis_text.append(f"🔴 RSI ({signals['rsi']:.1f}) is near overbought - Mild SELL signal")
    else:
        analysis_text.append(f"⚪ RSI ({signals['rsi']:.1f}) is NEUTRAL")
    
    # Price vs Moving Averages
    if signals['price_vs_ma20'] > 0 and signals['price_vs_ma50'] > 0 and signals['price_vs_ma200'] > 0:
        buy_signals += 1
        analysis_text.append(f"🟢 Price is ABOVE all major MAs (20, 50, 200) - UPTREND confirmed")
    elif signals['price_vs_ma20'] < 0 and signals['price_vs_ma50'] < 0 and signals['price_vs_ma200'] < 0:
        sell_signals += 1
        analysis_text.append(f"🔴 Price is BELOW all major MAs - DOWNTREND confirmed")
    else:
        analysis_text.append(f"⚪ Price is mixed relative to MAs - NEUTRAL trend")
    
    # Moving Average Alignment
    if signals['ma20_vs_ma50'] > 0 and signals['ma50_vs_ma200'] > 0:
        buy_signals += 1
        analysis_text.append(f"🟢 MAs are properly aligned (20 > 50 > 200) - BUY momentum")
    elif signals['ma20_vs_ma50'] < 0 and signals['ma50_vs_ma200'] < 0:
        sell_signals += 1
        analysis_text.append(f"🔴 MAs are inverted (20 < 50 < 200) - SELL momentum")
    
    # MACD Analysis
    if signals['macd'] > signals['signal_line']:
        buy_signals += 1
        analysis_text.append(f"🟢 MACD is ABOVE signal line - Bullish MACD crossover")
    else:
        sell_signals += 1
        analysis_text.append(f"🔴 MACD is BELOW signal line - Bearish MACD crossover")
    
    # Bollinger Bands
    if signals['price_vs_bb_lower'] < 0:
        buy_signals += 1
        analysis_text.append(f"🟢 Price is near/below lower Bollinger Band - Potential reversal UP")
    elif signals['price_vs_bb_upper'] > 0:
        sell_signals += 1
        analysis_text.append(f"🔴 Price is near/above upper Bollinger Band - Potential reversal DOWN")
    
    # Volume
    analysis_text.append(f"⚪ Volume: {signals['volume_trend']}")
    
    return buy_signals, sell_signals, analysis_text

def main():
    # Get ticker from user or use default
    ticker_symbol = input("Enter stock ticker (e.g., JPM, AAPL, MSFT): ").strip().upper() or "JPM"
    
    print("=" * 70)
    print(f"{ticker_symbol} STOCK TECHNICAL ANALYSIS")
    print("=" * 70)
    
    # Fetch data
    print(f"\n📊 Fetching {ticker_symbol} stock data (5 years)...")
    data = fetch_stock_data(ticker_symbol, period='5y')
    
    # Calculate indicators
    print("📈 Calculating technical indicators...")
    data = calculate_indicators(data)
    
    # Get latest signals
    signals = analyze_signals(data)
    
    # Generate recommendation
    buy_signals, sell_signals, analysis = generate_recommendation(signals)
    
    # Display results
    print("\n" + "=" * 70)
    print("CURRENT PRICE & KEY METRICS")
    print("=" * 70)
    print(f"\n💰 Current Price: ${signals['price']:.2f}")
    print(f"📊 RSI (14): {signals['rsi']:.2f} (30=oversold, 70=overbought)")
    print(f"📍 Distance from MA20: ${signals['price_vs_ma20']:.2f}")
    print(f"📍 Distance from MA50: ${signals['price_vs_ma50']:.2f}")
    print(f"📍 Distance from MA200: ${signals['price_vs_ma200']:.2f}")
    print(f"📊 MACD: {signals['macd']:.4f} | Signal: {signals['signal_line']:.4f}")
    print(f"📊 Volume Trend: {signals['volume_trend']}")
    
    print("\n" + "=" * 70)
    print("TECHNICAL ANALYSIS SIGNALS")
    print("=" * 70)
    for analysis_point in analysis:
        print(f"\n{analysis_point}")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATION")
    print("=" * 70)
    print(f"\n🟢 BUY Signals: {buy_signals}")
    print(f"🔴 SELL Signals: {sell_signals}")
    print(f"Net Score: {buy_signals - sell_signals}")
    
    if buy_signals > sell_signals + 1:
        recommendation = "🟢 STRONG BUY"
        color = "GREEN"
    elif buy_signals > sell_signals:
        recommendation = "🟢 BUY"
        color = "GREEN"
    elif sell_signals > buy_signals + 1:
        recommendation = "🔴 STRONG SELL"
        color = "RED"
    elif sell_signals > buy_signals:
        recommendation = "🔴 SELL"
        color = "RED"
    else:
        recommendation = "⚪ NEUTRAL / HOLD"
        color = "NEUTRAL"
    
    print(f"\n{'='*70}")
    print(f"📌 VERDICT: {recommendation}")
    print(f"{'='*70}")
    
    print("\n" + "=" * 70)
    print("EXPLANATION")
    print("=" * 70)
    
    if "STRONG BUY" in recommendation:
        print("""
✅ Multiple bullish indicators suggest strong upside momentum:
   • Price is above all major moving averages (uptrend)
   • RSI shows oversold conditions (buying opportunity)
   • MACD shows positive crossover
   • Moving averages are in proper bullish alignment
   
💡 STRATEGY: Consider accumulating on dips. Good entry point.
⚠️  Risk: Always use stop-loss below recent support levels.
""")
    elif "BUY" in recommendation:
        print("""
✅ More bullish than bearish signals present:
   • Price is trending above key moving averages
   • Technical setup supports further upside
   
💡 STRATEGY: Look for pullbacks to moving averages for entry.
⚠️  Risk: Monitor RSI for overbought conditions (>70).
""")
    elif "STRONG SELL" in recommendation:
        print("""
❌ Multiple bearish indicators suggest strong downside pressure:
   • Price is below all major moving averages (downtrend)
   • RSI shows overbought conditions
   • MACD shows negative crossover
   • Moving averages are inverted (bearish)
   
⛔ STRATEGY: Avoid buying. Consider short positions if experienced.
⚠️  Risk: Major support levels must be respected.
""")
    elif "SELL" in recommendation:
        print("""
❌ More bearish than bullish signals present:
   • Price is trending below key moving averages
   • Technical setup suggests downside continuation
   
⛔ STRATEGY: Wait for reversal signals before considering entry.
⚠️  Risk: Watch for bounce at support levels.
""")
    else:
        print("""
⚪ Market is balanced between bulls and bears:
   • Mixed technical signals
   • No strong directional bias
   
💡 STRATEGY: Wait for clearer signals before committing capital.
⚠️  Risk: Market could break either direction. Use wider stops.
""")
    
    print("\n" + "=" * 70)
    print("DISCLAIMER")
    print("=" * 70)
    print("""
This technical analysis is educational and not financial advice.
Stock markets are risky. Past performance doesn't guarantee future results.
Consult a financial advisor before making investment decisions.
Always use proper risk management (stop-losses, position sizing).
""")

if __name__ == "__main__":
    main()
