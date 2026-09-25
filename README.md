# ACC Landing

Responsive Spanish landing page for Inversiones ACC 2018 C.A. Built with plain HTML, CSS, and JavaScript, with no runtime dependencies. Local preview needs no build; AWS publishing uses a small Python packaging step. `SPEC.md` defines the original requirements; `design/reference.html` is the unchanged design source. Subsequent approved feedback and verification are recorded in `IMPLEMENTATION_NOTES.md`.

## Run locally

Open `index.html` directly in a browser, or serve this directory:

```sh
python3 -m http.server 8000
```

Visit `http://localhost:8000`. Google Fonts and the embedded Google map require an internet connection. With JavaScript disabled, static contact links and navigation still work; the mobile header exposes its navigation links.

## Customize

- **Images:** all foreground images use `object-fit: contain`. Product and learning cards show the complete supplied JPEGs; hero and industry use cleaned WebP derivatives. The `.media-surround` backgrounds fill unused image space with generated industrial/studio textures. Original JPEGs remain unchanged. When replacing an image, update its `src`, `width`, `height`, and `alt`, then review both desktop and mobile. Exact generation prompts and saved asset paths are in [design/ASSET_NOTES.md](design/ASSET_NOTES.md).
- **Logo:** `img/acc-logo.png` is the original transparent PNG supplied by ACC, preserved without pixel edits. The shared `<symbol id="logo">` frames its artwork with an SVG viewBox for the header and footer. Update that viewBox if replacement artwork has different margins. `favicon.svg` embeds the same image and frames the ACC mark; update it when replacing the logo. The five supplier logos are local files in `img/brands/`; their provenance is documented in the asset notes. Keep Danfoss in its native red/white colors.
- **Motion:** below-fold blocks reveal once using IntersectionObserver; buttons, cards, links, and the mobile menu have restrained transitions. CSS timing lives at the end of `css/styles.css`, and reveal groups are at the end of `js/main.js`. Initial content remains visible, keyboard focus reveals its container immediately, and `prefers-reduced-motion` disables movement. Without JavaScript or IntersectionObserver, all content stays visible.
- **WhatsApp:** edit the number and messages in the `CONFIG` object at the top of `js/main.js`. Update the static `data-whatsapp` link URLs in `index.html` as well, so the no-JavaScript fallback agrees. Use country-code digits only, without a plus sign. Keep displayed phone numbers, `tel:` links, and JSON-LD consistent.
- **Instagram and map:** update `CONFIG.instagramUrl` / `CONFIG.mapsQuery` and the corresponding static HTML fallbacks. Update JSON-LD `sameAs` when Instagram changes.
- **Domain:** canonical, `og:url`, JSON-LD, sitemap, and social-image URLs use `https://inversionesacc.com/`. Runtime asset paths remain relative for local previews. The AWS packaging script versions public assets without editing original images.

## Production on AWS

- Official website: [inversionesacc.com](https://inversionesacc.com/).
- `www.inversionesacc.com` redirects to the official HTTPS root domain.
- Repository: [vzladude/acc-landing](https://github.com/vzladude/acc-landing).
- AWS profile: `personal`; region: `us-east-1`; stack: `acc-landing-production`.
- Architecture: private S3, CloudFront with OAC and dedicated WAF, ACM certificate, and the existing Route 53 zone.
- Public resource identifiers are in `deploy/aws-production.json`; credentials are never stored here.

See [AWS deployment and recovery](deploy/AWS_DEPLOYMENT.md) for infrastructure, costs, verification, and rollback.

```sh
export AWS_PROFILE=personal
export S3_BUCKET=acc-landing-production-767397867309
export CLOUDFRONT_DISTRIBUTION_ID=E29C4VUSCEAMTM
./deploy.sh --dry-run
./deploy.sh
```

`deploy.sh` checks the AWS account, dedicated bucket, distribution origin, and production URL before writing. Python 3 packages static files into the ignored `.qa/production-site/` directory; the browser still runs only HTML, CSS, and vanilla JavaScript. Original image bytes remain unchanged. Images, JavaScript, and favicon receive content hashes and one-year immutable caching. The small stylesheet is embedded in production HTML to avoid a blocking network request on mobile; `css/styles.css` remains the editable source. HTML, robots, and sitemap use five-minute caching. Assets upload first and HTML last; previous versions are retained for cached pages and rollback. The script invalidates CloudFront after publishing.

GitHub stores the source. Pushing to `main` does not deploy to AWS: run the commands above after the checks pass. `.github/workflows/pages.yml` publishes only a relocation notice at the former GitHub Pages URL. That notice points to the official domain, preserves query parameters and anchors with JavaScript, includes a no-JavaScript fallback, and is marked `noindex`.

## Validate

Node/npm are optional developer tools, never site dependencies:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/redirect.test.cjs
python3 scripts/build_site.py
npx html-validate index.html .qa/production-site/index.html deploy/pages-redirect.html
bash -n deploy.sh
env -u S3_BUCKET -u CLOUDFRONT_DISTRIBUTION_ID bash deploy.sh
```

The final command must fail with a missing-variable message. Review desktop (1440×900) and mobile (390×844) screenshots against the reference, allowing the subsequently requested contained imagery, real logos, and motion. Check widths 320–1920px for overflow, exercise navigation and the mobile menu with a keyboard, and run mobile Lighthouse against the local HTTP server. See `IMPLEMENTATION_NOTES.md` for the completed acceptance results.
