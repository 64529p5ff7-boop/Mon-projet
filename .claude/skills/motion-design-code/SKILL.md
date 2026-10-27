---
name: "motion-design-code"
description: "Pipeline motion design 100 % code (sans After Effects) : film de lancement, promo produit, showreel, vidéo réseaux, remake d'une vidéo pour une autre marque. Brief, beat map, moteur HTML seek(t), rendu Playwright, ffmpeg, son, QA."
---

# Motion design 100 % code (adapté de github.com/howseen-ai/claude-motion-design, licence MIT)

Répondre en français. Un film = un dossier : `<nom>.html` + `render.py` + `audio.py` + `out/` (+ `brand/` logo, palette, captures ; + `facts.md` : chaque chiffre avec sa source).

## Mise en place
- Récupérer les scripts si absents : `git clone --depth 1 https://github.com/howseen-ai/claude-motion-design ~/claude-motion-design`. Modèles utiles : `skill/motion-design/scripts/render_template.py`, `audio_template.py`, `analyze_song.py`, `remake/` ; exemple complet : `examples/howseen-launch/`.
- Playwright + Chromium sont préinstallés. Dans cet espace, le shell n'atteint en général pas les sites de stock (Mixkit, Unsplash, Pexels) : demander à l'utilisateur sa musique / ses images, ou synthétiser les SFX en code (clic = sinus court décroissant, pop = sinus montant, thump = sinus descendant, whoosh = bruit fenêtré).

