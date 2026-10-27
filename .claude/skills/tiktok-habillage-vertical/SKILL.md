---
name: "tiktok-habillage-vertical"
description: "Habiller une vidéo 16:9 pour TikTok/Reels en 9:16 : bande vidéo centrée, titre en haut, pastille d'appel à commenter (« Commente « mot » … ») en bas, export prêt à poster."
---

# Habillage vertical TikTok d'une vidéo 16:9

Format « lead magnet » : la vidéo 16:9 garde sa composition, posée au centre d'un cadre 9:16 noir, avec un titre en haut et une pastille d'appel à l'action en bas qui incite à commenter un mot-clé.

## Demander (si absent)
- La vidéo source 16:9
- Le titre du haut (court, en MAJUSCULES, ex. « V2 VIDÉO MOTION DESIGN »)
- Le texte de la pastille (ex. « Commente « motion » si tu veux reproduire ce genre de vidéos »)
- Couleur de la pastille (défaut rouge foncé #8b1e2b, texte blanc), fond (défaut noir #000)

## Mise en page (1080x1920)
- Vidéo mise à l'échelle 1080 de large (1080x608), centrée verticalement (y = 656).
- Titre : blanc, gras, ~44 px, centré, ~80 px au-dessus de la vidéo (zone y 520-600).
- Pastille : rectangle arrondi, ~30 px de texte, centrée, ~70 px sous la vidéo ; marges latérales ≥ 60 px.
- Garder libres les zones de l'interface TikTok : 120 px à droite (boutons), 300 px en bas (légende), 150 px en haut.

## Fabrication
1. Générer le titre et la pastille en PNG transparents 1080x1920 avec Playwright (page HTML avec la police de la marque, `omit_background=True`) ou PIL. Vérifier l'image (Read) avant l'export.
2. Composer :
```
ffmpeg -i source.mp4 -i overlay.png -filter_complex "[0:v]scale=1080:-2,setsar=1[v];color=c=black:s=1080x1920:r=30[bg];[bg][v]overlay=0:(H-h)/2:shortest=1[b];[b][1:v]overlay=0:0" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out_9x16.mp4
```
3. Option pastille animée (apparition à 1 s, léger pulse toutes les 8 s) : rendre l'overlay en séquence PNG avec alpha et utiliser `-i overlay_%04d.png`.
4. Contrôle : planche `ffmpeg -i out_9x16.mp4 -vf "fps=1/5,scale=270:-1,tile=6x2" -frames:v 1 check.png`, vérifier lisibilité à petite taille et que rien n'est sous les boutons TikTok.
5. Envoyer le fichier (SendUserFile) et proposer la légende du post avec le même mot-clé que la pastille.

## Règles
- Ne pas ajouter de logo TikTok ni de faux identifiant : TikTok ajoute son filigrane lui-même.
- La promesse de la pastille doit être tenue (avoir réellement la ressource à envoyer aux commentateurs).