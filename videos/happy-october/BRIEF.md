---
workflow: general-video
flow: automation
storyboard: no
message: "Good morning, Queen — Happy October. Love you."
destination: social-vertical
aspect: 1080x1920
language: en
length: 15s
---

## Intent

Message vidéo du 1er octobre pour sa chérie : un selfie filmé « vite fait, sans préparation » (« Good morning Queen, I just want to say Happy October. Bye. Peace. Love you. »), embelli : intro, sous-titres animés, titre « Happy October » avec des feuilles d'automne, carte de fin avec photo.

## Assets

- assets/video/selfie.mp4 — selfie d'origine (10,7 s), stabilisé (vidstab), légèrement accentué, 1080×1920 à 30 i/s ; grade « warm-daylight » appliqué dans la composition
- assets/audio/voice.m4a — voix nettoyée : très fort bruit de moteur à l'origine (rapport signal/bruit ≈ 1 dB → ≈ 15 dB). Chaîne ffmpeg : passe-haut 90 Hz, RNNoise ×2 (modèle « somnolent-hogwash »), gate doux, EQ de présence, compresseur, loudnorm −16 LUFS
- assets/audio/bgm.m4a — musique originale générée par scripts/make-bgm.py (72 BPM, boîte à musique + nappe)
- assets/img/portrait.jpg — image fixe extraite du selfie (t = 3 s) pour la carte de fin
- assets/sfx/chime.mp3 — bruitage de la bibliothèque HyperFrames (licence Pixabay)
- assets/fonts — Great Vibes, Playfair Display, Montserrat (Fontsource, licence OFL)

## Notes

- Prénom inconnu : « Queen », comme dans le message.
- Sous-titres calés sur la voix : temps de la composition = temps de la source + 1,2 s.
