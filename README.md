# MAI KỲ HÀ Seafood

Bilingual Vietnamese / English seafood company website.

**Kết nối đại dương, phủ sóng toàn cầu.**  
**Connecting oceans, reaching the world.**

## Contents

- `dist/`: complete static website, shared images, styles and scripts; 28 pages per language.
- `build.py`, `detail_content.py`, `finish_content.py`: Vietnamese content and page generation.
- `english.py`, `en_translations.tsv`: English translations, routes and language navigation.
- `products.json`: generated product catalog.
- `tests/`, `validate.py`: static validation and interaction logic checks.

## Build

Requires Python 3 with Pillow. Node.js is used for the JavaScript checks.

```sh
python -m pip install -r requirements.txt
python build.py
python validate.py
python tests/bilingual.py
node --check dist/assets/app.js
node tests/hero-motion.cjs
node tests/inquiry.cjs
TEST_LANGUAGE=en node tests/inquiry.cjs
node tests/language-switch.cjs
```

All optimized images are included in `dist/assets/`. Keep them when rebuilding: the original photo archives are not required while these assets exist. Original upload paths in `build.py` are fallback paths only.

## Deployment notes

All links inside `dist/` are relative, so the same files work at a domain root, under a GitHub Pages project path (for example `https://<user>.github.io/maikyha/`) or opened locally. Vietnamese pages live at the site root; English pages live in `en/`.

### GitHub Pages

1. Push this repository to GitHub on the `main` branch, including `dist/assets/`.
2. In the repository, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` builds the site, runs every check, and publishes `dist/`. The site address appears in the **Actions** run and under **Settings → Pages**.

The workflow sets `SITE_URL` to the GitHub Pages address automatically; it is used only for canonical and language (hreflang) tags. When a custom domain is ready, change `SITE_URL` in the workflow to that domain (for example `https://maikyha.com`) and add the domain under **Settings → Pages**.

The contact form prepares an email using the visitor's email application; it does not submit to a backend. The visitor must review and send the email. A copy-text fallback is included.

## Validation scope

Checks cover page and asset links, translations, language switching, inquiry form logic and hero autoplay. These checks do not replace visual browser testing.
