---
workflow: general-video
flow: automation
storyboard: no
message: "Binance now has 3 AI products — here is which one is for you, and why you stay in control. Read the full guide."
destination: x-feed
aspect: 1080x1920
language: en
length: 40.6s
---

## Intent

Vidéo explicative de l'article du blog Binance du 26/10/2026 « Binance Intelligence Explained: Binance AI vs. Binance AI Pro vs. Agent OS » (https://www.binance.com/en/blog/tech/2612927534315150666). Objectif : donner envie à l'audience d'aller lire l'article complet, avec un appel à l'action final et le lien dans le post.

Déroulé : accroche (clip de Loreano au PC) → les 3 produits en un coup d'œil → Binance AI (informe, ne trade jamais) → AI Pro (idée en langage naturel → workflow testé puis approuvé) → Agent OS (agents IA branchés via le serveur MCP, permissions coupées par défaut) → « You stay in control » → fin sur Loreano qui sourit et pointe la caméra + carte de l'article.

## Assets

- assets/video/pc.mp4 — clip de Loreano au PC (8 s), repris de la vidéo Understanding Stocks : il tape (accroche), puis sourit et pointe la caméra (fin)
- assets/vo/vo.m4a — voix off anglaise générée avec Higgsfield (Seed Audio 1.0, voix « Grady »), pauses resserrées et accélérée de 8 % ; assets/vo/transcript.json = horaires mot à mot (hyperframes transcribe) qui calent les scènes
- assets/img/*.jpg — illustrations 3D générées avec Higgsfield (Z Image) : i0-trio, i1-phone, i2-laptop, i3-agent, i4-control
- assets/audio/bgm.m4a — lo-fi jazz / boom-bap original généré par scripts/make-bgm.py (96 BPM), baissé sous la voix
- assets/sfx/*.mp3 — bruitages de la bibliothèque HyperFrames (licence Pixabay), dont impact-bass-1 repris d'academy-cert

## Notes

- Lu avec Agent Reach le 27/10/2026. Toutes les infos à l'écran viennent de l'article : fonctionnalités de Binance AI, plans AI Pro (Standard gratuit, Premium 19,99 USDC/mois), permissions d'Agent OS désactivées par défaut sauf la lecture, compatibilité Claude Code / Cursor / Codex / ChatGPT, garde-fous communs (permissions, limites de financement, sous-comptes isolés, révocation à tout moment).
- Choix par défaut (non confirmés par l'utilisateur) : anglais et format X vertical comme les autres vidéos Binance du dossier ; « Not financial advice » à l'écran ; lien complet dans le post, pas dans la vidéo.
- V2 (demande de Loreano) : plus d'illustrations et une voix off. Chaque produit s'ouvre sur son illustration en grand, qui reste ensuite à l'écran pendant les explications. Coût Higgsfield : 4,1 crédits pour la voix et 0,15 crédit par image.
- Vérification des faits (V3) : chaque phrase de la voix et chaque texte à l'écran ont été relus contre l'article. Corrigé : « AI helps plan it » (l'article dit « help plan »), « Test it in paper trading » (le test est possible, pas obligatoire), « Quickest way in: the Binance MCP server » + agents faits maison, et titre exact de l'article dans la carte finale.
