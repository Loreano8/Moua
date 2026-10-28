---
workflow: general-video
flow: automation
storyboard: no
message: "You can now sell options on Binance Stock Options: get paid a premium upfront with a Covered Call or a Cash-Secured Put, and see what happens in each case."
destination: x-feed
aspect: 1080x1920
language: en
length: 55s
---

## Intent

Vidéo explicative illustrée et démonstrative de l'article du blog Binance du 27/10/2026 « Covered Call and Cash-Secured Put Are Now Live on Binance Stock Options » (https://www.binance.com/en/blog/ecosystem/3830803088632468425).

Déroulé, calé mot à mot sur la voix off : accroche (clip au PC, interrupteur BUY → SELL) → « vendre des options, être payé tout de suite » → Covered Call pas à pas (100 $, call à 110 $, +3 $) → graphique : le cours reste sous 110 $ / monte à 150 $ (vendu à 110 $, +40 $ abandonnés) → Cash-Secured Put pas à pas (100 $, on veut 90 $, USDC bloqués, put à 90 $, +3 $) → graphique : reste au-dessus de 90 $ / descend à 90 $ (87 $ effectif) / chute à 70 $ (−17 $ par action) → fin : risque élevé + carte de l'article.

## Assets

- assets/vo/vo.m4a — voix off anglaise Higgsfield (Seed Audio 1.0, voix « Grady »), pauses resserrées et accélérée de 7 % ; assets/vo/transcript.json = horaires mot à mot
- assets/img/i-premium.jpg, i-shares.jpg, i-vault.jpg — illustrations 3D Higgsfield (Z Image)
- assets/video/pc.mp4 — clip de Loreano au PC
- assets/audio/bgm.m4a — lo-fi original (scripts/make-bgm.py, 96 BPM), sous la voix
- scripts/make-setup-scenes.py et scripts/make-chart-scenes.py génèrent s3, s5 (étapes) et s4, s6 (graphiques)

## Notes

- Tous les chiffres sont les exemples de l'article (par action). Les trajectoires de prix des graphiques sont illustratives : seuls les points de départ, d'exercice et d'arrivée viennent de l'article. Mention à l'écran : « Example prices from the Binance article · per share · not financial advice ».
- Coût Higgsfield : 5,5 crédits pour la voix, 0,15 par image.
