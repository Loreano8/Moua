---
workflow: general-video
flow: automation
storyboard: no
message: "A raw wallet address is 42 random characters; loreano.ai is one name, mine, that works as a payment address."
destination: x-feed
aspect: 1080x1920
language: en
length: 26s
---

## Intent

Vidéo pour la campagne Binance Wallet « My Agent ID » (#MyAgentID, date limite 31/10/2026 16:00 UTC). Elle montre à quoi sert concrètement l'Agent ID loreano.ai et ce qu'il change par rapport à une adresse classique.

Déroulé (120 BPM, coupes à la mesure) : accroche sur le clip de Loreano au PC, avec une adresse 0x… interminable qui se tape → l'adresse se brouille et devient loreano.ai, puis la comparaison ✕ / ✓ → la carte Agent ID tourne et arrive, avec ses règles (un par personne, non transférable, pas renommable, gratuit hors frais BNB) → démonstration « Send 1 USDT to loreano.ai » : l'agent montre la vraie adresse, attend la confirmation → « dans AI Pro, en langage normal, dans ta limite journalière » → fin sur Loreano qui sourit : « Every onchain agent needs a name. Mine is loreano.ai ».

## Assets

- assets/video/pc.mp4 — clip de Loreano au PC (8 s), sans son (le clavier ne s'entend plus)
- assets/img/agent-id-card.png — carte Agent ID de Loreano, recadrée, fond transparent
- assets/audio/bgm.m4a — musique électronique originale (120 BPM, la mineur) générée par scripts/make-bgm.py
- assets/sfx/*.mp3 — bruitages de la bibliothèque HyperFrames (licence Pixabay)

## Notes

- Sources : doc Binance « Agentic Wallet × AI Pro » (web3.binance.com/en/dev-docs/products/agentic-wallet/ai-pro), page « Send Tokens », page Agent ID (« Every Onchain Agent Needs a Name », « Use this name to represent your Agent Onchain »).
- L'adresse 0x7f3A…19D2 est un exemple, pas l'adresse de Loreano. La scène d'envoi est marquée « Illustrative example ».
- Pas de musique Higgsfield (aucun modèle de musique sur le plan gratuit) ni HeyGen (compte requis) : musique composée en local.
