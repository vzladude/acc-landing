# Asset notes

Updated September 13, 2026, following the user's request for contained images, ImageGen surroundings, real brand logos, and professional motion.

## Image treatment

All foreground images use `object-fit: contain` without crop transforms. Generated background textures fill the remaining wrapper area. The full source posts remain visible in product and Instagram cards. Hero and technician photographs use cleaned ImageGen derivatives so promotional overprints do not compete with the page headings. Generative editing reconstructs details, so these two derivatives are illustrative edits rather than untouched documentary photographs. All eight supplied JPEGs remain byte-for-byte unchanged.

Generation mode: **built-in ImageGen**, using local image references. No CLI or external image-generation API was used. PNG masters remain in `/Users/josegregorioflores/.codex/generated_images/01a0997e-519b-74b1-99c6-ce331149944c/`. Optimized WebP copies are stored in this repository at the paths below. Compression used `cwebp` on generated assets only (quality 78/76/82/80 respectively); the studio and technician derivatives were also resized. CSS backgrounds are decorative and do not replace meaningful image alt text.

## Brand logo provenance

The logos are locally hosted authentic artwork, not generated lettering. Each has a descriptive Spanish-accessible brand name in `alt`, explicit dimensions, and lazy loading. Brand artwork remains the property of its respective owner.

