# Studio Motion — 8 outils motion design pour Claude Code

Les 8 outils de la vidéo « 8 outils motion design » (@saas_builders), installés comme
compétences (skills) du projet dans `.claude/skills/`. Ils se chargent automatiquement
dans chaque nouvelle session Claude Code ouverte sur ce dépôt.

| # | Outil (vidéo) | Source | Compétences installées |
|---|---|---|---|
| 1 | Product Launch Motion | [AbubakrChan/product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) | `product-launch-motion` |
| 2 | Motion Graphics Skills (15 compétences) | [charlie947/motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills) | `brand-intake`, `motion-brief-writer`, `motion-prompt-writer`, `launch-video`, `apple-launch-film`, `vox-explainer`, `animated-chart`, `milestone-reveal`, `model-showdown`, `title-sequence-3d`, `loop-cover`, `newsletter-promo`, `reference-to-motion`, `motion-effects`, `reel-export` |
| 3 | Hyperframes | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `slideshow`, `remotion-to-hyperframes`, `figma` |
| 4 | Motion Graphics | [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics) | `motion-broll`, `object-separation`, `explainer-default`, `explainer-engaging`, `explainer-high-energy`, `sound-effects` |
| 5 | Animate (7 styles) | [cth9191/animate](https://github.com/cth9191/animate) | `animate` |
| 6 | Claude Motion (sound design) | [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) | `claude-motion-motion-design`, `claude-motion-sound-design`, `claude-motion-review-loop`, `claude-motion-web-sims` + toolkit dans `outils-motion/claude-motion/` |
| 7 | Motion (animer ton site) | [199-biotechnologies/motion-dev-animations-skill](https://github.com/199-biotechnologies/motion-dev-animations-skill) | `motion-dev-animations` |
| 8 | Motion Design Skills (12 principes Disney) | [LottieFiles/motion-design-skill](https://github.com/lottiefiles/motion-design-skill) | `motion-design` |

Les noms exacts des outils 6 et 7 ne sont pas donnés dans la vidéo (envoyés en DM) :
ce sont les dépôts publics qui correspondent le mieux à la description.

## Les 5 catégories (comment les combiner)

1. **Vidéos de lancement** — `product-launch-motion` (script, voix off, mouvements de
   caméra, étalonnage) + les 15 compétences Motion Graphics Skills pour les vidéos de
   lancement réelles.
2. **Monter tes vidéos** — `hyperframes` coupe blancs et ratés, ajoute animations et
   sous-titres ; `motion-broll` crée des plans d'illustration calés sur ta voix,
   `object-separation` détoure l'arrière-plan.
3. **Vidéos animées** — `animate` (7 styles, storyboard d'abord), puis
   `claude-motion-sound-design` / `sound-effects` pour tout le sound design.
4. **Animer ton site** — `motion-dev-animations` : boutons, cartes, transitions de page.
5. **Les fondations** — `motion-design` (12 principes de Disney, timing, easing) : toutes
   les autres compétences s'appuient dessus pour que le résultat ait l'air fait par un humain.

### Chaîne type « Studio Motion »

```
brand-intake → motion-brief-writer → product-launch-motion / animate
   → hyperframes (montage, sous-titres) → motion-broll / object-separation
   → sound-effects ou claude-motion-sound-design → motion-design (relecture des principes)
   → reel-export (formats réseaux sociaux)
```

## Prérequis

- Node.js ≥ 22, FFmpeg, Python 3 (présents dans l'environnement cloud).
- Hyperframes : `npx hyperframes` (téléchargé au premier usage).
- `object-separation` télécharge un modèle SAM2 au premier lancement (lourd).
- Claude Motion : `cd outils-motion/claude-motion && npm install` avant le premier rendu.

Licences : MIT pour tous, Apache-2.0 pour Hyperframes (fichier `LICENSE` dans chaque compétence).
