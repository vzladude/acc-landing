# ACC Inversiones — Landing page implementation spec

You are implementing a production landing page for **Inversiones ACC 2018 C.A. (ACC Inversiones)**, a distributor of industrial electrical supplies and automation components in Valencia, Carabobo, Venezuela. The visual design is final and lives in this repo: open `design/reference.html` in a browser — it contains three artboards: **A-desktop (1440px)**, **A-mobile (390px)** and **A-guía** (mini style guide). Turn the design into a real, responsive, deployable static site with pixel-faithful results at those two widths and sensible behaviour in between.

All UI copy is in **Spanish** (already written in the reference — reuse it verbatim, including accents). Code, comments, commit messages, file names and documentation are in **English**.

## 1. Stack and constraints

- Plain **HTML + CSS + vanilla JS**. No frameworks, no build step, no runtime npm dependencies. Must work opened from disk and served from S3 + CloudFront.
- All asset paths **relative** (`./css/styles.css`, `./img/contactor.jpg`), never absolute `/…`.
- File layout:

```
index.html
css/styles.css
js/main.js
img/                 ← the 8 photos provided (keep the file names)
favicon.svg
robots.txt
deploy.sh            ← S3 + CloudFront deploy script (§7)
README.md            ← run locally, deploy, swap images/logo/WhatsApp number
design/reference.html   ← keep untouched, it is the source of truth
SPEC.md
```

- Fonts from Google Fonts: **Oswald 700** (headings, always uppercase) and **Poppins** 400/500/600 + italic 400/500 (body, buttons, support lines). `<link rel="preconnect">` for both hosts. Fallbacks: `Oswald, Impact, "Arial Narrow", sans-serif` and `Poppins, system-ui, sans-serif`.
- Design tokens as CSS custom properties on `:root`:
  - `--orange: #FE6102` (brand, CTA, keywords, diagonal corners), `--orange-hover: #FF7E07`, `--black: #0C0B0B` (page background), `--card: #161514`, `--product-bg: #E9E5E1` (behind product photos), `--white: #FFFFFF`, text on black uses `rgba(255,255,255,.85/.75/.62/.45)` exactly as the reference.
  - Radii: **4px** on buttons, **0** on cards (this brand is square-cornered). Borders `1px solid rgba(255,255,255,.08)`.
  - Container padding: 120px at ≥1440px, 64px tablet, 20px mobile.
  - Diagonal corners are pure CSS: `clip-path: polygon(...)` orange triangles (64px on cards, 220–300px on sections desktop, 90px mobile) — reuse one utility class with modifiers (`.corner--tl`, `.corner--br`).

## 2. Page structure (in order, with these ids)

Every section is a `<section>` with the given `id`; header and footer links anchor-scroll to them (`scroll-behavior: smooth`, `scroll-margin-top` = header height). Header is sticky, black, with the 1px bottom border, and gets a subtle shadow once scrolled.

1. `<header>` — logo (§4) left, nav **Productos · Marcas · Por qué ACC · Aprende · Contacto**, orange button "Cotiza por WhatsApp" right. Mobile: logo + hamburger (two white bars and a shorter orange third bar, as in the reference) opening a full-screen black overlay with the links and the WhatsApp button; closes on link click, Escape and close button; focus trapped; `aria-expanded`/`aria-controls` wired.
2. `#hero` — full-bleed photo `img/tablero-control.jpg` (`object-fit: cover`, `object-position: 50% 0%`; on mobile the reference scales it 1.6× from top-center) with the two gradient overlays from the reference (left-to-right and top-to-bottom), eyebrow "Suministros eléctricos industriales · Valencia", H1 "MAXIMIZAMOS LA **CONTINUIDAD** DE TU PLANTA" ("continuidad" in orange), italic paragraph, CTAs "Cotiza por WhatsApp" (orange, black text) → §5 and "Ver productos" (white outline) → `#productos`. Orange triangle bottom-right (desktop) / top-right (mobile), `aria-hidden`. Desktop hero height 800px; mobile 640px; use `min-height` + `clamp()` so the H1 (132px desktop → 58px mobile) never overflows.
3. `#productos` — H2 "PRODUCTOS **CON STOCK**" + italic side paragraph, 4-column grid (desktop) / stacked 120px-thumb rows (mobile) of product cards: image box 250px high on `--product-bg`, orange corner triangle, Oswald title, description, outline orange "Cotizar" button (→ §5 with the product-specific message). Cards data and image crops (apply the exact `transform: scale()` + `transform-origin` from the reference — the photos have Instagram text that must stay cropped out):
   - Protección eléctrica · "Breakers, interruptores de caja moldeada." · `img/breaker-caja-moldeada.jpg` · scale(1.15) origin 50% 60%
   - Control de motores · "Contactores, relés térmicos, guardamotores." · `img/contactor.jpg` · scale(1.9) origin 100% 45%
   - Sensores e instrumentación · "Sensores SICK, transmisores de presión Danfoss." · `img/transmisor-presion.jpg` · scale(2.3) origin 72% 100%
   - Automatización · "PLC, HMI, variadores de frecuencia." · `img/tablero-control.jpg` · scale(2.4) origin 50% 0%
