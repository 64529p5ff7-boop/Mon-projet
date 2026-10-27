---
name: "analyse-reference-motion"
description: "Décortiquer une vidéo motion design de référence (MP4) : planche de frames, découpage des plans, rythme, palette, typo, transitions, et fiche de style réutilisable."
---

# Analyse d'une vidéo de référence

Quand l'utilisateur envoie une ou plusieurs vidéos d'inspiration, produire une fiche de style exploitable pour reproduire l'esprit (sans copier logos ni marques).

## Étapes techniques
1. Infos : `ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact video.mp4`
2. Planche contact : `ffmpeg -i video.mp4 -vf "fps=1/1.5,scale=360:-1,tile=6x4" -frames:v 1 sheet.jpg` puis la lire en image.
3. Détection des coupes : `ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep pts_time` → liste des timecodes de plans, durée moyenne d'un plan.
4. Palette : extraire 3-4 frames clés et en tirer 5 couleurs dominantes (Python + PIL quantize), donner les hex.
5. Audio : `ffmpeg -i video.mp4 -af ebur128 -f null -` pour le niveau ; si voix off, transcrire si un outil est dispo, sinon noter « musique seule ».
6. Zoomer sur une frame précise si besoin : `ffmpeg -ss 12.5 -i video.mp4 -frames:v 1 f.jpg`.

## Fiche de style à livrer
- Format, durée, nombre de plans, durée moyenne par plan
- Structure narrative (hook → marque → fonctionnalités → relance → CTA) avec timecodes
- Palette (hex) et usage (fond, accent, texte)
- Typographies (famille approchante, graisse, casse, alignement) et polices libres équivalentes (Google Fonts)
- Éléments graphiques récurrents (mockups, icônes, formes de fond, 3D/2D)
- Catalogue des transitions et mouvements (avec timecode d'exemple)
- Easing et rythme (doux / punchy, calé musique ou non)
- Ce qui marche bien / ce qui pourrait être amélioré (lisibilité, durée des textes à l'écran, safe zones TikTok)
- 3 idées pour réutiliser ce style sur un autre projet

Comparer les références entre elles si plusieurs vidéos sont fournies (tableau côte à côte).