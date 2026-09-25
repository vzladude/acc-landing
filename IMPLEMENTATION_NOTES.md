# Implementation notes

## AWS production migration — September 25, 2026

Published the approved landing at **https://inversionesacc.com/** in the user's personal AWS account, following the IHM infrastructure pattern. Work was committed in deployment sections on `codex/aws-production`.

- Created CloudFormation stack `acc-landing-production` in `us-east-1`: private encrypted S3, signed OAC origin access, distribution-scoped bucket policy, dedicated WAF rate rule, managed security/cache policies, and a canonical redirect function. The distribution is `E29C4VUSCEAMTM`; no IHM resources were modified.
- ACM issued the certificate for root and www using DNS validation in the existing Route 53 hosted zone. The initial stack kept website DNS inactive. After successful preflight TLS/content checks, a separate reviewed change set added only root/www A and AAAA aliases. The stack is `UPDATE_COMPLETE`, CloudFront is `Deployed`, and the certificate is `ISSUED`.
- The dedicated CloudFront Free subscription is `ACTIVE`, including the WAF and Route 53 hosted zone. It is managed outside CloudFormation. Deployment identifiers and status are in `deploy/aws-production.json`; lifecycle and cost details are in `deploy/AWS_DEPLOYMENT.md`.
- Updated canonical, Open Graph, Twitter image URLs, JSON-LD, robots and sitemap to the official HTTPS root. HTTP, www, `/index.html`, and the temporary CloudFront host lead to the canonical site. Redirect checks preserve URL-encoded and repeated query parameters.
- Replaced direct repository syncing with a runtime-only Python packaging step, account/bucket/origin checks and `--dry-run`. Images, JavaScript and favicon have SHA-256-derived filenames; original image bytes remain intact. All inline SVG logo and CSS background references resolve. The small stylesheet is embedded in production HTML to remove a render-blocking round trip; the editable source stays in `css/styles.css`. The final package has 23 files / 755,537 bytes. Assets upload first, HTML last, prior assets remain available, and CloudFront is invalidated after publishing.
- The GitHub Pages workflow now packages only `deploy/pages-redirect.html`: a noindex relocation page with a direct link, browser redirect preserving query/fragment, and no-JavaScript fallback. GitHub remains the source repository; AWS uploads are explicit through `deploy.sh`.

Verification:

- Five Python tests pass, covering complete release assets and unchanged image bytes, consistent indexing/social URLs, reproducibility, invalid release rejection, and five missing/wrong AWS target cases. Four Node tests pass for canonical pass-through, alternate-host redirects, index normalization, and encoded/repeated query preservation.
- HTML validation passes for source, production HTML and the relocation notice; JavaScript and shell syntax and `git diff --check` pass.
- Pre-DNS verification checked all 24 initial files over normally validated TLS using `curl --connect-to`. After the stylesheet optimization, all 23 final public files returned HTTP 200 with matching SHA-256 hashes and expected cache headers. Source/infrastructure URLs and direct S3 object access were denied. All four S3 public-access blocks remain enabled.
- Browser checks at 320, 390, 768, 1024, 1440 and 1920px show no horizontal overflow. Desktop/mobile visual review verifies the real logo, hero, products, backgrounds and contact/map. All 14 HTML images loaded, all nine WhatsApp links retain the expected phone/message, and the email remains correct. The mobile menu opens with Enter, traps Tab/Shift+Tab, restores focus on Escape, and closes/focuses the destination after keyboard selection. Browser console errors: none.
- Final mobile Lighthouse 13.5.0 / Chrome 154.0.8037.57 on the public AWS URL: **99 Performance, 100 Accessibility, 100 Best Practices, 100 SEO**. FCP 0.9s, LCP 1.5s, CLS 0.054, TBT 40ms. Earlier diagnostic runs used the old installed Chrome 139 and are retained separately; the final audit used a freshly installed official stable native browser.

Evidence (ignored local files): `.qa/preflight-verification.json`, `.qa/production-verification.json`, `.qa/responsive-production.json`, `.qa/lighthouse-production-chrome154.report.html` / `.json`, and `.qa/production-desktop.png` / `production-mobile.png`. Deployment/recovery instructions are in `deploy/AWS_DEPLOYMENT.md`.

