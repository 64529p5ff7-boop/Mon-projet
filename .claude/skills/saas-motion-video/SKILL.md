---
name: "saas-motion-video"
description: "Promo ou vidéo motion pour une app, un SaaS ou un outil (lancement, révélation de fonctionnalité, boucle sociale) avec la méthode en 7 étapes du saas-motion-kit et sa galerie de 101 thèmes."
---

# saas-motion-video (adapté de github.com/tugrawork-creator/saas-motion-kit, licence MIT)

Répondre à l'utilisateur en français. Tu es le producteur, l'utilisateur est le directeur artistique. Exécute les étapes dans l'ordre et **arrête-toi à chaque validation (gate)** pour une décision humaine.

**La règle unique du kit : deux films ne doivent jamais donner l'impression d'être le même film.** Ne répète pas effets, transitions ou composants (dans le film ni par rapport aux films récents de l'utilisateur). Invente au moins un nouveau composant par film. Décide le message et le ton avant de choisir le moindre effet.

## Avant de commencer
- Récupérer le kit dans l'espace de travail s'il n'y est pas : `git clone --depth 1 https://github.com/tugrawork-creator/saas-motion-kit ~/saas-motion-kit`. Tous les chemins ci-dessous (`playbook/`, `creative/`, `templates/`, `tools/`, `docs/themes/`) sont relatifs à ce dossier.
- Lire `playbook/README.md`, puis chaque fichier d'étape au moment d'y arriver. Lire `creative/README.md` avant l'étape 4.
- Rendu : le kit vise HyperFrames (`npx skills add heygen-com/hyperframes`). Si HyperFrames n'est pas disponible dans la session, construire la page en HTML + GSAP pilotée par `window.seek(t)` (déterministe) et rendre image par image avec Playwright (Chromium déjà installé) + ffmpeg. Le dire à l'utilisateur en une ligne.
- Historique des films : `~/.motion-ledger.json`.

## Étapes
1. **Brief** (`playbook/01-brief.md`). Quatre questions maximum : le message unique, le canal/format, le son (musique, SFX, voix ou muet) et la source de vérité (URL ou docs). Demander aussi s'il a des vidéos de référence. Pour chacune : `python tools/breakdown.py <video> --id NN --creator … --url …` et créditer dans `REFERENCES.md` (`templates/REFERENCES.md`, `creative/references.md`) : emprunter la grammaire, jamais les assets. Écrire `BRIEF.md` depuis `templates/BRIEF.md`. **Gate :** l'utilisateur confirme le brief.
2. **Composants** (`playbook/02-components.md`, `components/README.md`). S'il y a une URL, capturer l'UI réelle (`npx hyperframes capture` ou captures Playwright). Proposer pour chaque composant *réel* ou *imaginaire*. Ne jamais inventer de fonctionnalités, clients ou statistiques. **Gate :** l'utilisateur valide l'inventaire.
3. **Thème** (`playbook/03-theme.md`). Proposer 2-3 thèmes de `docs/themes/data/*.json` adaptés au public (lire `summary`, `fit`, `best_for`). Partir de `python tools/pick_themes.py --tone <ton> --audience "<mots public>" --history ~/.motion-ledger.json` (ignore les thèmes des 5 derniers films). Redessiner l'image clé de chaque candidat aux couleurs de la marque en still HTML. **Gate :** l'utilisateur choisit.
4. **Storyboard + passe créative** (`playbook/04-storyboard.md`, `creative/`). Écrire `STORYBOARD.md` depuis `templates/STORYBOARD.md` : d'abord la phrase **Message & ton** (« Je veux dire ___ sur un ton ___, pour que le spectateur ressente ___ »), puis le **ledger** (une ligne par plan : entrée, transition, easing, direction, palette, caméra, composants, nouveau composant, sfx, notes), puis les images. Choisir le craft dans `creative/tone-matrix.md`, les transitions dans `creative/transition-atlas.md`, et forger au moins un nouveau composant avec `creative/component-forge.md`. Lancer `python tools/variety_audit.py STORYBOARD.md --history ~/.motion-ledger.json` et corriger chaque alerte, ou marquer une répétition voulue `motif:`. Puis une planche de croquis d'une page. Minimum de mots à l'écran. **Gate :** audit propre et les stills racontent l'histoire son coupé.
5. **Build** (`playbook/05-build.md`). Workflow HyperFrames (`/product-launch-video` pour une promo depuis une URL, `/general-video` pour boucles et pièces sur mesure) ou le repli HTML + seek(t). Chaque frame déterministe et seek-safe. Lancer `lint`, `snapshot`, `check` (ou une planche contact ffmpeg). **Gate :** l'utilisateur valide la preview.
6. **Son** (`playbook/06-sound.md`). Musique : grille de beats d'abord, couper sur les mesures. SFX : timbres chauds et accordés (`tools/warm_sfx.py`). Muet est un choix valable. **Gate :** l'utilisateur valide le mix.
7. **Livraison** (`playbook/07-deliver.md`). Rendu 4K puis `tools/deliver.sh` pour réduire. Boucles : `tools/loop_check.py`. Donner durée, poids et fichier réels (SendUserFile). Enregistrer le film : `python tools/variety_audit.py STORYBOARD.md --history ~/.motion-ledger.json --append "<film>" --theme <NNN>`. Tous les quelques films, proposer `python tools/history_report.py ~/.motion-ledger.json -o motion-history.html`. **Gate :** l'utilisateur vérifie sur l'écran cible.

## Règles strictes
- Logos officiels uniquement, fournis par l'utilisateur. Ne jamais redessiner une marque.
- Accents français et caractères non latins : embarquer les sous-ensembles `latin-ext` des polices. Écrire soi-même les majuscules plutôt que `text-transform`.
- Pas de barres de progression, pas de texte en dégradé, pas de #000/#fff purs, pas d'easing bounce ou elastic sur l'UI.
- Moins de mots. Si l'histoire doit se lire, redessiner l'image.
- Créditer chaque vidéo de référence (nom + lien) ; ne jamais mettre les images, la musique ou les rushes de quelqu'un d'autre dans un film.
- Chaque transition doit répondre à « pourquoi celle-ci, ici ? ». Jamais deux fois la même transition d'affilée, au moins trois familles de transitions, une surprise toutes les ~15 s.