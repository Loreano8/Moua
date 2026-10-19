---
workflow: general-video
flow: automation
storyboard: no
message: "Sketch : le fils dit tout haut que le gâteau du voisin finit au chien."
destination: social-vertical
aspect: 1080x1920
language: fr
length: 23.6s
---

## Intent

Sketch comique vertical façon reel « dessin au trait » (inspiré d'un format Facebook, personnages originaux).
M. Bernard, le voisin, apporte son gâteau aux carottes ; la mère fait semblant d'adorer ; Léo, son fils, révèle que le dernier a fini au chien.

## Assets

- assets/audio/dialogue.wav : voix Piper (tom = Bernard, siwis = mère, siwis montée de 5,5 demi-tons = Léo), générée par scripts/make-voices.py
- assets/timing.json : timing mot à mot (faster-whisper) et battement de bouche, par scripts/analyse-voices.py
- index.html : généré par scripts/build.py (personnages SVG dessinés à la main dans le script)

## Notes

- Pour changer une réplique : modifier LINES dans scripts/make-voices.py, puis relancer make-voices.py → analyse-voices.py → build.py.
