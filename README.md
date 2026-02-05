# The Oracle's Almanac

A cyberpunk-styled prediction market dashboard that pulls live data from Polymarket.

## Quick Start

```bash
# Generate fresh almanac
python3 generate_almanac.py

# Start local server
./serve.sh
# Open http://localhost:8888
```

## Requirements

- Python 3.6+
- Internet connection (fetches from Polymarket API)

No additional packages needed — uses only Python standard library (`urllib`, `json`).

## Files

| File | Purpose |
|------|---------|
| `generate_almanac.py` | Fetches Polymarket data, generates HTML |
| `index.html` | The generated dashboard |
| `serve.sh` | Starts a local HTTP server on port 8888 |

## How It Works

1. Fetches top 10 active markets by 24h volume from Polymarket
2. Generates a static HTML page with:
   - Scrolling ticker of top markets
   - Featured analysis sections (currently hardcoded)
   - Top markets list with volumes
   - Generation timestamp

## Limitations

- **Featured sections are hardcoded** — "Featured Signal" and "Wildcard" don't update automatically
- **No mobile layout** — best viewed on desktop
- **No caching** — fails if Polymarket API is down

## Future Improvements

- [ ] LLM integration for dynamic market analysis
- [ ] Mobile responsive layout
- [ ] Automated regeneration (cron)
- [ ] Deployment to static hosting
- [ ] Email/Telegram distribution

## Development

To modify styling, edit the `<style>` block in `generate_almanac.py`.

The cyberpunk theme uses:
- `--accent: #00ff9d` (cyber green)
- `--secondary: #ff0055` (cyber pink)
- `--bg: #0a0a12` (dark background)