## 0. Non négociables
- **Zéro invention à l'écran** : chiffres réels sourcés ; tout ce qui est illustratif est étiqueté « Données d'exemple » / « Illustration ». Jamais de fonctionnalité qui n'existe pas. Pas de `facts.md` → pas de chiffres.
- Logos officiels uniquement (fournis), jamais redessinés. Légendes de post vraies (pas de « fait en 10 minutes » si c'est faux).
- Avec une référence : prendre la grammaire, jamais le contenu, les logos, la musique ou les personnes.

## 1. Déroulé (toujours dans cet ordre)
1. **Brief du réalisateur** avant tout code : durée, format maître, formats dérivés depuis la MÊME timeline (16:9, 1:1, 9:16, 4:5), sujet + promesse en une ligne, public, canal, **style de référence nommé** (jamais « premium moderne »), puis les **états** avec timecodes (hook 0-2,5 s → forme qui devient écran 1 → écran 2 avec clic curseur → preuve chiffrée réelle → logo + URL). Sortie : 6 beats + liste des calques + plan son, puis STOP pour validation.
2. **Beat map** (`BEATMAP.md`) : BPM → durée du beat, chaque scène sur un beat, **le drop sur le moment visuel clé**. Rien d'immobile plus d'1 s.
3. **4 stills** (ou une image par beat) → les regarder (Read) → corriger → seulement ensuite le rendu complet.
4. Rendu complet → scan des « pops » → audio → mux → envoyer le fichier avec une légende vraie.

## 2. Le moteur (un seul fichier HTML)
- Tout est calculé depuis le temps dans `window.seek = async (t) => {…}` : **pas de transitions CSS, pas de timers, pas d'état entre frames**. `window.ready = true` après chargement des polices/images. Jamais `Math.random` : PRNG à graine (mulberry32).
- **Ressorts** en forme fermée `step(tau, f, z)` ; presets (raideur/amortissement) : UI vive 320/30, conteneurs/caméra 170/26, typo/logos lourds 120/24, mascottes 180/12. Amortissement ≥ 0,72, jamais de rebond cartoon. Jamais de mouvement linéaire.
- **Caméra** = un transform sur un conteneur, clés `[t, zoom, x, y]`, zoom interpolé en espace log, jamais zoom in/out dos à dos. Punch de beat +0,012, +0,03 par mesure après le drop.
- **Éléments partagés** pour chaque passage (le bouton emporte son label dans la page suivante). Le plan suivant entre déjà en mouvement dans la direction de la sortie.
- **Texte masqué qui monte** (translateY 105 % dans overflow:hidden), décalage mot par mot 55 ms.
- **Floods** : cercle depuis l'objet source qui couvre le coin le plus lointain (hypot × 1,05) en ~0,3 s.
- Librairies pilotables : GSAP (`tl.pause(); tl.totalTime(t+0.001,true); tl.totalTime(t,true)`), anime.js (`autoplay:false` + `seek`), WAAPI (`a.pause(); a.currentTime=t*1000`), Lottie (`goToAndStop`). Jamais de lib temps réel non pilotable.
- Ajouter des contrôles de preview : Espace lecture/pause, ←/→ image par image, R rejouer, affichage du temps.

## 3. Règles anti « look IA »
UNE couleur d'accent ; **une seule chose bouge à la fois** ; un seul système de formes du début à la fin (transformations plutôt que coupes) ; interdits : dégradés arc-en-ciel, particules, chrome brillant, emoji, lorem ipsum, flips 3D gratuits ; typo assez grosse pour un téléphone ; zone sûre 9:16 décidée au storyboard ; toujours la police de la marque. Test muet : quelqu'un qui regarde sans son doit résumer le film en une phrase.

## 4. Rendu (render_template.py)
- Servir le dossier en HTTP (`python -m http.server` en arrière-plan), Playwright, viewport = taille vidéo. Attendre `document.fonts.ready`, mettre en pause les animations CSS, attendre 2 `requestAnimationFrame` après chaque `seek(t)` avant la capture.
- Modes : `probe t1 t2…` (planche), `beats`, `draft` (960x540, 30 fps, toujours avant le master), `full` (sous-frames mélangées pour le flou de bougé, obturateur 0,5 ; jamais de flou à travers une coupe), `pops`, `loop` (position ET vitesse au raccord).
- Films > 25 s : rendre en 3 morceaux en parallèle puis concaténer.
- Encodage final : `scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p`, libx264 crf 16 (`-preset veryfast` sauf demande de qualité max), AAC 256k, `+faststart`. Supersampling 2× pour un texte net.

## 5. Son
- Trouver le drop par l'énergie (bandes basses/pleines par mesure, puis fenêtres 20-50 ms) avec `analyze_song.py`, jamais une grille auto. Démarrer la musique à `drop_morceau - drop_film`.
- Placer chaque SFX par son pic mesuré, gain 0,04-0,3, frappes clavier au rythme de l'animation de frappe. Loudnorm en deux passes à −14 LUFS, TP −1. Voix off : musique baisée de ~9 dB dessous.
- BPM et ambiance : 60-80 solennel, 90-110 fluide, 115-123 élégant, > 125 hype.

## 6. Boucle de critique (avant et après le rendu complet)
```
ffmpeg -i out/final.mp4 -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 out/contact.png
ffmpeg -ss <t-0.1> -i out/final.mp4 -vf "scale=320:-1,tile=12x1" -frames:v 1 out/strip.png
ffmpeg -i out/final.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 out/phone.png
```
Noter sur 10 : hook des 2 premières secondes, lisibilité à 360 px, qualité du mouvement, variété (du nouveau toutes les 2-4 s), composition, exactitude marque/données, synchro son. Lister les 3 pires problèmes avec timecodes, corriger, re-rendre seulement les secondes concernées, renoter. **Répéter jusqu'à 8+ partout.** Pour un film important, faire la critique par un sous-agent séparé en lecture seule. Aucune image figée sauf le plan final.

## 7. Mode remake (copie image par image d'une vidéo pour une autre marque)
Avec la vidéo de référence fournie : `remake/remake_analyze.py` extrait frames, audio et coupes, puis écrire `SPEC.md` (tableau des plans : id, f0-f1, contenu référence, remplacement marque). Moteur `core.js` + `index.html` (seek(F), registre de plans, caméra, curseur), stubs par groupe (`remake_stub.py`), construction par groupes (éventuellement en sous-agents parallèles), rendu `remake_render.py`, `remake_sync.py encode`, QA `remake_qa.py`. Ne jamais réutiliser la musique, la voix ou les personnes de la référence ; créditer la marque d'origine ; pas de co-marquage qui suggère un partenariat.

## 8. Mode film produit (45-75 s, app ou SaaS)
Histoire en chaîne : problème dans les mots du client (3-5 s) → chaque étape PRODUIT ce que la suivante utilise (caméra continue) → résultat mesurable à l'écran → CTA final. Écrans **reconstruits en code** à partir des captures (couleurs échantillonnées au pixel, polices, rayons, ombres dans un fichier `ui-tokens`), animés élément par élément. Textes dans un dictionnaire FR/EN. Pensé pour une lecture sans son. Marges sûres 110 px (16:9) / 80 px (9:16). Livrer 16:9 + 9:16 recomposé (pas un recadrage).

## 9. Diagnostic
| Symptôme | Cause → correction |
|---|---|
| Film générique | Pas de brief/états/style nommé → brief + facts + référence |
| Texte flou, logo délavé | Mis à l'échelle en bitmap → SVG réel, supersampling |
| Saccades à l'export | Timers / transitions CSS → seek(t) pur, attente 2 rAF |
| La boucle saute | Position OK mais pas la vitesse → vérifier `loop` |
| Cheap, ça rebondit | Easing bounce → ressorts amortis ≥ 0,72 |
| Fonctionnalité inventée | Pas de captures / facts.md |
| WebGL noir | Lancer Chromium avec les flags SwiftShader/ANGLE |

## Livraison
☐ stills validés ☐ 0 pop inexpliqué ☐ drop sur le moment clé ☐ −14 LUFS ☐ BT.709 TV range ☐ étiquettes « Données d'exemple » ☐ légende vraie ☐ fichier envoyé (SendUserFile).