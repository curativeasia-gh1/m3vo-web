# M3VO website

Static multi-page website for m3vo.com, hosted on Cloudflare Pages. The repository root is the deployment output. M3VO provides software and automation services; the shared WhatsApp inbox is a product within that offering.

## Build and validate

Edit `_generator/build.py` for page content, metadata and structured data. Edit `_generator/styles.css` and `_generator/app.js` for shared styling and behaviour.

```sh
python3 _generator/build.py
python3 scripts/check_site.py _generator/dist
cp -R _generator/dist/. .
python3 scripts/check_site.py .
```

Commit the generator and regenerated output together. Cloudflare Pages uses an empty build command and `/` as the output directory. Keep the standalone preview out of search using its generated `noindex` tag.

## Content rules

- FAQ structured data must match the questions and answers displayed on that page.
- WhatsApp pricing is quote-based: do not reintroduce public tier prices or tier-specific AI entitlements in HTML, metadata, JSON-LD or llms.txt.
- Publish only verified company, team and customer facts. Case studies need customer permission and evidence for outcome claims.
- Cite official sources for grant guidance and show when the guidance was reviewed. Do not imply M3VO or its products are grant-approved without evidence.
- Product and service claims must agree across visible copy and machine-readable descriptions.

## Contact form

`functions/api/contact.js` handles POST `/api/contact`. Configure Resend and/or a webhook in Cloudflare Pages:

| Variable | Purpose |
|---|---|
| `CONTACT_TO` | Recipient; defaults to `hello@m3vo.com` |
| `RESEND_API_KEY` | Enables Resend email delivery |
| `CONTACT_FROM` | Verified Resend sender |
| `CONTACT_WEBHOOK_URL` | Optional enquiry webhook |

At least one delivery method is required. Without either, the endpoint returns a 503 and directs the visitor to email. Never commit credentials.

## After deployment

1. Verify the live homepage, WhatsApp page, updated guide, robots.txt and sitemap.xml.
2. Run `python3 scripts/indexnow.py --submit` (or pass changed URLs) to notify Bing and other IndexNow engines. It reads the key from the root `<key>.txt` file, which `_generator/build.py` writes; the file must be live before submitting. Run it without `--submit` first for a dry run.
3. Submit the sitemap and request recrawling of changed URLs in Google Search Console and Bing Webmaster Tools. Indexing and AI citations are not guaranteed.
4. Add verified team credentials and genuine customer case studies when the supporting material is available.
