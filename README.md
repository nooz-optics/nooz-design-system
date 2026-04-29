# Nooz Optics Design System

A design system for **Nooz Optics** (nooz-optics.com) — a French-founded international eyewear brand selling reading glasses, sunglasses, blue-light glasses and accessories across 20+ countries.

## Brand at a glance

- **Product**: Affordable, design-forward optical & sun eyewear. Categories include Reading, Sun, Bluelight, Kids, Sport, Reading‑Sun (polarized readers), Reading‑Degressive (progressives), and seasonal collections (e.g. Club House SS26, Original).
- **Channels**: E-commerce (Shopify Storefront), retail stores with in-store appointments (Odoo POS), CMS-driven marketing site (Contentful).
- **Markets**: EU, UK, US, CA, AU, NZ, SG — 18 site locales, 10 Contentful locales.
- **Tone**: International, friendly, utilitarian. Product copy is direct and informative; marketing leans warm and confident without being salesy.
- **Identity**: Resolutely **angular** — 0px border radius on buttons/cards/images is a deliberate brand choice. Quasi-flat: shadows are barely perceptible (`rgba(0,0,0,0.05)` max). The palette pairs warm terracota `#DC693B` with cream `#FCFAFA` background and deep grey text — never pure black for body copy.

## Products represented

Only one codebase was provided, covering the **public e-commerce website** (`nooz-web/`). This is a Next.js 15 + React 19 app with:
- Product listings, product detail pages (with optical/sun lens configurators)
- Cart drawer, checkout (redirect to Shopify checkout)
- Blog, help center, retail shop finder, in-store booking flow
- "Magic Mirror" virtual try-on
- B2C (default) and B2B (`NEXT_PUBLIC_APP_NAME=B2B`) variants

No dedicated mobile app, admin UI, or separate marketing site was included.

## Sources

- **Codebase (read-only mount)**: `nooz-web/` — Next.js 15 App Router, Mantine 7, CSS Modules, TypeScript 5, next-intl 4, Zustand 5. Production site: https://www.nooz-optics.com
- **Design-system rules file**: `nooz-web/.cursor/rules/design-system.mdc` — auto-extracted from the production site on 2026-04-12.
- **Theme source**: `nooz-web/src/styles/NoozTheme.ts` — Mantine theme with all color tokens.
- **Global CSS**: `nooz-web/src/styles/app.css` — container paddings, header theming, card default.
- **Fonts**: `nooz-web/public/fonts/` — Mont (Light / Regular / Semibold / Bold — OTF).
- **Logos**: `nooz-web/public/assets/logo/` — black, white, pro, PNG.
- **Component library**: `nooz-web/src/components/{atoms,molecules,organism,template,layouts}/` — atomic-design folder structure.
- **Copy examples**: `nooz-web/messages/en-us.json` and 19 other locale files.

No Figma was attached. Screenshots of production UI were not attached — components in this system were built by reading the source code (Mantine component props, CSS modules) and cross-referencing the auto-extracted design-system rules.

---

## Content fundamentals

### Voice & tone

Nooz copy is **direct, warm, plainspoken**. It reads like a knowledgeable friend, not a luxury brand. It informs before it sells.

- **Casing**: Sentence case for everything except proper nouns and the brand name. Navigation labels are sentence-case too ("Reading glasses", not "READING GLASSES" or "Reading Glasses"). The category pill/filter chips often use lower/sentence case.
- **Person**: Primarily **you/your**. "Your booking", "Your gift", "Find us", "Select your gift". First-person "we" appears rarely, reserved for brand/story pages.
- **Punctuation**: French typography conventions bleed through — a non-breaking space is inserted before `?`, `!`, `:`, `;`, `.` (see `cleanText()` in `atoms/Text`). Titles rarely end in a period.
- **Microcopy examples** (from `messages/en-us.json`):
  - CTAs: "Discover the collection", "Checkout", "Cancel", "Confirm", "Filter", "Reset filters", "Show more"
  - Product states: "In stock", "Pre-order", "Sold out", "additional articles"
  - Forms: "First name & last name" (placeholder), "Enter your contact details"
  - Promotions: "Your gift", "Free Shipping"
  - Help/booking: "Find us", "Your Booking", "Add to calendar", "Select date and time"
