# Nooz Design Tokens

`nooz.tokens.json` — design tokens au format **W3C Design Tokens Community Group (DTCG)**. Compatible avec :

- **Figma Tokens Studio** (plugin officiel) — import direct du JSON
- **Style Dictionary** (CLI Amazon) — génère CSS / SCSS / Swift / Android / Tailwind
- **Tokens Studio CLI** — sync GitHub ↔ Figma en continu
- Les outils de design sync modernes (Specify, Supernova)

---

## Usage

### 1 · Figma Tokens Studio (le plus simple)

1. Dans Figma : Plugins → **Tokens Studio for Figma** → Run
2. Settings → Sync providers → **JSON (local file)** ou **GitHub**
3. Import `tokens/nooz.tokens.json`
4. Applique les tokens aux layers Figma — les styles deviennent liés à ce fichier

Mise à jour : rééxécute le plugin après chaque pull pour propager les changements.

### 2 · Style Dictionary (pour générer CSS / Tailwind automatiquement)

```bash
npm i -D style-dictionary
```

`config.json` :
```json
{
  "source": ["tokens/*.tokens.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "files": [{ "destination": "dist/tokens.css", "format": "css/variables" }]
    },
    "tailwind": {
      "transformGroup": "js",
      "files": [{ "destination": "dist/tokens.js", "format": "javascript/module" }]
    }
  }
}
```

```bash
npx style-dictionary build
```

Tu obtiens :
- `dist/tokens.css` — variables CSS (`--color-brand-terracota: #DC693B`)
- `dist/tokens.js` — objet JS pour Tailwind `theme.extend`

### 3 · Tailwind direct (via `@theme` inline en v4)

```css
@import "tailwindcss";
@theme {
  --color-terracota: #DC693B;
  --color-reading:   #731520;
  --font-sans: "Mont", -apple-system, sans-serif;
  --radius-*: initial;  /* on réinitialise : radius 0 = défaut Nooz */
  --radius-pill: 100px;
}
```

---

## Structure

| Groupe | Usage |
|---|---|
| `color.brand` | Terracota, black, white, background cream |
| `color.text` | 4 niveaux de gris pour texte |
| `color.neutral` | Borders, backgrounds surface |
| `color.accent` | Blue, yellow, error |
| `color.category` | 12 couleurs produit (sun, reading, bluelight, kids, sport, club-house…) |
| `color.semantic` | `fg-1/2/3`, `bg-1/2/3`, `border`, `accent` — aliases |
| `typography.style` | `display`, `h1–4`, `body`, `small`, `caption` — bundles prêts à l'emploi |
| `spacing` | `xs` (8) → `2xl` (60) |
| `radius` | `0` par défaut, whitelist pour exceptions |
| `shadow` | 5 niveaux, tous très subtils |

---

## Règles Nooz rappelées

- **Radius 0** est le défaut. Les autres valeurs sont des exceptions documentées.
- **Mont** est la seule famille. Pas d'Inter, Roboto, system-ui.
- **Pas de gradient**, pas de color hex en dur dans le code : utiliser les tokens.
- **Prix** : toujours format `79,90 $` (virgule, espace, décimales en `weight.thin`).