4. `#marcas` — eyebrow "Marcas que representamos" and five dashed-border tiles with the brand names as Oswald text: Siemens · Schneider Electric · LS Electric · SICK · Danfoss (desktop: five equal tiles 84px high; mobile: wrapping chips). Leave a `<!-- TODO: replace text tiles with official brand logos (SVG) -->`.
5. `#por-que` — H2 "¿POR QUÉ **ACC**?" + italic line, then 2×2 grid of benefits with orange top border, big orange number, Oswald title, description (01 Stock local en Valencia · 02 Asesoría técnica · 03 Entregas rápidas · 04 Cotización en minutos, copy from the reference).
6. `#industria` — two columns: left text block (eyebrow "Control tradicional vs Industria 4.0", H2 "¿CUÁL ESTÁ OPERANDO **TU PLANTA**?", italic "3 señales de que necesitas automatizar tu proceso.", numbered list 01–03 with the divider lines); right column is the reference's photo placeholder → use `img/tecnico-planta.jpg` with `object-fit: cover`, `object-position: 60% 100%`, the left-to-right black gradient and the orange triangle bottom-right. Orange triangle top-left of the section. On mobile the photo (260px) goes above the text, as in A-mobile.
7. `#aprende` — H2 "APRENDE CON **ACC**" + link "@accinversiones →" (Instagram). Three 4:5 cards linking to Instagram: "¿Qué es realmente un breaker?" `img/breaker-negro.jpg` · "¿Qué es un contactor y por qué tu motor lo necesita?" `img/contactor.jpg` · "¿Qué es un relé térmico?" `img/rele-termico.jpg`; each with "Ver en Instagram →". Mobile: 120px-thumb rows.
8. `#contacto` — orange band "COTIZA AQUÍ TU REQUERIMIENTO" + italic "Respuesta en minutos por WhatsApp.", then two columns: contact grid (WhatsApp 0412-5003831 · Correo attcliente2018@gmail.com · Teléfonos 0412-5003831 / 0412-7480335 · Horario Lun–Vie 8:00–17:00 · Ubicación Valencia, Carabobo, Venezuela) with the big orange "Escríbenos por WhatsApp" button, and the map card: a Google Maps **Embed** `<iframe>` (no API key) at `https://www.google.com/maps?q=Inversiones+ACC+2018+Valencia+Carabobo&output=embed`, `loading="lazy"`, `title="Ubicación de ACC Inversiones"`, `referrerpolicy="no-referrer-when-downgrade"`, 440px high desktop / 200px mobile, 1px border like the reference. Email is a `mailto:` link; phones are `tel:+58412…` links.
9. `<footer>` — logo, the five nav links, "@accinversiones" (Instagram), "© Inversiones ACC 2018 C.A. · Valencia, Carabobo, Venezuela" with the year rendered by JS (fallback 2026).

## 3. Responsive rules

- Desktop reference 1440px; mobile 390px; match both closely (spacing, sizes, colours, type scale). Fluid type with `clamp()`; tablet breakpoint (~768–1024px): product grid 2 columns, benefits 2 columns, `#industria` stacked, container padding 64px.
- No horizontal page scroll at any width from 320px to 1920px. Above 1440px keep content in a centered 1440px max-width container while backgrounds and hero photo stay full-bleed.
- Respect `prefers-reduced-motion`.

## 4. Logo

