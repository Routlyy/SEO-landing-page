# Routly SEO landing

Static site. No build step.

- `index.html` — page
- `styles.css` — styles (palette + type tokens in `:root`)
- `assets/hero.jpg` — hero arch image
- `assets/cta-seo.jpg` — CTA banner image

Preview: `open index.html` or `python3 -m http.server 8080` then http://localhost:8080

Swap copy in `index.html`; swap colors in `:root` of `styles.css`.

CSS: source of truth is `styles.css`. It is minified and INLINED into all 6 HTML pages.
After any `styles.css` edit run `./build.sh` (wraps `build.py`) to re-inline, or the pages keep the old styles.

Fonts: self-hosted in `assets/fonts/` (Fraunces + Inter woff2, subset; Fraunces pinned to opsz 144, italic pinned to weight 300).
To change fonts, re-download from Google Fonts and update the `@font-face` block at the top of `styles.css`.

Local preview: `python3 serve.py` (port 8080). It gzips + sets cache headers like production (Vercel), so local Lighthouse numbers match the deploy. Plain `python3 -m http.server` also works but scores lower on Performance (no compression).

SEO: `sitemap.xml`, `robots.txt`, `vercel.json` (cache headers), canonical/hreflang/OG/JSON-LD in each page head. Canonical base is the Vercel deploy URL; swap it in all heads + `sitemap.xml` + `robots.txt` if a custom domain is added.
