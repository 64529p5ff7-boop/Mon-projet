# Épisode 3 : Mike, le poulet qui a vécu 18 mois sans tête

Durée : environ 1 min 10. Charte Wake up smart. Style cartoon sans gore : après la hache, le cou du poulet se termine par un simple capuchon rosé.

Aperçu : `mike-apercu-voix-temporaire.mp4` (voix de synthèse provisoire, à remplacer par la voix ElevenLabs).

## Storyboard

| Plan | Voix off | À l'écran |
|------|----------|-----------|
| 1. Accroche | Ce poulet a vécu 18 mois… sans tête. Et c'est une histoire vraie. | « 18 MOIS / SANS TÊTE. » en très grand, un poulet sans tête qui traverse l'écran en marchant, tampon « HISTOIRE VRAIE ». La 1re image sert de miniature. |
| 2. Le décor | 10 septembre 1945. Dans une ferme du Colorado, Lloyd Olsen prépare le dîner. Au menu : un jeune coq nommé Mike. | Pastille « 10 SEPTEMBRE 1945 », grange rouge, « FRUITA · COLORADO », « LLOYD OLSEN, FERMIER », puis « AU MENU : MIKE ». |
| 3. La hache | Un coup de hache. Mais Mike… se relève. Et il repart picorer, comme si de rien n'était. | La hache s'abat, flash blanc, tremblement, plumes qui volent (aucun sang). Le poulet titube, puis marche et picore. Tampon « IL SE RELÈVE ». |
| 4. Le gag | Le lendemain matin, Olsen le retrouve endormi… la tête sous l'aile. Enfin, ce qu'il en reste. | Nuit, lune, étoiles, poulet endormi avec des « z ». « LA TÊTE SOUS L'AILE… », puis « ENFIN… CE QU'IL EN RESTE ». |
| 5. L'explication | L'explication ? La hache a raté la veine jugulaire. Un caillot a stoppé le saignement. Et la base du cerveau… est restée intacte. | Cou du poulet en surbrillance, 3 cartes cochées une à une : jugulaire ratée, caillot, base du cerveau intacte. |
| 6. Survivre | Alors Olsen le nourrit à la pipette : de l'eau, du lait, des petits grains de maïs. Directement dans le gosier. | Pipette qui descend et goutte, pastilles « EAU », « LAIT », « MAÏS ». |
| 7. La gloire | Mike devient une star. Le magazine Life parle de lui. Il part en tournée… 25 cents pour le voir. Il est assuré 10 000 dollars. | Une de journal « MIRACLE MIKE » (sans logo réel), trajet de tournée en pointillés, ticket « 25¢ », tampon « ASSURÉ 10 000 $ ». |
| 8. La chute | Mais en mars 1947, dans un motel de Phoenix, Mike s'étouffe en pleine nuit. La seringue qui servait à le dégager… avait été oubliée la veille. | L'écran s'assombrit, enseigne néon « MOTEL » qui grésille, le poulet s'efface, seringue barrée « OUBLIÉE LA VEILLE ». |
| 9. L'héritage | 18 mois sans tête. Un record du monde. Et aujourd'hui encore, sa ville du Colorado organise chaque année un festival en son honneur. | « 18 MOIS SANS TÊTE », tampon « RECORD DU MONDE », confettis, Mike avec un chapeau de fête, « FRUITA · UN FESTIVAL CHAQUE ANNÉE ». |
| 10. Abonnement | Abonne-toi à Wake up smart. Chaque jour, une histoire à savoir, en une minute. | Logo soleil levant, bouton « + ABONNE-TOI ». |

Le texte à coller dans ElevenLabs est dans `VOIX-OFF.txt`.

## Publication

- **Légende proposée** : « Il a vécu 18 mois sans tête 🐔 Histoire vraie, Colorado, 1945. Tu connaissais ? #histoirevraie #insolite #lesaviezvous #wakeupsmart »
- **Question à épingler en commentaire** : « Quel animal mérite le prochain épisode ? »

## Fabrication

1. `build/tts.py` + `build/timeline_tts.py` : voix provisoire (Kokoro) et timeline de l'aperçu.
2. Quand la voix ElevenLabs est là : détection des silences + transcription (`asr.py` de l'épisode 2), puis un `sync.py` qui regroupe les morceaux de parole par plan, comme pour l'épisode 2. L'impact de la hache se cale tout seul sur la fin de « Un coup de hache. ».
3. `node render.js sfx`, puis `python3 ../../core/audio.py timeline.json sfx.json mix.wav voix.wav 0`, puis `OUT=../mike.mp4 node render.js full`.