- **No emoji** in product or marketing copy. Icons carry the visual burden.
- **Numbers & units**: Localised; prices show the whole-number portion in heavier weight and the decimal part in muted grey (`--nooz-decimal` `#8D8D8D`, weight 100) — e.g. **19**<span style="color:#8D8D8D;font-weight:100">.95 €</span>.
- **Localisation reality**: Some strings are untranslated (e.g. an English key sometimes contains a French fallback — "Votre demande a bien été pris en compte."). This is a quirk of Contentful pulls; don't mimic it — use the target locale only.

### Vibe

International e-commerce with French sensibility. Never "luxury", never "tech". Think: a well-run optical boutique that ships worldwide. Minimal hype, lots of product clarity.

---

## Visual foundations

### Colors
- **Primary**: Terracota `#DC693B` — used for CTAs, anchor links, accents. **Not** a brand logo color; the logo is **black on cream**.
- **Background**: `#FCFAFA` cream — the signature canvas. Pure white is for cards / surfaces on top of cream.
- **Text**: `#585858` body, `#2D2D2D` titles. Nooz avoids pure black for running copy.
- **Category colors** encode product type (sun yellow, reading burgundy, bluelight blue, kids orange, sport green, etc.) — used as pastille dots, section headers on PLPs, and badge backgrounds. They come from the CMS; never hardcode them.
- Accents are single-color; **no gradients** in default UI. The only gradient in the theme is a developer-default for `Text variant="gradient"` (rarely used).

### Typography
- One family everywhere: **Mont** (custom, OTF). Weights shipped: 100 (Light), 300 (Regular), 500 (Semibold), 700 (Bold). The theme references 900 (Black) but no 900 file exists — it falls through to 700.
- Body defaults to **14px / weight 400 / line-height 1.55**. The Mantine root is 16px but `<Text>` is explicitly 14.
- Scale: 10, 11, 12, 13, 14, 18, 24, 28, 34, 42, 70px. Don't invent in-between sizes.
- Headings use weight **500** (display) or **600** (card titles). The "heavy display" moments go to **900** (which renders as 700).

### Backgrounds
- No full-bleed hero imagery as default — the PLP/home is mostly cream with product imagery on cream tiles.
- Product media tiles have a warm off-white **`#F1ECEE`** behind images to avoid harsh contrast.
- **No textures, grain, or hand-drawn illustrations.** Imagery is clean product photography (warm, natural light) and lifestyle shots.
- **No patterns** except optional category color blocks in CMS-authored sections.

### Animation
- Minimal. Hover is `opacity 0.4s ease` on buttons (**not** a color change). Header slides on scroll `top 0.7s ease-out`.
- Framer Motion is installed but used sparingly for drawers and product carousels. No bouncy easings, no scroll-linked parallax, no confetti.
- Transitions are functional, not decorative.

