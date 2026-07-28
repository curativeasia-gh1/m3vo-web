# m3vo-web

Marketing landing page for m3vo — a shared WhatsApp/omnichannel inbox positioned on pricing transparency (per-seat pricing, automation + AI included at the entry tier, Meta/BSP fees itemized rather than marked up).

## Structure

- `index.html` — single-page site: hero, cost breakdown, features, pricing, competitor comparison table, FAQ, CTA
- `styles.css` — all styling, no build step
- `script.js` — mobile nav toggle + FAQ accordion behavior

No framework, no build step — open `index.html` directly or serve the folder with any static host (Vercel, Netlify, GitHub Pages, S3).

## Before publishing

- Pricing figures ($19 / $49 / $99) and the competitor comparison table are illustrative, pulled from the July 2026 competitive research doc — confirm current numbers before this goes live.
- Replace the placeholder contact address (`hello@m3vo.io`) with a real one.
- No logo asset yet — the header/footer use a CSS gradient mark as a placeholder.

## Deploy to this repo

```
git init
git add .
git commit -m "Initial m3vo marketing site"
git branch -M main
git remote add origin https://github.com/curativeasia-gh1/m3vo-web.git
git push -u origin main
```
