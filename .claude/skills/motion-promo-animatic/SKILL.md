---
name: "motion-promo-animatic"
description: "Produire une animatic/animation promo à partir d'un storyboard : génère la vidéo animée (Motion ou HTML), l'exporte en 16:9 et 9:16, et peut l'envoyer dans Canva."
---

# Animatic / animation promo

Prend un storyboard (idéalement issu du skill promo-app-storyboard) et produit une version animée à montrer au client ou à finaliser.

## Préparation
- Vérifier qu'on a : storyboard avec timecodes, palette hex, polices, assets (logos, captures d'app). S'il manque des assets, utiliser des placeholders clairement marqués (rectangle « LOGO », écran vide de téléphone).
- Ne jamais redessiner un logo de marque de mémoire : utiliser le fichier fourni ou un placeholder.

## Production
1. Si le type d'artifact « Motion » est disponible (Artifact quickstart / list types), créer l'animation depuis ce type en suivant ses instructions.
2. Sinon, construire une page HTML/CSS/JS (GSAP via cdnjs) avec une timeline par plan, durée totale = storyboard, et la publier en artifact.
3. Rendu MP4 si demandé : capturer avec Playwright (Chromium préinstallé) image par image à 30 fps puis `ffmpeg -framerate 30 -i f_%05d.png -c:v libx264 -preset veryfast -pix_fmt yuv420p out.mp4`.
4. Déclinaisons : 16:9 (1920x1080) et 9:16 (1080x1920, texte en haut, téléphone en bas, garder 15 % de marge pour l'interface TikTok).
5. Musique : laisser une piste vide ou ajouter la musique fournie par l'utilisateur (`ffmpeg -i out.mp4 -i music.mp3 -shortest -c:v copy -c:a aac final.mp4`).

## Bonnes pratiques d'animation
- Textes : apparition mot par mot, 0,3-0,5 s, ease-out ; rester lisible au moins 1,2 s.
- Téléphone : entrée avec léger overshoot (back.out), rotation 3D légère en style B.
- Transitions : balayage par vague, zoom dans l'écran, slide, flou de mouvement sur les carrousels.
- Un seul mouvement principal à la fois par plan.

## Export vers Canva (optionnel)
Si l'utilisateur veut retoucher dans Canva, utiliser l'outil Canva d'import d'animation Claude Motion (import-claude-motion-from-url) puis suivre le statut du job, et donner le lien du design.

## Livraison
Envoyer le MP4 (SendUserFile) et/ou l'artifact, avec une ligne sur ce qui reste à remplacer (placeholders, musique).