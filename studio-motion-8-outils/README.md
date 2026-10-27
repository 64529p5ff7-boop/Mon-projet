# Studio Motion — 8 outils (remake)

Remake image par image de la vidéo « 8 outils motion design » (82 s, 9:16). La mise en page,
les animations, la mascotte, les cartes et les sous-titres calés sur la voix sont identiques.
L'audio d'origine est conservé.

**Seule différence :** ton compte (`handle` dans `build/timeline.json`) remplace
@saas_builders. L'écran de fin TikTok (le logo et la barre de recherche ajoutés par TikTok
au téléchargement) a été retiré : TikTok le remet automatiquement avec ton compte quand ta
vidéo est téléchargée.

## Fichiers

- `studio-motion-8-outils.mp4` : la vidéo finale (1080 x 1920, 30 i/s, 77,6 s).
- `build/scene.html` : la scène animée (canvas), avec `render(t)` comme fonction pure du temps.
- `build/captions.txt` : le texte des sous-titres, un groupe par ligne. Les mots entre `[ ]`
  sont surlignés en orange.
- `build/captions.json` : l'instant d'apparition de chaque mot, calculé par `timing.py` à
  partir de l'analyse image par image de l'original (`analyse_sous_titres.json`).
- `build/timeline.json` : la durée totale et le nom du compte affiché.
- `build/audio.flac` : la piste audio d'origine, coupée à 77,6 s.

## Régénérer

```bash
cd build
python3 timing.py                     # après avoir modifié captions.txt
node render.js stills 1.8 19.4 76.5   # images de contrôle still_<t>.jpg
node render.js                        # rendu complet -> ../studio-motion-8-outils.mp4
```