This migration fulfills hosting and custom-domain deployment. Form delivery, GA4 and Search Console remain separate pending integrations; no IHM analytics ID was reused. `SPEC.md`, `design/reference.html`, copy, original images and visual design were preserved. The approved migration's asset versioning and release packaging supersede the original deployment script's direct `--delete` sync and source-file caching behavior.

## Phase 1 — identity and positioning, September 23, 2026

Implemented the user's approved first phase on `codex/phase-1-identity-copy`, with separate commits for the logo, hero/metadata, product heading, brand wording, five benefits, and contact copy.

- Replaced the provisional typed ACC mark in header, footer, and favicon with the supplied official PNG. The source file at `img/acc-logo.png` is byte-for-byte unchanged; SVG viewports frame the existing artwork without editing its pixels. Details are in `design/ASSET_NOTES.md`.
- Kept “Maximizamos la continuidad de tu planta” and placed “ACC no solo suministra, sino que ayuda a identificar la solución correcta.” directly below it.
- Replaced the product stock heading with “Suministros eléctricos y soluciones de automatización” and removed stock/immediate-delivery/minute-based/same-day response claims from all live copy and search/social descriptions. Visually inspected the retained source posts for conflicting claims.
- Changed the supplier heading to “Trabajamos con marcas reconocidas”.
- Replaced the four old benefits with five concrete points: understanding the requirement, finding the solution, recognized brands, optimizing the purchase, and accompanying the customer. The fifth benefit spans both columns, preserving the existing typography and orange-rule styling.
- Contact now says “Gestionamos tu requerimiento con rapidez” and lists “Realizamos envíos nacionales” under coverage. The confirmed destination email remains `attcliente2018@gmail.com`.
- Adjusted logo dimensions and the longer product heading across breakpoints. Existing contained imagery, animation, WhatsApp destinations, map, and source/reference files remain intact.

Scope follows the phased plan: form delivery is phase 2, analytics is phase 3, and expanded categories/process/verified trust data are phase 4. Phase 1 does not mark the complete original P0 feedback as finished. No form or analytics service was configured in this phase.

Verification on this revision:

- HTML validation, JavaScript syntax, Bash syntax, and whitespace checks pass. A scan of live text and metadata finds none of the retired claims. All nine WhatsApp destinations retain the correct number and exact default/category message; the confirmed email link is correct.
- Browser checks at 320, 360, 390, 600, 767, 768, 820, 900, 1024, 1100, 1280, 1440, and 1920px show no horizontal overflow, product-title clipping, or overlapping header controls. Desktop and mobile visual review includes the supplied logo, revised copy, product heading, and five benefits.
- Keyboard menu checks pass: Enter opens, Tab/Shift+Tab wrap, Escape closes and restores focus, and selecting a mobile anchor closes the menu and focuses the destination.
- Mobile Lighthouse 13.5.0, run at **2026-09-24 00:05:00 UTC** (September 23 in Venezuela): **95 Performance, 100 Accessibility, 100 Best Practices, 100 SEO**. FCP 1.1s, LCP 2.9s, CLS 0.01, TBT 40ms. Reports: `/tmp/acc-phase1-qa/artifacts/lighthouse.report.html` and `.json`; optional QA tooling is outside the repository.

