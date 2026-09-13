# Implementation notes

Completed on September 13, 2026, on branch `codex/landing-page`.

The page uses plain HTML, CSS, and a dependency-free JavaScript IIFE. Every page section was implemented and committed in specification order: header, hero, products, brands, benefits, industry, learning, contact, and footer. SEO/deployment and final visual/performance corrections have separate commits. There is no build step, package manifest, runtime npm dependency, or application analytics.

`SPEC.md`, `design/reference.html`, and all eight original JPEGs are unchanged.

## Acceptance results — SPEC.md section 9

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. Desktop and mobile visual match | PASS | Captured 1440×900 and 390×844 viewport screenshots, full pages, and section crops; compared both reference artboards section by section. All corresponding section heights match in Chromium. Hero, brand, benefit, and contact-band comparisons have no detected pixel differences at Pixelmatch's 0.1 threshold; desktop products also match at that threshold. The real technician photo and live map replace the designated placeholders. Minor text rasterization differences and the required year are described below. |
| 2. No horizontal overflow | PASS | Automated browser assertions at every integer width from 320 through 1920px, including 320, 390, 768, 1024, 1440, and 1920px: 1,601 widths checked. |
| 3. HTML validation and clean runtime | PASS | `npx html-validate index.html`, `node --check js/main.js`, and `git diff --check` pass. A separate implementation-only browser session recorded zero console errors, HTTP errors/404s, or failed requests. |
| 4. Mobile Lighthouse ≥90 | PASS | Lighthouse 13.4.1 / Chromium 151: Performance **99**, Accessibility **100**, Best Practices **100**, SEO **100**. Final run: 2026-09-13 07:01:57 UTC. FCP 1.1s, LCP 2.1s, CLS 0.006, total blocking time 0ms. |
| 5. Keyboard operation | PASS | Enter/Space open the menu; Tab and Shift+Tab remain inside it; Escape and the close button close it and restore focus. All five menu links close it and navigate correctly. Every visible page link/button is reachable by Tab. Resizing to desktop closes the dialog and releases scroll locking. Also checked the menu in the Codex browser. |
| 6. CTAs and anchors | PASS | All nine WhatsApp links use `584125003831` and the exact default or category-specific message. Instagram, email, and both telephone links were checked. Header, footer, and mobile navigation land on the intended section without covering its heading. The Google Maps embed loaded and was visually verified at both target widths. |
| 7. Deployment checks | PASS | `bash -n deploy.sh` passes. The script rejects both missing variables and each individually missing variable. A mocked AWS CLI verified the sync/delete filters, cache headers, image upload, and final `/*` invalidation without contacting AWS. |

Additional checks: `file://` opening, no-JavaScript navigation and static contact fallbacks, image dimensions/lazy loading, semantic landmarks, Spanish metadata, JSON-LD, the single reusable logo symbol, reduced motion, and the scrolled header shadow.

## Reference differences and implementation decisions

- **Requested placeholder replacements:** `#industria` uses the supplied `tecnico-planta.jpg` with the prescribed crop and gradients; `#contacto` uses the real lazy-loaded Google Maps iframe. The original photograph contains social-post lettering, which remains because the specification requires this exact asset and prohibits JPEG re-encoding.
- **Requested working behavior:** the header is sticky, the hamburger opens a full-screen accessible dialog, links have real destinations, and the copyright includes the current year with a static 2026 fallback. The year is an explicit specification requirement even though the reference artboard does not show it.
- **Logo:** header and footer share one inline SVG symbol, as required, in place of the reference's HTML logotype. It retains the reference's font sizes, connector cut, caption, and mobile footer alignment. SVG text and semantic text wrappers can produce small subpixel rasterization differences; there is no intentional restyling.
- **Mobile artboard takes precedence for mobile presentation:** its shortened hero eyebrow, hidden side paragraphs/Instagram heading link, text-only product quote links with arrows, 120px image rows, and abbreviated footer location are preserved. The location remains in the mobile contact details. These reconcile the general section descriptions with the explicit A-mobile design.
- **Measured dimensions include borders:** the reference header's 88px/64px inner heights become 89px/65px with its border. Those complete heights are used for sticky-anchor offsets. Likewise, the map has a 440px/200px content height plus its two border pixels. Product rows preserve the reference's inline-image baseline spacing.
- **Font loading:** the Google Fonts stylesheet loads without blocking the initial render; the critical Oswald font is preloaded. A `noscript` stylesheet preserves the required fonts without JavaScript. The specified font families, weights, fallbacks, and final appearance are unchanged. This improved measured mobile Performance from 88 to 99 without modifying the JPEGs.
- **HTML validation:** two narrowly scoped, documented suppressions preserve explicit specification copy: `long-title` for the exact required title, and `tel-non-breaking` for the reference's literal telephone hyphens. All other recommended validation rules remain enabled; the final validator reports no errors or warnings.
- **Deployment packaging:** the script additionally allowlists deployable files so original social-media material, design briefs, notes, and local QA artifacts cannot be uploaded. The image pass uses `aws s3 cp --recursive` to reliably apply immutable cache metadata even when existing image bytes are unchanged. No AWS deployment was performed.

No other intentional visual or copy changes were made. Official ACC/brand vectors and the canonical/custom-domain configuration remain the explicit TODOs requested by the specification.

## Local verification artifacts

QA tools were installed outside the repository at `/tmp/acc-landing-qa`; they are not site dependencies. Screenshots, browser assertions, and deployment simulations are stored in `/tmp/acc-landing-qa/artifacts`:

- `viewport-1440.png`, `viewport-390.png`: required viewport captures.
- `actual-1440.png`, `actual-390.png`: complete page captures.
- `reference-desktop.png`, `reference-mobile.png`, `compare-*.png`, `visual-comparison.json`: reference comparisons.
- `contact-live-1440.png`, `contact-live-390.png`: visible, loaded map captures. Offscreen iframe content may be omitted by Chromium from a full-page capture, so the live map was captured separately while visible.
- `acceptance.json`, `deploy-checks.json`, `final-geometry-*.json`: automated assertions and geometry.
- `lighthouse-final.report.html`, `lighthouse-final.report.json`: final Lighthouse report.

These temporary artifacts can be removed without affecting the site. `README.md` documents local use, customization, validation, and S3/CloudFront setup.
