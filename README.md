# ACC Landing

Responsive Spanish landing page for Inversiones ACC 2018 C.A. Built with plain HTML, CSS, and JavaScript, with no build step or runtime dependencies. `SPEC.md` defines the requirements; `design/reference.html` is the unchanged design source.

## Run locally

Open `index.html` directly in a browser, or serve this directory:

```sh
python3 -m http.server 8000
```

Visit `http://localhost:8000`. Google Fonts and the embedded Google map require an internet connection. With JavaScript disabled, static contact links and navigation still work; the mobile header exposes its navigation links.

## Customize

- **Images:** all foreground images use `object-fit: contain`. Product and learning cards show the complete supplied JPEGs; hero and industry use cleaned WebP derivatives. The `.media-surround` backgrounds fill unused image space with generated industrial/studio textures. Original JPEGs remain unchanged. When replacing an image, update its `src`, `width`, `height`, and `alt`, then review both desktop and mobile. Exact generation prompts and saved asset paths are in [design/ASSET_NOTES.md](design/ASSET_NOTES.md).
- **Logo:** replace the single inline `<symbol id="logo">` in `index.html`; header and footer reuse it through `<use>`. Update `favicon.svg` too. The five brand logos are local files in `img/brands/`; their provenance is documented in the asset notes. Keep Danfoss in its native red/white colors.
- **Motion:** below-fold blocks reveal once using IntersectionObserver; buttons, cards, links, and the mobile menu have restrained transitions. CSS timing lives at the end of `css/styles.css`, and reveal groups are at the end of `js/main.js`. Initial content remains visible, keyboard focus reveals its container immediately, and `prefers-reduced-motion` disables movement. Without JavaScript or IntersectionObserver, all content stays visible.
- **WhatsApp:** edit the number and messages in the `CONFIG` object at the top of `js/main.js`. Update the static `data-whatsapp` link URLs in `index.html` as well, so the no-JavaScript fallback agrees. Use country-code digits only, without a plus sign. Keep displayed phone numbers, `tel:` links, and JSON-LD consistent.
- **Instagram and map:** update `CONFIG.instagramUrl` / `CONFIG.mapsQuery` and the corresponding static HTML fallbacks. Update JSON-LD `sameAs` when Instagram changes.
- **Domain:** complete the canonical TODO and add `og:url` once the public domain is known. Social-image paths are relative as specified; use the final fully qualified image URL if your sharing platform requires it.

## Deploy to S3 and CloudFront

1. Install AWS CLI and configure credentials with access to the destination bucket and CloudFront invalidations.
2. Create a dedicated S3 bucket. Keep Block Public Access enabled and **do not enable S3 static website hosting**.
3. Create a CloudFront distribution with the bucket's regular S3 REST endpoint as its origin. Configure **Origin Access Control (OAC)** and a bucket policy allowing that distribution to read objects. Redirect HTTP viewers to HTTPS.
4. Set the CloudFront default root object to `index.html`. Use a cache policy with minimum TTL 0 so it honors the origin cache headers, and enable compression.
5. Deploy from any directory:

```sh
S3_BUCKET=your-dedicated-bucket \
CLOUDFRONT_DISTRIBUTION_ID=your-distribution-id \
./deploy.sh
```

The script fails before deployment if either variable is missing. It syncs the deployable files, deletes stale files within the included paths, applies five-minute caching to HTML/CSS/JS (also the favicon and robots file), uploads images with one-year immutable caching, and invalidates `/*`. Images are copied each time so cache metadata is correct even when their bytes have not changed. It excludes Git, the design, documentation, source briefs, and local validation artifacts through an allowlist. Use a dedicated bucket because `--delete` removes stale deployed files.

**TODO — custom domain:** create a Route 53 hosted zone, request and validate an ACM certificate in **us-east-1**, attach the certificate and alternate domain name to CloudFront, and create Route 53 A/AAAA alias records targeting the distribution. Then complete the canonical metadata in `index.html`.

## Validate

Node/npm are optional developer tools, never site dependencies:

```sh
npx html-validate index.html
bash -n deploy.sh
env -u S3_BUCKET -u CLOUDFRONT_DISTRIBUTION_ID bash deploy.sh
```

The final command must fail with a missing-variable message. Review desktop (1440×900) and mobile (390×844) screenshots against the reference, allowing the subsequently requested contained imagery, real logos, and motion. Check widths 320–1920px for overflow, exercise navigation and the mobile menu with a keyboard, and run mobile Lighthouse against the local HTTP server. See `IMPLEMENTATION_NOTES.md` for the completed acceptance results.
