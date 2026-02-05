#!/usr/bin/env python3
import json
import urllib.request
import datetime
import os
import sys

# Configuration
OUTPUT_FILE = "index.html"
POLYMARKET_API_URL = "https://gamma-api.polymarket.com/markets?limit=10&active=true&closed=false&order=volume24hr&ascending=false"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def generate_market_analysis(market_data):
    """
    Generate 2-3 sentence analysis for top 3 markets using Gemini API.
    Returns a list of dicts with 'question', 'probability', 'volume', 'analysis', 'oracle_take'.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ GOOGLE_API_KEY not set, using fallback analysis")
        return None
    
    analyses = []
    top_markets = market_data[:3]
    
    for market in top_markets:
        question = market.get('question', 'Unknown')
        outcomes = json.loads(market.get('outcomePrices', '[]'))
        yes_price = float(outcomes[0]) if len(outcomes) > 0 else 0
        probability = f"{yes_price * 100:.1f}%"
        volume = market.get('volume24hr', 0)
        description = market.get('description', '')[:500]  # Truncate for prompt
        
        prompt = f"""You are The Oracle, a cynical market analyst with a cyberpunk edge. Analyze this prediction market:

Question: {question}
Current Probability: {probability}
24h Volume: ${float(volume):,.0f}
Description: {description}

Provide:
1. REALITY CHECK (2-3 sentences): What's the real situation? Any institutional signals, news, or context the market might be missing?
2. ORACLE'S TAKE (1-2 sentences): Your cynical, insightful prediction. Is this mispriced? Political theater? A sleeper bet?

Keep it punchy and cyberpunk. No fluff. Format as JSON:
{{"reality_check": "...", "oracle_take": "..."}}"""

        try:
            request_data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.8, "maxOutputTokens": 300}
            }
            
            req = urllib.request.Request(
                f"{GEMINI_API_URL}?key={api_key}",
                data=json.dumps(request_data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.load(response)
                text = result['candidates'][0]['content']['parts'][0]['text']
                # Extract JSON from response (handle markdown code blocks)
                if '```json' in text:
                    text = text.split('```json')[1].split('```')[0]
                elif '```' in text:
                    text = text.split('```')[1].split('```')[0]
                analysis_json = json.loads(text.strip())
                
                analyses.append({
                    'question': question,
                    'probability': probability,
                    'volume': f"${float(volume):,.0f}",
                    'reality_check': analysis_json.get('reality_check', 'Analysis unavailable.'),
                    'oracle_take': analysis_json.get('oracle_take', 'The Oracle remains silent.')
                })
                print(f"  ✓ Analyzed: {question[:50]}...")
                
        except Exception as e:
            print(f"  ⚠️ Failed to analyze '{question[:40]}...': {e}")
            analyses.append({
                'question': question,
                'probability': probability,
                'volume': f"${float(volume):,.0f}",
                'reality_check': 'The Oracle\'s vision is clouded for this market.',
                'oracle_take': 'Signals unclear. Proceed with caution.'
            })
    
    return analyses

def fetch_top_markets():
    try:
        req = urllib.request.Request(
            POLYMARKET_API_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            return data
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return []

def format_currency(val):
    if not val: return "$0"
    return f"${float(val):,.0f}"

def format_percent(val):
    if not val: return "0%"
    return f"{float(val)*100:.1f}%"

def generate_html(markets, analyses=None):
    # Get top 5 for the ticker
    ticker_items = []
    for m in markets[:5]:
        question = m.get('question', 'Unknown')
        outcomes = json.loads(m.get('outcomePrices', '[]'))
        yes_price = outcomes[0] if len(outcomes) > 0 else 0
        ticker_items.append(f"{question} (YES: {float(yes_price)*100:.1f}%)")
    
    ticker_text = "  ///  ".join(ticker_items)

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d %H:%M")
    last_updated = now.strftime("%B %d, %Y at %H:%M:%S %Z") or now.strftime("%B %d, %Y at %H:%M:%S EST")
    
    # Build dynamic featured sections from analyses
    featured_sections = ""
    if analyses and len(analyses) > 0:
        # Primary featured market
        a = analyses[0]
        featured_sections += f"""
            <div class="card">
                <h2>Featured Signal: {a['question'][:60]}{'...' if len(a['question']) > 60 else ''}</h2>
                <p><strong>Market:</strong> {a['question']}</p>
                <div class="stat-row">
                    <span>Volume: {a['volume']}</span>
                    <span>Status: Active</span>
                </div>
                <div class="probability">{a['probability']}</div>
                <div class="probability-label">Market Probability</div>
                
                <p><strong>The Reality Check:</strong></p>
                <p>{a['reality_check']}</p>
                
                <div class="insight">
                    "The Oracle's Take: {a['oracle_take']}"
                </div>
            </div>
"""
        # Secondary market (if available)
        if len(analyses) > 1:
            a2 = analyses[1]
            featured_sections += f"""
            <div class="card">
                <h2>The Wildcard: {a2['question'][:50]}{'...' if len(a2['question']) > 50 else ''}</h2>
                <p><strong>Market:</strong> {a2['question']}</p>
                <div class="probability">{a2['probability']}</div>
                <p><strong>The Reality Check:</strong></p>
                <p>{a2['reality_check']}</p>
                <div class="insight">
                    "The Oracle's Take: {a2['oracle_take']}"
                </div>
            </div>
