"""Flask web app for interactive stock analysis with HTML GUI"""
import os
import sys
import traceback
from flask import Flask, request, jsonify, send_from_directory, render_template_string

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Output directory for generated HTML files
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lock file to prevent concurrent analysis for same ticker
import threading
analysis_locks = {}
lock_manager = threading.Lock()


def get_lock(ticker):
    with lock_manager:
        if ticker not in analysis_locks:
            analysis_locks[ticker] = threading.Lock()
        return analysis_locks[ticker]


@app.route('/')
def index():
    """Serve the main HTML GUI page"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stock Analysis Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: #0f0f23;
                color: #e0e0e0;
                min-height: 100vh;
            }

            .navbar {
                background: linear-gradient(135deg, #1a1a3e 0%, #2d1b69 100%);
                padding: 15px 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 2px solid #3d2b7e;
                position: sticky;
                top: 0;
                z-index: 100;
            }

            .navbar .logo {
                font-size: 1.5em;
                font-weight: 700;
                color: #fff;
            }

            .navbar .logo span {
                color: #7c5cfc;
            }

            .search-box {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .search-box input {
                padding: 12px 20px;
                font-size: 1.1em;
                border: 2px solid #3d2b7e;
                border-radius: 30px;
                background: #1a1a3e;
                color: #fff;
                width: 250px;
                outline: none;
                transition: all 0.3s;
            }

            .search-box input:focus {
                border-color: #7c5cfc;
                box-shadow: 0 0 15px rgba(124, 92, 252, 0.3);
            }

            .search-box input::placeholder {
                color: #666;
            }

            .btn-analyze {
                padding: 12px 35px;
                font-size: 1.1em;
                font-weight: 600;
                border: none;
                border-radius: 30px;
                background: linear-gradient(135deg, #7c5cfc 0%, #9b59b6 100%);
                color: white;
                cursor: pointer;
                transition: all 0.3s;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .btn-analyze:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(124, 92, 252, 0.4);
            }

            .btn-analyze:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            .btn-analyze .spinner {
                display: none;
                width: 18px;
                height: 18px;
                border: 2px solid rgba(255,255,255,0.3);
                border-top-color: #fff;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                margin-right: 8px;
                vertical-align: middle;
            }

            .btn-analyze.loading .spinner {
                display: inline-block;
            }

            .btn-analyze.loading .btn-text {
                display: none;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            .main-content {
                padding: 30px;
                max-width: 1600px;
                margin: 0 auto;
            }

            .status-bar {
                text-align: center;
                padding: 20px;
                font-size: 1.1em;
                color: #888;
            }

            .status-bar.success {
                color: #00cc66;
            }

            .status-bar.error {
                color: #ff4444;
            }

            .result-tabs {
                display: flex;
                gap: 5px;
                margin-bottom: 0;
                flex-wrap: wrap;
            }

            .tab-btn {
                padding: 12px 25px;
                background: #1a1a3e;
                border: 1px solid #3d2b7e;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
                color: #888;
                cursor: pointer;
                font-size: 0.95em;
                transition: all 0.3s;
            }

            .tab-btn:hover {
                color: #fff;
                background: #2d1b69;
            }

            .tab-btn.active {
                background: #2d1b69;
                color: #fff;
                border-color: #7c5cfc;
                box-shadow: 0 -2px 10px rgba(124, 92, 252, 0.2);
            }

            .tab-content {
                display: none;
                background: #1a1a3e;
                border: 1px solid #3d2b7e;
                border-radius: 0 10px 10px 10px;
                overflow: hidden;
            }

            .tab-content.active {
                display: block;
            }

            .tab-content iframe {
                width: 100%;
                height: 85vh;
                border: none;
            }

            .recommendation-badge {
                display: inline-block;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: 700;
                font-size: 1.2em;
                margin-left: 15px;
            }

            .badge-BUY, .badge-STRONG_BUY {
                background: rgba(0, 204, 102, 0.2);
                color: #00cc66;
            }

            .badge-SELL, .badge-STRONG_SELL {
                background: rgba(255, 68, 68, 0.2);
                color: #ff4444;
            }

            .badge-NEUTRAL, .badge-HOLD {
                background: rgba(255, 215, 0, 0.2);
                color: #ffd700;
            }

            .quick-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 25px;
            }

            .stat-card {
                background: #1a1a3e;
                border: 1px solid #3d2b7e;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
            }

            .stat-card .label {
                font-size: 0.85em;
                color: #888;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }

            .stat-card .value {
                font-size: 1.8em;
                font-weight: 700;
            }

            .hidden {
                display: none !important;
            }

            @media (max-width: 768px) {
                .navbar {
                    flex-direction: column;
                    gap: 15px;
                }
                .search-box input {
                    width: 180px;
                }
                .tab-btn {
                    padding: 10px 15px;
                    font-size: 0.85em;
                }
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <div class="logo">📊 <span>StockScope</span> Pro</div>
            <div class="search-box">
                <input
                    type="text"
                    id="tickerInput"
                    placeholder="Enter ticker (e.g., GOOGL)"
                    autocomplete="off"
                    autofocus
                >
                <button class="btn-analyze" id="analyzeBtn" onclick="runAnalysis()">
                    <span class="spinner"></span>
                    <span class="btn-text">Analyze</span>
                </button>
            </div>
        </div>

        <div class="main-content">
            <div id="statusBar" class="status-bar">
                Enter a stock ticker above and click <strong>Analyze</strong>
            </div>

            <!-- Results section (hidden until analysis done) -->
            <div id="resultsSection" class="hidden">
                <!-- Quick stats -->
                <div class="quick-stats" id="quickStats"></div>

                <!-- Tabs -->
                <div class="result-tabs">
                    <button class="tab-btn active" onclick="switchTab('technical')">📈 Technical Analysis</button>
                    <button class="tab-btn" onclick="switchTab('chart')">📊 Price Chart & MAs</button>
                    <button class="tab-btn" onclick="switchTab('support')">🎯 Support & Resistance</button>
                </div>

                <div class="tab-content active" id="tab-technical">
                    <iframe id="iframe-technical" src="" title="Technical Analysis"></iframe>
                </div>
                <div class="tab-content" id="tab-chart">
                    <iframe id="iframe-chart" src="" title="Price Chart"></iframe>
                </div>
                <div class="tab-content" id="tab-support">
                    <iframe id="iframe-support" src="" title="Support & Resistance"></iframe>
                </div>
            </div>
        </div>

        <script>
            let currentAnalysis = null;

            function switchTab(tabName) {
                // Update tab buttons
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');

                // Update tab content
                document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
                document.getElementById('tab-' + tabName).classList.add('active');
            }

            function setStatus(msg, type) {
                const bar = document.getElementById('statusBar');
                bar.textContent = msg;
                bar.className = 'status-bar ' + (type || '');
            }

            function setLoading(loading) {
                const btn = document.getElementById('analyzeBtn');
                if (loading) {
                    btn.classList.add('loading');
                    btn.disabled = true;
                } else {
                    btn.classList.remove('loading');
                    btn.disabled = false;
                }
            }

            async function runAnalysis() {
                const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
                if (!ticker) {
                    setStatus('⚠️ Please enter a stock ticker', 'error');
                    return;
                }

                setLoading(true);
                setStatus('⏳ Analyzing ' + ticker + '... Fetching data...', '');
                document.getElementById('resultsSection').classList.add('hidden');

                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ ticker: ticker })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.error || 'Analysis failed');
                    }

                    currentAnalysis = data;

                    // Update iframes with timestamp to prevent caching
                    const ts = new Date().getTime();
                    document.getElementById('iframe-technical').src = '/files/' + data.technical_file + '?t=' + ts;
                    document.getElementById('iframe-chart').src = '/files/' + data.chart_file + '?t=' + ts;
                    document.getElementById('iframe-support').src = '/files/' + data.support_file + '?t=' + ts;

                    // Show quick stats
                    const statsDiv = document.getElementById('quickStats');
                    if (data.recommendation) {
                        const badgeClass = 'badge-' + data.recommendation.replace(/ /g, '_');
                        statsDiv.innerHTML = `
                            <div class="stat-card">
                                <div class="label">Ticker</div>
                                <div class="value" style="color:#7c5cfc;">${ticker}</div>
                            </div>
                            <div class="stat-card">
                                <div class="label">Recommendation</div>
                                <div class="value"><span class="recommendation-badge ${badgeClass}">${data.recommendation}</span></div>
                            </div>
                            <div class="stat-card">
                                <div class="label">Buy Signals</div>
                                <div class="value" style="color:#00cc66;">${data.buy_signals !== undefined ? data.buy_signals : '—'}</div>
                            </div>
                            <div class="stat-card">
                                <div class="label">Sell Signals</div>
                                <div class="value" style="color:#ff4444;">${data.sell_signals !== undefined ? data.sell_signals : '—'}</div>
                            </div>
                        `;
                    } else {
                        statsDiv.innerHTML = '';
                    }

                    // Show results
                    document.getElementById('resultsSection').classList.remove('hidden');

                    // Reset to first tab
                    document.querySelectorAll('.tab-btn').forEach((btn, i) => btn.classList.toggle('active', i === 0));
                    document.querySelectorAll('.tab-content').forEach((tc, i) => tc.classList.toggle('active', i === 0));

                    setStatus('✅ Analysis complete for ' + ticker + ' | ' + data.recommendation || 'Done', 'success');

                } catch (err) {
                    setStatus('❌ Error: ' + err.message, 'error');
                    console.error(err);
                } finally {
                    setLoading(false);
                }
            }

            // Allow pressing Enter to trigger analysis
            document.getElementById('tickerInput').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    runAnalysis();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/analyze', methods=['POST'])
def analyze():
    """Run all analyses for a given ticker and return file paths"""
    data = request.get_json()
    if not data or 'ticker' not in data:
        return jsonify({'error': 'Missing ticker parameter'}), 400

    ticker = data['ticker'].strip().upper()
    if not ticker or not ticker.isascii() or len(ticker) > 10:
        return jsonify({'error': 'Invalid ticker symbol'}), 400

    lock = get_lock(ticker)

    # Try to acquire lock without blocking; if busy, return immediately
    if not lock.acquire(blocking=False):
        return jsonify({'error': f'Analysis for {ticker} is already in progress. Please wait.'}), 429

    try:
        # Run all 3 analyses
        import fetch_stock
        import generate_html_analysis
        import create_support_resistance_guide

        result = {
            'ticker': ticker
        }

        # 1. Price Chart with Moving Averages
        chart_result = fetch_stock.run_analysis(ticker, output_dir=OUTPUT_DIR)
        result['chart_file'] = os.path.basename(chart_result['chart_file'])

        # 2. Technical Analysis Dashboard
        tech_result = generate_html_analysis.run_analysis(ticker, output_dir=OUTPUT_DIR)
        result['technical_file'] = os.path.basename(tech_result['dashboard_file'])
        result['recommendation'] = tech_result['recommendation']
        result['buy_signals'] = tech_result['buy_signals']
        result['sell_signals'] = tech_result['sell_signals']

        # 3. Support & Resistance Guide
        support_result = create_support_resistance_guide.run_analysis(ticker, output_dir=OUTPUT_DIR)
        result['support_file'] = os.path.basename(support_result['guide_file'])

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500
    finally:
        lock.release()


@app.route('/files/<path:filename>')
def serve_file(filename):
    """Serve generated HTML analysis files"""
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  📊 StockScope Pro - Stock Analysis Dashboard")
    print("=" * 60)
    print(f"\n  🌐 Server starting at: http://127.0.0.1:5000")
    print(f"  📁 Output directory: {OUTPUT_DIR}")
    print(f"\n  Open your browser and enter any stock ticker!")
    print("=" * 60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)