| Brand | Saved file | Source and processing |
| --- | --- | --- |
| Siemens | `img/brands/siemens.svg` | [Wikimedia source record](https://commons.wikimedia.org/wiki/File:Siemens_AG_logo.svg), [SVG download](https://upload.wikimedia.org/wikipedia/commons/3/3c/Siemens_AG_logo.svg). Source record attributes the artwork to Siemens AG. CSS renders a white silhouette on the dark tile. |
| Schneider Electric | `img/brands/schneider-electric.svg` | [Wikimedia source record](https://commons.wikimedia.org/wiki/File:Schneider_Electric_2007.svg), [SVG download](https://upload.wikimedia.org/wikipedia/commons/9/95/Schneider_Electric_2007.svg). Source record traces the vector to the company's 2007 annual report. CSS renders a white silhouette. |
| LS Electric | `img/brands/ls-electric.png` | [Official website header PNG](https://www.ls-electric.com/assets/img/common/logo1.png), discovered in the site's header bundle. Preserved as supplied, displayed in white using CSS. |
| SICK | `img/brands/sick.svg` | Exact path and polygon geometry extracted from the `cms-footer-logo` component in the [official website bundle](https://www.sick.com/_ui/webcc/prod/7c289a4f/standalone/main-AZ4IH7T5.js). Wrapped in a standalone SVG, retaining the white wordmark and “Sensor Intelligence” tagline. No tracing or generated replacement. |
| Danfoss | `img/brands/danfoss.svg` | [Official website SVG](https://www.danfoss.com/static/images/new-logo.svg). Preserved in its native red and white; no monochrome filter, which would erase the lettering against its red field. |

## Exact ImageGen prompts

### Industrial surround

- Saved asset: `img/backgrounds/industrial-surround.webp` (1536×1024).
- References: `img/tablero-control.jpg`.
- Master: `exec-f8219e6c-ebcb-4999-87b6-17ed7aec9d5d.png` in the generation directory above.

```text
Use case: photorealistic-natural. Asset type: seamless contextual background for the empty side margins around contained industrial photos on ACC Inversiones' black landing page. Input image is a STYLE AND ENVIRONMENT REFERENCE ONLY, not an image to reproduce. Generate a wide 1536x1024 photorealistic continuation environment: dark industrial electrical control cabinet interior, understated steel DIN rails, tidy orange and charcoal wiring, terminal blocks at the far outer edges. The central 55% should be very quiet near-black with softly defocused industrial depth, because a full, unaltered original photo will be layered over it. Match the reference's charcoal blacks, warm subdued industrial lighting and perspective. The far left and right edge detail must be natural, subtle, and unobtrusive, blending toward near-black #0C0B0B. No readable letters, no text, no slogans, no logos, no watermark, no person or hand, no prominent isolated product. Do not recreate or alter a branded component. Produce only the background photographic asset, not a website screenshot or a collage.
```

### White studio surround

- Saved asset: `img/backgrounds/studio-surround.webp` (960×640).
- References: `img/breaker-caja-moldeada.jpg`.
- Master: `exec-e51b76e0-8785-47fd-9664-d6703a18e163.png` in the generation directory above.

```text
Use case: product-mockup. Asset type: a neutral photographic extension background for the empty side margins around a contained industrial product photograph. Input image is a LIGHTING AND BACKGROUND REFERENCE ONLY. Generate a wide 1536x1024 completely empty white product photography studio surface, matching the attached Siemens breaker post's clean white seamless backdrop. White-to-very-light warm gray at the extreme bottom edge with a faint real photographic contact-plane texture, soft diffuse lighting, no visible horizon. Center and upper 90% should be almost pure white, corners clean. This will sit behind the original unaltered breaker photo, so preserve an empty, neutral composition that merges naturally with its white edges. No product, no object, no shadows from imaginary objects, no text, no letters, no ACC mark, no Siemens logo, no orange triangle, no watermark. Only the quiet photographic background, not a website mockup.
```

### Clean, extended hero

- Saved asset: `img/hero-control-extended.webp` (1536×1024).
- References: `img/tablero-control.jpg; generated industrial surround PNG`.
- Master: `exec-ae3ba076-1451-4af1-b4ee-a66b15ee0a1c.png` in the generation directory above.

```text
Use case: precise-object-edit. Asset type: professional industrial landing-page hero photo, 1536x1024 landscape. Input image 1 is the EDIT TARGET. Input image 2 is SUPPORTING BACKGROUND STYLE only. Primary request: remove only the overlaid advertising text, orange/black ACC logo, and watermark-like graphic elements from input 1 and reconstruct the photographic scene behind them. Preserve the original electrical control cabinet, breakers, wiring, gloved hand, sleeve, perspective, and photographic lighting. Keep any tiny labels physically printed on the actual equipment, but do not add or invent new readable equipment labels. Expand/outpaint the original portrait photo to a wide landscape composition: preserve the entire original scene at full height on the RIGHT, extend the empty industrial cabinet environment naturally to the LEFT, using input 2's dark charcoal industrial depth. No crop or zoom into the original subject. Left 55% should be quiet dark photographic negative space for large HTML headlines, with subdued rails and wiring disappearing into black. Preserve photo realism and natural scale. Right side retains the authentic gloved hand reaching toward the control cabinet. No advertising text, no headline, no logos overlaid on the photo, no watermark, no new person, no duplicate arm. Output only the finished clean extended photograph, not a website mockup.
```

### Clean technician photo

- Saved asset: `img/technician-clean.webp` (800×1000).
- References: `img/tecnico-planta.jpg`.
- Master: `exec-444b19ee-c010-4947-9de3-8f90df6f7732.png` in the generation directory above.

```text
Use case: precise-object-edit. Asset type: clean professional industrial website photograph, portrait 1024x1280. The attached image is the EDIT TARGET. Remove only the advertising overlays: all large promotional lettering at the top, the italic promotional lettering in the lower middle, and the orange/black ACC logo at the bottom. Reconstruct the real photographic scene behind those overlays seamlessly. Preserve the full original composition without cropping or zooming: the technician viewed from behind wearing a hard hat and gray work shirt, their original pose and arm reaching toward the electrical cabinet touchscreen, the electrical cabinet equipment, workshop background, perspective, and natural lighting. Keep the person's face turned away as in the original. Preserve tiny equipment markings that belong physically to the machinery, but do not invent new readable labels. Extend small missing areas only as needed to keep the entire subject and cabinet within the portrait frame. Photorealistic, precise and understated, matching the original photograph. No new person, no duplicate limbs, no advertising text, no large letters, no added logos, no watermark. Output only the cleaned photograph, not a mockup, poster, or website.
```

