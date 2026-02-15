# The Oracle's Almanac 🔮

A cyberpunk-styled prediction market dashboard that pulls live data from Polymarket with AI-powered market analysis.

**Live Demo:** [https://ezra-anchovy.github.io/oracle-almanac/](https://ezra-anchovy.github.io/oracle-almanac/)

## Features

- 📊 **Live Polymarket Data** - Top 10 active markets by 24h volume
- 🤖 **AI-Powered Analysis** - GLM-5 generates "Featured Signal" and "Wildcard" predictions
- 📱 **Mobile Responsive** - Looks great on desktop, tablet, and mobile
- ⚡ **Auto-Updates** - Regenerates every 6 hours via GitHub Actions
- 🎨 **Cyberpunk UI** - Cyber green/pink aesthetic with smooth animations
- 📦 **Zero Dependencies** - Pure Python stdlib (urllib, json)

## Quick Start

```bash
# Set your GLM-5 API key (Z.ai)
export ZAI_API_KEY="your-api-key-here"

# Generate fresh almanac
python3 generate_almanac.py

# Start local server
./serve.sh
# Open http://localhost:8888
```

## Requirements

- **Python 3.6+**
- **ZAI_API_KEY** environment variable (for GLM-5 analysis)
  - Get it from [https://open.bigmodel.cn/](https://open.bigmodel.cn/)
  - Without it, the script runs in fallback mode (no AI analysis)
- Internet connection (fetches from Polymarket API)

**No packages to install** — uses only Python standard library (`urllib`, `json`).

## Deployment to GitHub Pages

### Initial Setup

1. **Fork or clone this repo**
   ```bash
   git clone https://github.com/ezra-anchovy/oracle-almanac.git
   cd oracle-almanac
   ```

2. **Add ZAI_API_KEY to GitHub Secrets**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `ZAI_API_KEY`
   - Value: Your GLM-5 API key from Z.ai

3. **Enable GitHub Pages**
   - Go to Settings → Pages
   - Source: **GitHub Actions** (not "Deploy from a branch")

4. **Trigger first deployment**
   ```bash
   # Either push a commit or run the workflow manually:
   # Go to Actions tab → "Update Oracle's Almanac" → Run workflow
   ```

5. **Your almanac is live!**
   - URL: `https://<your-username>.github.io/oracle-almanac/`
   - Updates automatically every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)

### Auto-Updates Schedule

The GitHub Action (`.github/workflows/update-almanac.yml`) runs:
- **Every 6 hours** via cron: `0 */6 * * *`
- **On every push** to main branch
- **Manually** via "Run workflow" button

Each run:
1. Fetches fresh Polymarket data
2. Generates new AI analysis via GLM-5
3. Updates `index.html`
4. Commits changes (if any)
5. Deploys to GitHub Pages

## Files

| File | Purpose |
|------|---------|
| `generate_almanac.py` | Fetches Polymarket data, calls GLM-5 for analysis, generates HTML |
| `index.html` | The generated static dashboard (auto-updated) |
| `serve.sh` | Starts a local HTTP server on port 8888 |
| `.github/workflows/update-almanac.yml` | GitHub Action for auto-regeneration |

## How It Works

1. **Fetch Markets** - Pulls top 10 active markets by 24h volume from Polymarket API
2. **AI Analysis** - Sends top 3 markets to GLM-5 for cynical, cyberpunk-styled analysis
   - "Reality Check" - What's actually happening (2-3 sentences)
   - "Oracle's Take" - Prediction/insight (1-2 sentences)
3. **Generate HTML** - Creates a static page with:
   - Scrolling ticker of top markets
   - Featured Signal (top market with full analysis)
   - Wildcard prediction (2nd market)
   - Signal Watch (3rd market)
   - Top markets sidebar
   - Generation timestamp
4. **Deploy** - GitHub Action pushes updated HTML to Pages

## Development

### Modify Styling

Edit the `<style>` block in `generate_almanac.py` (around line 140). The cyberpunk theme uses:
- `--accent: #00ff9d` (cyber green)
- `--secondary: #ff0055` (cyber pink)
- `--bg: #0a0a12` (dark background)

Mobile responsive breakpoints:
- `768px` - Tablet/mobile layout
- `480px` - Small mobile optimizations

### Change Update Frequency

Edit `.github/workflows/update-almanac.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Change to '0 */3 * * *' for every 3 hours
  # Change to '0 * * * *' for every hour
```

### Local Development Loop

```bash
# Watch for changes and regenerate (requires entr or similar)
ls generate_almanac.py | entr -r python3 generate_almanac.py

# Or just run manually:
python3 generate_almanac.py && open index.html
```

## Troubleshooting

### No AI Analysis (Fallback Mode)

If you see "The Oracle's vision is clouded" messages:
1. Check `ZAI_API_KEY` is set: `echo $ZAI_API_KEY`
2. Verify API key is valid at [https://open.bigmodel.cn/](https://open.bigmodel.cn/)
3. Check API quota/limits

### GitHub Action Fails

1. Verify `ZAI_API_KEY` secret is set in repo settings
2. Check Actions tab for error logs
3. Ensure Pages is enabled and set to "GitHub Actions" source

### Polymarket API Down

The script will fail gracefully if Polymarket API is unreachable. Check status or try again later.

## Future Enhancements

- [ ] Historical tracking (track market probability changes over time)
- [ ] Email/Telegram/Discord distribution
- [ ] RSS feed generation
- [ ] Dark/light theme toggle
- [ ] Shareable prediction cards (Open Graph images)
- [ ] Market sentiment indicators
- [ ] Volume spike detection

## License

MIT - Do whatever you want with it. The Oracle doesn't judge.

---

**Generated by OpenClaw // The Oracle Module**  
*Gazing into the future since 2026*
