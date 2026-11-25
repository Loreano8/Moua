# Revue — Portefeuille crypto (71,2 s, 1080×1920, fr)

## Choix créatifs
- Une seule scène 3D continue (table en bois, mur sauge) au lieu de scènes séparées : la caméra voyage d'objet en objet, sans coupe franche, comme dans le reel de référence.
- Boucle « problème → Alors… → Ça s'appelle X » ×5 (auto-garde, phrase de récupération, portefeuille matériel, sauvegarde métal, passphrase), puis vue éclatée, mise en garde « faux support » et chute « Toi seul as la clé ».
- Accroche ajoutée sur la toute première image (« TON APPLI ≠ TON PORTEFEUILLE ») pour la miniature des réseaux.
- Sous-titres mot à mot, centrés dans la bande sûre de TikTok (x 120–780 px), retirés pendant la vue éclatée où les étiquettes 3D disent déjà les mots.
- Mots de récupération affichés = exemples génériques (« tigre, nuage… »), jamais une vraie phrase.
- Non construit : les variantes de récit (le script a été validé tel quel).

## Mesuré / regardé / non vérifié
- Mesuré : `check` sans erreur ni avertissement de zone sûre ; horaires des mots (transcription whisper `small`, fr) qui pilotent toutes les apparitions.
- Regardé : 18 images de contrôle, la planche de 12 plans, les planches `--review` (vue téléphone 360 px) et les corrections.
- Non vérifié à l'oreille : la voix Kokoro (`ff_siwis`) a été contrôlée par retranscription, pas écoutée. « malware » est réécrit « mal ouère » pour la synthèse seulement.
- Son : voix seule, pas de musique ni de bruitages (aucune source de musique sans compte HeyGen).

## Plan le plus faible
- 48–54 s (passphrase) : la plaque et la tuile n°25 flottent devant le mur, sans lien physique avec la table ; avec plus de temps, une main ou le coffre en arrière-plan ancrerait le plan.
- Ouverture : objets un peu petits dans le cadre vertical (beaucoup de mur au-dessus).

## Avertissements gardés volontairement
- `composition_file_too_large` (world.html, captions.html) : le monde 3D est une seule scène continue ; les sous-titres sont générés par `scripts/build-captions.py`.
- `timeline_track_too_dense` : 195 mots de sous-titres + 8 étiquettes, attendu pour des sous-titres mot à mot.
- `canvas_content_at_edge` : le canvas 3D est plein cadre par construction.
- `console_warning` : Three.js r159 en build UMD (déprécié mais fonctionnel, chargé en local).