Publication: [GitHub Pages deployment 35937122502](https://github.com/vzladude/acc-landing/actions/runs/35937122502) succeeded for site commit `24f7d9d6114b893b56baaba0fc3bc16a661def9b`. The public site was visually verified with the official logo and updated hero/brand/benefit content; all 23 hosted files returned HTTP 200 and matched the local bytes. Evidence: `/tmp/acc-phase1-qa/artifacts/published-files.json`. The working tree is on `main`, with the phase's section commits preserved.

## Earlier implementation and publication — September 13, 2026

Completed and refined on September 13, 2026, on branch `codex/landing-page`, then fast-forwarded to `main` for GitHub Pages publication.

The page uses plain HTML, CSS, and a dependency-free JavaScript IIFE. Every original page section was implemented and committed in specification order: header, hero, products, brands, benefits, industry, learning, contact, and footer. SEO/deployment, verification corrections, and the subsequent visual refinements have separate conventional commits. There is no build step, package manifest, runtime npm dependency, or application analytics.

`SPEC.md`, `design/reference.html`, and all eight original JPEGs are unchanged.

## Subsequent user-requested refinements

After approving the initial implementation as nearly perfect, the user requested complete contained images, ImageGen fills for resulting gaps, real brand logos, and professional animation. These instructions supersede the original reference's crop transforms, text-only brand placeholders, and restricted JavaScript responsibilities. The original pixel-match evidence remains historical; the current page intentionally includes the requested visual changes.

- **Complete images:** all 14 foreground images use `object-fit: contain`, with no image scale transforms. Product and learning cards show the complete original posts. Generated industrial and white studio backgrounds fill unused space. Mobile product rows have a 157px minimum image height to accommodate the full post.
- **Clean main photographs:** the hero uses a landscape ImageGen extension of the control-cabinet photo; the industry section uses a cleaned technician derivative. Their promotional lettering and overlaid marks were removed to keep page headings readable. These are illustrative generative edits and may reconstruct photographic details. The source JPEGs remain intact; only new assets were compressed to WebP.
- **Real brands:** Siemens, Schneider Electric, LS Electric, SICK, and Danfoss now use locally hosted authentic artwork. Five equal desktop tiles become a two-column mobile grid. Siemens, Schneider, and LS use white CSS silhouettes; SICK uses white source artwork, while Danfoss retains red and white. Source links, processing, exact ImageGen prompts, input references, and saved paths are in [design/ASSET_NOTES.md](design/ASSET_NOTES.md).
- **Motion:** below-fold sections and cards reveal once with a short fade and 20px vertical movement, staggered by 65ms. Buttons, cards, navigation underlines, Instagram links, and the mobile menu have restrained interactions. The initial hero is never hidden for an entrance animation. Focus immediately reveals its container. Reduced-motion preferences disable movement, including when changed during the session; no-JavaScript and no-IntersectionObserver fallbacks keep all content visible.

## September 13 acceptance results — SPEC.md section 9

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. Desktop and mobile visual review | VERIFIED WITH REQUESTED CHANGES | Captured 1440×900 and 390×844 viewports, full pages, and section crops. Reviewed contained product/learning posts, generated fills, clean main photographs, five logos, and preserved typography, colors, and section order. The updated user request replaces literal pixel equality for these visual treatments. The live map remains the required placeholder replacement. |
| 2. No horizontal overflow | PASS | Re-ran automated assertions on the final image assets at every integer width from 320 through 1920px: 1,601 widths, including all six mandatory sizes. |
| 3. HTML validation and clean runtime | PASS | `npx html-validate index.html`, `node --check js/main.js`, and `git diff --check` pass. Browser checks recorded zero console errors, HTTP errors/404s, or unexpected failed requests. All 14 images load, have correct aspect-ratio attributes, use contain, and have no scaling transforms. |
| 4. Mobile Lighthouse ≥90 | PASS | Lighthouse 13.4.1 / Chromium 151, final run **2026-09-13 08:17:27 UTC**: Performance **96**, Accessibility **100**, Best Practices **100**, SEO **100**. FCP 1.1s, LCP 2.8s, CLS 0.014, total blocking time 0ms. |
| 5. Keyboard operation | PASS | Enter/Space open the menu; Tab and Shift+Tab stay inside it; Escape and the close button close it and restore focus. All five menu links close it and navigate correctly. Every visible page link/button is reachable by Tab. Resizing to desktop releases the dialog and scroll lock. A separate motion test verifies immediately visible focused content. |
| 6. CTAs and anchors | PASS | All nine WhatsApp links use `584125003831` and the exact default or category-specific message. Instagram, email, and telephone URLs are correct. Header, footer, and mobile links land without the sticky header covering the target heading. The configured Google Maps iframe loads. |
| 7. Deployment checks | PASS | `bash -n deploy.sh` passes. Previous missing-variable and mocked-AWS checks remain valid for the unchanged script: it rejects both absent variables and either individually absent variable; sync/delete filters, cache headers, image upload, and `/*` invalidation were verified without contacting AWS. New nested logo/background assets are covered by its existing recursive image upload. |

Additional final checks: `file://` opening, no-JavaScript navigation and contact fallbacks, semantic landmarks, Spanish metadata, JSON-LD, one reusable ACC logo symbol, image loading and proportions, one-time reveals, runtime reduced-motion changes, observer-unavailable fallback, and the scrolled header shadow.

## Original implementation decisions retained

- The header is sticky, the hamburger opens an accessible full-screen dialog, links have real destinations, and the copyright includes the current year with a static 2026 fallback.
- Header and footer share one inline SVG symbol reproducing the reference's ACC logotype, connector cut, caption, and mobile alignment. An official ACC vector remains a TODO.
- The mobile artboard's shortened hero eyebrow, hidden side paragraphs/Instagram heading link, text-only product quote links with arrows, 120px thumbnail widths, and shortened footer location remain. Full location details appear in the contact section.
- Header anchor offsets include the border: 89px desktop and 65px mobile. Map content heights remain 440px desktop and 200px mobile, plus borders.
- The Google Fonts stylesheet loads without blocking the initial render; critical Oswald is preloaded. A `noscript` stylesheet supplies fonts without JavaScript. Required families, weights, and fallbacks remain.
- Two narrowly scoped HTML-validator suppressions preserve specification copy: `long-title` for the exact title, and `tel-non-breaking` for literal telephone hyphens. All other recommended rules remain enabled.
- The optional AWS deployment allowlists site files so design sources and notes are excluded. Its image pass reapplies immutable cache metadata even if image bytes are unchanged. No AWS deployment was performed. The subsequent GitHub Pages publication supplies the canonical URL; custom-domain configuration remains optional.

## GitHub Pages publication

Published September 13, 2026, at the user's explicit request:

- Public repository: [vzladude/acc-landing](https://github.com/vzladude/acc-landing), default branch `main`.
- Live site: [https://vzladude.github.io/acc-landing/](https://vzladude.github.io/acc-landing/), HTTPS enforced.
- [First successful deployment](https://github.com/vzladude/acc-landing/actions/runs/34764485244): site commit `5cf299e8f9d49be7d723fb728d16852c71b5e0a7`, completed at 15:04:27 UTC.
- `.github/workflows/pages.yml` publishes site changes pushed to `main` and supports manual dispatch. The workflow packages only the static site files and uses official GitHub actions pinned to verified release commit SHAs. Documentation-only changes do not trigger another deployment.
- Canonical, Open Graph URL, JSON-LD URL, and absolute social-image metadata point to the public Pages address. Runtime assets retain relative paths for the project subdirectory and local previews.
- Post-deployment verification: the public URL returned HTTP 200; all 22 hosted files matched their local bytes; design/specification/implementation documents correctly returned 404 on Pages. The public page was opened and visually verified in the browser, including loaded contained hero imagery, the canonical URL, and no horizontal overflow at the current 556px viewport.
- HTML validation, JavaScript syntax, Bash syntax, workflow YAML parsing, and whitespace checks passed before publication. Deployment evidence is saved in `/tmp/acc-landing-qa/artifacts/github-pages-verification.json`.

## Verification artifacts and history

Optional QA tools are installed outside the repository at `/tmp/acc-landing-qa`; they are not site dependencies.

September 13 artifacts:

- `/tmp/acc-landing-qa/refinement-artifacts/`: final full pages, target viewports, section crops, and geometry for 1440px and 390px.
- `/tmp/acc-landing-qa/artifacts/refinement-acceptance.json`: complete final functional and 1,601-width checks.
- `/tmp/acc-landing-qa/artifacts/motion-assets.json`: motion, keyboard visibility, reduced-motion, observer fallback, and asset assertions.
- `/tmp/acc-landing-qa/artifacts/lighthouse-refinement-final.report.html` and `.json`: final mobile audit.
- `/tmp/acc-landing-qa/artifacts/deploy-checks.json`: unchanged deployment-script verification.

The original implementation's reference screenshots, section comparisons, and `lighthouse-final.report.*` remain in the artifacts directory. Before these requested refinements, corresponding reference section heights matched, with zero detected Pixelmatch differences at threshold 0.1 for hero, brands, benefits, contact band, and desktop products. Its historical Lighthouse score was 99/100/100/100 at 07:01:57 UTC. These historical pixel and performance results do not describe the current refined visuals.

Temporary QA artifacts can be removed without affecting the site. `README.md` documents local use, customization, motion behavior, validation, and S3/CloudFront setup.
