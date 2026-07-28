# m3vo-web

Marketing landing page for **M3VO** (Mevo Tech, a project by Curative Holdings) — a shared WhatsApp/omnichannel inbox positioned on pricing transparency (per-seat pricing, automation + AI included at the entry tier, Meta/BSP fees itemized rather than marked up).

- Domain: m3vo.com
- Contact: hello@m3vo.com

## Structure

- `index.html` — single-page site: hero, cost breakdown, features, pricing, competitor comparison table, FAQ, CTA. Includes canonical URL, Open Graph/Twitter meta, favicons, and JSON-LD (Organization, SoftwareApplication/offers, FAQPage).
- `styles.css` — all styling, no build step
- `script.js` — mobile nav toggle + FAQ accordion behavior
- `assets/` — logo (512/1024), favicons, apple-touch-icon, OG share image (1200×630)
- `favicon.ico` — multi-size icon at repo root
- `robots.txt` — allows all standard and AI/answer-engine crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, etc.)
- `sitemap.xml` — single-page sitemap
- `llms.txt` — plain-language product/pricing summary for LLM crawlers and agents

No framework, no build step — open `index.html` directly or serve the folder with any static host (Vercel, Netlify, GitHub Pages, S3).

## Before publishing

- Pricing figures ($19 / $49 / $99) and the competitor comparison table are illustrative, pulled from the July 2026 competitive research doc — confirm current numbers before this goes live.
- All `https://m3vo.com/...` URLs (canonical, OG, sitemap, JSON-LD, robots.txt) assume the site is deployed at the root of that domain — update them if the deploy target changes.

## Deploy to this repo

```
git init
git add .
git commit -m "Initial m3vo marketing site"
git branch -M main
git remote add origin https://github.com/curativeasia-gh1/m3vo-web.git
git push -u origin main
```