"""
        # Third market (if available)
        if len(analyses) > 2:
            a3 = analyses[2]
            featured_sections += f"""
            <div class="card">
                <h2>Signal Watch: {a3['question'][:50]}{'...' if len(a3['question']) > 50 else ''}</h2>
                <p><strong>Market:</strong> {a3['question']}</p>
                <div class="stat-row">
                    <span>Volume: {a3['volume']}</span>
                    <span>Probability: {a3['probability']}</span>
                </div>
                <p>{a3['reality_check']}</p>
                <div class="insight">
                    "The Oracle's Take: {a3['oracle_take']}"
                </div>
            </div>
"""
    else:
        # Fallback static content if no analyses available
        featured_sections = """
            <div class="card">
                <h2>Featured Signal</h2>
                <p>The Oracle's vision is currently clouded. API analysis unavailable.</p>
                <div class="insight">
                    "Check back soon for market insights."
                </div>
            </div>
"""

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THE ORACLE'S ALMANAC</title>
    <style>
        :root {{
            --bg: #0a0a12;
            --text: #e0e0e0;
            --accent: #00ff9d; /* Cyber Green */
            --secondary: #ff0055; /* Cyber Pink */
            --panel: #11111b;
            --border: #333344;
            --font-mono: 'Courier New', Courier, monospace;
            --font-display: 'Impact', sans-serif;
        }}
        
        body {{
            background-color: var(--bg);
            color: var(--text);
            font-family: var(--font-mono);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            border: 1px solid var(--border);
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.1);
        }}

        header {{
            border-bottom: 2px solid var(--accent);
            padding: 20px;
            text-align: center;
            background: radial-gradient(circle at center, #1a1a2e 0%, #0a0a12 100%);
        }}

        h1 {{
            font-family: var(--font-display);
            font-size: 3rem;
            margin: 0;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: var(--accent);
            text-shadow: 2px 2px 0px var(--secondary);
        }}

        .meta {{
            font-size: 0.8rem;
            color: #888;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .ticker-wrap {{
            width: 100%;
            overflow: hidden;
            background-color: var(--accent);
            color: var(--bg);
            white-space: nowrap;
            padding: 5px 0;
            font-weight: bold;
            border-bottom: 1px solid var(--border);
        }}

        .ticker {{
            display: inline-block;
            animation: ticker 30s linear infinite;
        }}

        @keyframes ticker {{
            0% {{ transform: translate3d(100%, 0, 0); }}
            100% {{ transform: translate3d(-100%, 0, 0); }}
        }}

        .grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            padding: 20px;
        }}

        .main-col {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .card {{
            background: var(--panel);
            border: 1px solid var(--border);
            padding: 20px;
            position: relative;
        }}
        
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--secondary), transparent);
        }}

        h2 {{
            color: var(--accent);
            border-bottom: 1px dashed var(--border);
            padding-bottom: 10px;
            margin-top: 0;
            font-size: 1.2rem;
            text-transform: uppercase;
        }}

        .stat-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9rem;
        }}

        .probability {{
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--secondary);
            text-align: center;
            margin: 10px 0;
        }}
        
        .probability-label {{
            text-align: center;
            font-size: 0.8rem;
            color: #888;
            text-transform: uppercase;
        }}

        .insight {{
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-left: 3px solid var(--secondary);
            margin-top: 15px;
            font-style: italic;
        }}

        .tag {{
            background: var(--border);
            padding: 2px 6px;
            font-size: 0.7rem;
            border-radius: 4px;
        }}

        footer {{
            text-align: center;
            padding: 20px;
            font-size: 0.8rem;
            color: #555;
            border-top: 1px solid var(--border);
        }}

    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>The Oracle's Almanac</h1>
        <div class="meta">Vol. 1 // Issue {datetime.datetime.now().strftime('%j')} // {today}</div>
    </header>

    <div class="ticker-wrap">
        <div class="ticker">{ticker_text}</div>
    </div>

    <div class="grid">
        <div class="main-col">
{featured_sections}
        </div>

        <div class="sidebar">
            <div class="card">
                <h2>Top Active Markets</h2>
                <ul style="padding-left: 20px; font-size: 0.9rem;">
    """
    
    for m in markets[:5]:
        q = m.get('question')
        vol = format_currency(m.get('volume24hr'))
        html += f"<li>{q}<br><span class='tag'>{vol} Vol</span></li>"

    html += f"""
                </ul>
            </div>
            
            <div class="card">
                <h2>Data Info</h2>
                <div class="stat-row">
                    <span>Status:</span>
                    <span style="color: var(--accent)">LIVE</span>
                </div>
                <div class="stat-row">
                    <span>Updated:</span>
                    <span>{today}</span>
                </div>
                <div class="stat-row">
                    <span>Markets:</span>
                    <span>{len(markets)} tracked</span>
                </div>
            </div>
        </div>
    </div>

    <footer>
        Generated by OpenClaw // The Oracle Module<br>
        <span style="color: var(--accent);">Last Updated: {last_updated}</span>
    </footer>
</div>

</body>
</html>
    """
    return html

def main():
    print("🔮 Gazing into the future...")
    markets = fetch_top_markets()
    if not markets:
        print("❌ Clouded vision. Could not fetch markets.")
        sys.exit(1)
        
    print(f"📊 Fetched {len(markets)} active markets.")
    
    print("🤖 Consulting Gemini for market analysis...")
    analyses = generate_market_analysis(markets)
    if analyses:
        print(f"✓ Generated {len(analyses)} market analyses")
    else:
        print("⚠️ Running without LLM analysis (fallback mode)")
    
    html = generate_html(markets, analyses)
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
        
    print(f"✨ Prophecy sealed: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
