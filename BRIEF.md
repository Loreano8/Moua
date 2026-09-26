---
workflow: general-video
flow: automation
storyboard: no
message: "Moua fait le travail répétitif pour que tu te concentres sur l'essentiel"
destination: social-vertical
aspect: 1080x1920
language: fr
length: 8.5s
---

## Intent

Courte promo verticale pour les réseaux sociaux présentant l'app / le produit Moua. Le plan fourni (une personne qui travaille sur un portable) sert de décor. Par-dessus : des textes animés, une musique de fond et un appel à l'action final.

## Assets

- assets/video/desk.mp4 — clip fourni (6 s, 720×1280, 60 i/s) ; fond des 7 premières secondes, légèrement ralenti
- assets/audio/bgm.m4a — musique d'ambiance originale générée par scripts/make-bgm.py (120 BPM)

## Customizations

- Appel à l'action : « Essaie gratuitement »

## Notes

- Choix par défaut (non confirmés par l'utilisateur) : nom du produit « Moua », accroches « Moins de tâches. / Plus d'impact. / Moua gère le reste. », slogan de fin et palette sombre avec accent ambre (rappel des détails dorés du t-shirt).
- La musique est synthétisée : ni connexion HeyGen ni MusicGen n'étaient disponibles dans l'environnement. Remplacer assets/audio/bgm.m4a par un morceau sous licence si besoin.
- GSAP est fourni en local (assets/vendor) pour un rendu hors ligne et déterministe.
