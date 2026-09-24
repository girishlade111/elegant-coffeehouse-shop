# Flavored — Elegant Coffeehouse Landing Page

A single-page, pixel-faithful landing page for **Flavored**, an elegant coffeehouse brand.
Built with pure **Astro** (static output, no UI framework, no Tailwind), hand-written CSS,
and **~0.9 KB of gzipped client JavaScript**.

> *Coffee — the best for you.* Freshly roasted beans, lattes, and a menu you can order
> from the app — presented in a warm, glassmorphic single-page experience.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Available Scripts](#available-scripts)
- [Project Structure](#project-structure)
- [Swapping the Cup Images](#swapping-the-cup-images)
- [Changing the Copy or Currency](#changing-the-copy-or-currency)
- [Design Tokens](#design-tokens)
- [Interactivity](#interactivity)
- [Performance & Measured Results](#performance--measured-results)
- [Deployment](#deployment)
- [Notes](#notes)
- [License](#license)

---

## Features

- **Pure Astro, zero framework overhead** — no React/Vue/Svelte, no Tailwind; every
  component is a scoped `.astro` file with hand-written CSS.
- **Seven-section landing page** — Navbar, Hero, Product Showcase, Feature Spotlight,
  App Section (with phone mockups), Reserve CTA, and Footer.
- **Single source of truth for copy** — every string, price, link, and JSON-LD field
  lives in `src/data/site.ts`; no copy is hard-coded in components.
- **Fluid, responsive layout** — `clamp()`-based type scale and spacing hold from
  360 px to 1920 px with zero horizontal scrolling.
- **Glassmorphic shell** over a fixed coffee-bokeh backdrop with a CSS gradient
  fallback if the image is missing.
- **~0.9 KB gzipped client JS** — scroll reveals via `IntersectionObserver`, hero float,
  heart toggle, cart bounce, and mobile menu; all vanilla TypeScript.
- **Scroll-driven bean parallax** using `animation-timeline: view()` behind
  `@supports`, so it degrades gracefully where unsupported.
- **SEO & accessibility built in** — OG meta, canonical, JSON-LD (`CafeOrCoffeeShop`),
  sitemap integration, skip link, `aria-pressed` / `aria-live` announcements,
  contrast ratios of 9.1:1–19.5:1.
- **Optimized images** — `astro:assets` emits AVIF with WebP fallback at 1x/2x;
  the hero cup is `loading="eager"` + `fetchpriority="high"`.
- **Self-hosted fonts** — Roboto 400/500/700 via `@fontsource/roboto`; nothing is
  fetched from a CDN.

---

## Tech Stack

| Layer | Choice |
| --- | --- |
| Framework | [Astro](https://astro.build) 7 (static output) |
| Language | TypeScript 5.9, Astro components, vanilla CSS |
| Integrations | `@astrojs/sitemap` |
| Fonts | `@fontsource/roboto` (self-hosted) |
| CSS minify | Lightning CSS (via Vite) |
| Asset pipeline | `astro:assets` — AVIF + WebP responsive images |
| Client JS | Vanilla TypeScript in `<script>` tags (~0.9 KB gzipped) |
| Asset generation (optional) | Python + Pillow + NumPy (`scripts/generate-assets.py`) |

---

## Prerequisites

- **Node.js** 18.17+ (20 LTS recommended)
- **npm** 9+ (comes with Node)
- Optional: **Python 3** with `Pillow` and `NumPy` if you want to regenerate the
  placeholder artwork

---

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/elegant-coffeehouse-shop.git
cd elegant-coffeehouse-shop

# 2. Install dependencies
npm install

# 3. Start the dev server (http://localhost:4321)
npm run dev
```

---

## Available Scripts

| Script | What it does |
| --- | --- |
| `npm run dev` / `npm start` | Dev server with HMR at `http://localhost:4321` |
| `npm run build` | Static production build into `dist/` |
| `npm run preview` | Serve the built `dist/` locally |
| `npm run check` | `astro check` — type-checking + template diagnostics |
| `npm run astro` | Pass any CLI command directly to Astro |

---

## Project Structure

```
├── public/
│   └── favicon.svg                 static favicon
├── scripts/
│   └── generate-assets.py          regenerates placeholder art (Pillow + NumPy)
├── src/
│   ├── assets/
│   │   ├── bg/coffee-bokeh.jpg     fixed backdrop behind the glass shell
│   │   └── cups/*.png              drink artwork (swap freely — see below)
│   ├── components/                 one .astro file per section, styles scoped
│   │   ├── Navbar.astro            sticky glass navbar + mobile menu
│   │   ├── Hero.astro              headline, chips, floating hero cup
│   │   ├── ProductShowcase.astro   #menu section
│   │   ├── ProductCard.astro       glass / cream product cards
│   │   ├── FeatureSpotlight.astro  #about section with bean scatter
│   │   ├── AppSection.astro        "App is Available" + store buttons
│   │   ├── PhoneMenu.astro         left phone mockup screen
│   │   ├── PhoneDetail.astro       right phone mockup screen
│   │   ├── ReserveCTA.astro        #contact reserve-a-table CTA
│   │   ├── Footer.astro            footer columns + bean spill
│   │   ├── Icon.astro              inline SVG icon set
│   │   ├── Cup.astro               PNG-first cup with SVG fallback
│   │   ├── CupArt.astro            pure inline SVG cup variants
│   │   ├── BeanScatter.astro       deterministic bean positions
│   │   └── Logo.astro              brand wordmark
│   ├── data/
│   │   ├── site.ts                 ALL copy, prices, links, footer, JSON-LD
│   │   └── beans.ts                bean scatter positions (fixed literals)
│   ├── layouts/
│   │   └── BaseLayout.astro        <head>, SEO/OG meta, fonts, backdrop, shell
│   ├── pages/
│   │   └── index.astro             the page; the seven sections in order
│   └── styles/
│       ├── tokens.css              design tokens (colour, type scale, canvas)
│       └── global.css              reset, base type, backdrop, shell
├── astro.config.mjs                Astro config (static, sitemap, image opts)
├── tsconfig.json                   TypeScript config
├── package.json
└── .gitignore                      ignores node_modules/, dist/, .astro/, etc.
```

---

## Swapping the Cup Images

Drop a replacement PNG into `src/assets/cups/` using the **same filename** and it is
picked up automatically at build time — no code change needed.

| File | Used by | Suggested framing |
| --- | --- | --- |
| `hero-heart.png` | Hero cup (the LCP element) | Top-down latte on a saucer, square, saucer ≈ 96% of the canvas |
| `rosetta-large.png` | Feature spotlight | Top-down latte, square, crema ≈ 94% of the canvas |
| `americano.png` | Product card 1 | Square, cup centred |
| `cappuccino-bear.png` | Product card 2 | Square, cup centred |
| `latte-small.png` | Compact/thumbnail slots | Square, cup centred |

Use square, transparent-background PNGs at **900×900** (large slots) or **640×640**
(cards). The components read the image's intrinsic size, so any resolution works, but
keeping the cup centred and the saucer touching the canvas edges keeps the layout
identical to the reference.

`Cup.astro` looks for a matching PNG first and falls back to `CupArt.astro` (pure
inline SVG) if the file is absent — so deleting a PNG degrades gracefully instead of
breaking the page.

To regenerate the shipped placeholders:

```bash
python scripts/generate-assets.py     # needs Pillow + NumPy
```

---

## Changing the Copy or Currency

Everything readable lives in **`src/data/site.ts`** — nav labels, hero heading and
chips, product names/prices, the feature blurb, app copy, the reserve CTA, the footer
columns, and the JSON-LD. No copy is hard-coded in components.

Prices are numbers, formatted in one place:

```ts
// src/data/site.ts
const usd = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
export const formatPrice = (n: number) => usd.format(n);
```

To switch currency, change those two lines — e.g. `currency: 'EUR'` with `'de-DE'`,
or `currency: 'INR'` with `'en-IN'`. Every price on the page follows.

---

## Design Tokens

`src/styles/tokens.css` holds the measured page canvas and the type scale. The values
were read off the reference artboard at a **1440 px** viewport:

| Token | Value | Notes |
| --- | --- | --- |
| `--page-max` | `1232px` | shell width; it spans x 104–1336 |
| `--shell-pad-x` | `clamp(20px, 7.31vw, 105px)` | content starts at x 209 |
| `--shell-pad-y` | `clamp(28px, 4.6vw, 66px)` | shell top edge at y 96 |
| `--fs-h1` | `clamp(40px, 4.4vw, 64px)` | hero heading |
| `--fs-h2` | `clamp(24px, 2.5vw, 36px)` | with `--lh-h2: 1.16` |
| `--espresso-900` | `#1f0404` | headings + button fills |

Fluid values are `clamp()` throughout, so the layout holds from 360 px to 1920 px with
no horizontal scrolling.

---

## Interactivity

All vanilla TypeScript inside Astro `<script>` tags — no framework, no islands, no
hydration directives.

- **Scroll reveal** via `IntersectionObserver` with an 80 ms stagger. Content is fully
  visible with JS disabled; the script only adds the transition.
- **Hero cup float**, button hover/press, **heart toggle** (`aria-pressed`), **cart
  bounce** with an `aria-live="polite"` announcement, and **mobile menu**.
- **Bean parallax** uses `animation-timeline: view()` behind `@supports`, so it is
  simply absent where scroll-driven animations are unsupported.

---

## Performance & Measured Results

Verified on the production build:

| Check | Result |
| --- | --- |
| `astro check` | 21 files — 0 errors, 0 warnings, 0 hints |
| Client JS | **0.9 KB gzipped** (budget: 5 KB) |
| LCP (mobile, 4× CPU, Slow 4G) | **1.22 s** (budget: < 2.0 s) |
| CLS | **0** |
| Accessibility audit | all checks pass; contrast 9.1:1–19.5:1 |
| Horizontal overflow | none at 360 / 390 / 414 / 600 / 768 / 900 / 1024 / 1280 / 1440 / 1920 |

---

## Deployment

The build is fully static — deploy by uploading the `dist/` folder to any static host.

```bash
npm run build     # outputs to dist/
```

Examples:

- **Netlify / Vercel / Cloudflare Pages** — build command `npm run build`,
  publish directory `dist`
- **GitHub Pages** — push `dist/` to the `gh-pages` branch or use an action
- **Any web server** — copy `dist/` to your web root

Remember to set the real site URL in two places after you have a domain:

1. `astro.config.mjs` → `site: 'https://your-domain.com'`
2. `src/data/site.ts` → `site.url` (and the JSON-LD `url`)

---

## Notes

- Fonts are self-hosted via `@fontsource/roboto` (400/500/700, latin subset).
  Nothing is fetched from a CDN.
- Images go through `astro:assets`, emitting AVIF with a WebP fallback at `1x`/`2x`.
  The hero cup is `loading="eager"` + `fetchpriority="high"`; everything else is lazy.
- The bokeh backdrop has a CSS gradient fallback stack, so the page still reads
  correctly if `coffee-bokeh.jpg` is missing.
- The shipped cup artwork and backdrop are **procedurally generated placeholders**.
  Replace them with real photography before going live.
- `node_modules/`, `dist/`, `.astro/`, `.env*`, and local scratch folders are
  excluded via `.gitignore`.

---

## License

All rights reserved unless otherwise noted. Replace this section with your preferred
license (e.g. MIT) before publishing if you intend to open-source the project.