No vector logo yet. Reproduce the reference logotype as **one reusable inline SVG** `<symbol id="logo">` used in header and footer: "ACC" in Oswald 700 orange with a thin black horizontal bar across the middle (the reference draws it as a 3px black line at 47% height — emulate the "connector" cut) and "INVERSIONES" in tiny white letter-spaced caps beneath. Add `<!-- TODO: replace with official ACC vector logo -->`. `favicon.svg`: black square with the orange "ACC" mark.

## 5. WhatsApp CTAs

- Number: 0412-5003831 → `https://wa.me/584125003831?text=<url-encoded>`.
- Default message (header, hero, contact, mobile menu): `Hola ACC, quiero cotizar un requerimiento para mi planta.`
- Product "Cotizar" buttons: `Hola ACC, quiero cotizar: <nombre de la categoría>.`
- Instagram: `https://www.instagram.com/accinversiones/`. External links `target="_blank" rel="noopener"`.

## 6. JavaScript (`js/main.js`)

Dependency-free IIFE with one `CONFIG` object at the top:

```js
const CONFIG = {
  whatsappNumber: '584125003831',
  whatsappDefaultMessage: 'Hola ACC, quiero cotizar un requerimiento para mi planta.',
  whatsappProductMessage: (name) => `Hola ACC, quiero cotizar: ${name}.`,
  instagramUrl: 'https://www.instagram.com/accinversiones/',
  mapsQuery: 'Inversiones ACC 2018 Valencia Carabobo',
};
```

Responsibilities: build every WhatsApp href from `CONFIG` (HTML keeps a static href as no-JS fallback), mobile menu open/close + focus trap, header shadow on scroll, footer year, set the map iframe `src` from `CONFIG.mapsQuery`. Nothing else, no analytics.

## 7. Deploy script (`deploy.sh`)

Bash, driven by `S3_BUCKET` and `CLOUDFRONT_DISTRIBUTION_ID` env vars (fail fast with a clear message if missing). `aws s3 sync . s3://$S3_BUCKET --delete` excluding `.git/*`, `design/*`, `SPEC.md`, `deploy.sh`, `README.md`; `--cache-control "max-age=31536000, immutable"` for `img/*`, `--cache-control "max-age=300"` for html/css/js; then `aws cloudfront create-invalidation --paths "/*"`. README documents bucket setup (no static website hosting, CloudFront OAC, default root object `index.html`) and the custom-domain step (Route 53 hosted zone + ACM certificate in us-east-1 + alias record) as a TODO.

## 8. SEO, accessibility, performance

- `<html lang="es">`, `<title>ACC Inversiones — Suministros eléctricos industriales en Valencia, Carabobo</title>`, Spanish meta description (~150 chars), Open Graph + Twitter tags (image `img/tablero-control.jpg`), `<!-- TODO: canonical when domain is known -->`.
- JSON-LD `LocalBusiness`: name "Inversiones ACC 2018 C.A.", telephone `+584125003831`, email, address Valencia / Carabobo / VE, openingHours `Mo-Fr 08:00-17:00`, `sameAs` Instagram.
- Landmarks, heading hierarchy H1 → H2 → H3, Spanish `alt` text, visible focus styles (orange outline on black), contrast ≥ 4.5:1 for body text (`rgba(255,255,255,.62)` on `#0C0B0B` passes; black text on orange buttons passes).
- Images: `width`/`height` attributes, `loading="lazy"` below the hero, `decoding="async"`; do not re-encode the JPEGs. `robots.txt` allowing everything.

## 9. Acceptance criteria (verify before finishing)

1. Screenshots at 1440×900 and 390×844 match `design/reference.html` section by section (the only allowed differences: the live map and the real photo in `#industria`).
2. No horizontal overflow at 320, 390, 768, 1024, 1440, 1920 px.
3. `npx html-validate index.html` passes; no console errors or 404s.
4. Lighthouse (mobile) ≥ 90 in Performance, Accessibility, Best Practices, SEO.
5. Keyboard-only: mobile menu opens/closes, Escape closes it, every link and button reachable.
6. Every CTA opens the correct `wa.me` URL with the prefilled text; nav anchors land on the right section with the header not covering the heading.
7. `bash -n deploy.sh` passes and it refuses to run without the two env vars.

Commit in small conventional commits (`feat: hero section`, …). When everything passes, write `IMPLEMENTATION_NOTES.md` listing any deviation from the reference and why.