### Hover states
- Buttons, links, tiles: **`opacity: 0.7`** on hover. Return to `opacity: 1` on focus.
- Cards have no hover by default (some surfaces change cursor to pointer — that's it).
- Color changes on hover are reserved for nav links (`--header-nav-link-hover: terracota`).

### Press / active states
- No explicit scale or shrink animation. The `opacity` drop functions as the press affordance.

### Borders
- Default border: `1px solid var(--mantine-color-gray-4)` (`#CED4DA`) from Mantine.
- Dividers inside header/menu use `rgba(222, 226, 230, 1)` in light mode, `rgba(255,255,255,0.2)` in dark mode.
- No heavy or colored borders anywhere; dimmed grey or nothing at all.

### Shadow system
- Near-zero shadow culture. The house card shadow is **`0px 0px 10px rgba(0,0,0,0.05)`**. An alternate is `0px 4px 10px rgba(0,0,0,0.02)` (per `.card` in `app.css`).
- Dropdowns / popovers: a stacked Mantine `lg`/`xl` shadow but still `0.05` max opacity.
- Color-pickers use **inset shadow** for the "pressed" affordance: `inset 0 0 0 1px rgba(0,0,0,0.1), inset 0 0 4px rgba(0,0,0,0.15)`.
- **Never exceed `rgba(0,0,0,0.05)` for outer shadow.**

### Protection gradients / capsules
- **No protection gradients** over imagery. Text is either placed against plain cream/white, or against a solid color block (category color).
- Badges are flat pill capsules (`border-radius: 100px`) with solid fills — e.g. `original` red pill for "NEW". No glow, no gloss.

### Layout rules
- Fixed header at the top: z-index `99999`, hides on scroll-down / shows on scroll-up (`top 0.7s ease-out`).
- Header comprises 3 strips: banner (30px) → nav bar (60px) → sub (40px). Total ~130px reserved.
- Footer is always **black** (`#000000`) with white text — 4-column desktop, stacking on mobile.
- Content containers use **64 / 32 / 16 px** horizontal padding at desktop / tablet / mobile. **No max-width** — content fills the viewport.
- Modals/drawers take z-index `99990`. Mobile drawer has `border-radius: 30px 30px 0 0` on its top edge.

### Transparency & blur
- **No backdrop-filter blur anywhere.** Surfaces are opaque.
- Light colorized overlays (`rgba(<color>, 0.1)`) are used for `button.variant="light"` fills — subtle tinted chips.

### Imagery color vibe
- Warm, daylight, natural. Neutral studio backgrounds (often the `#F1ECEE` warm off-white). No cool tones, no heavy B&W, no grain, no heavy filter.
- Lifestyle shots feature real people wearing the product, generally mid-shot, good light.

### Corner radii
- **0px everywhere** — buttons, cards, inputs, images. This is Nooz's core identity gesture.
- Exceptions are intentional and deliberate:
  - `4px` — some Mantine input defaults (kept conservative)
  - `8px` — pickers, cookie banner, diopter modals
  - `14px` — selection cards
  - `20px` — ClearCard / ReviewClearCard (editorial marketing cards)
  - `30px 30px 0 0` — bottom-sheet mobile drawer
  - `100px` — pill badges (breadcrumbs, cart count)
  - `50%` — color dots, avatars
- **If it's not one of the above, it's 0.**

### Cards
- Flat, white, 0 radius, `shadow-card`, `padding: 0` (content provides its own padding), `cursor: pointer` when clickable.
- No borders on default cards.

---

## Iconography

- **Icon system**: [**Tabler Icons**](https://tabler.io/icons) via `@tabler/icons-react` (v3.21). Stroke icons at `stroke: 1.5`, default size `16px`.
- The codebase ships no custom icon font or SVG sprite. Icons are imported by name (e.g. `IconShoppingBag`, `IconUser`, `IconSearch`, `IconChevronDown`, `IconMenu2`, `IconMapPin`, `IconCalendar`, `IconHeart`) and rendered through `<Icon iconKey="..." />` which looks up `TablerIcons[`Icon${iconKey}`]`.
- **SVG assets shipped**: only a small set of decorative/utility SVGs — the Nooz logo (black/white/pro), a newsletter envelope (`newsletter.svg`), and a pupillary-distance overlay (`pd-overlay.svg`). Country flag SVGs live in `public/assets/flags/`.
- **Unicode / emoji**: **Not used.** No emoji in product copy, no unicode icons anywhere in the components.
- **Color handling**: icons default to the `text` color token (`#585858`). When Contentful supplies a hex, it wins.
- In this design system we link Tabler Icons from CDN (same package, pinned version) — same stroke/size defaults as production.

---

## Index (manifest)

| File / folder | What it is |
|---|---|
| `README.md` | (this file) overview, content + visual + icon fundamentals |
| `SKILL.md` | Skill manifest — load this to get an agent ready to design for Nooz |
| `colors_and_type.css` | CSS variables + semantic classes for color, type, spacing, radii, shadows |
| `fonts/` | Mont OTFs (light / regular / semibold / bold) |
| `assets/` | Logos (black / white / pro / png), newsletter & PD overlay SVGs |
| `preview/` | HTML cards that populate the Design System review tab |
| `ui_kits/web/` | High-fidelity recreation of the Nooz marketing + PDP web UI |

### UI kits

- **`ui_kits/web/`** — single kit. Covers header / nav, category grid, product card, product detail page, footer, cart drawer. `index.html` shows an interactive click-thru.

No slide template was provided — no `slides/` folder is shipped.
