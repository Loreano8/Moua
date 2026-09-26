# Moua

Projet vidéo [HyperFrames](https://hyperframes.heygen.com) : des compositions HTML + GSAP rendues en MP4/WebM.

## Démarrage

```bash
npm run dev      # aperçu dans le Studio (navigateur)
npm run check    # lint + validation runtime + mise en page + contraste
npm run render   # rendu MP4
```

Nécessite Node.js 22+. Le rendu local utilise Chrome et ffmpeg (`npx hyperframes doctor` pour vérifier).

## Structure

- `index.html` — composition principale (timeline racine `main`, 1920×1080, 10 s)
- `compositions/` — sous-compositions (`data-composition-src`)
- `hyperframes.json` — configuration du projet et du registre de blocs
- `meta.json` — métadonnées du projet
- `CLAUDE.md` / `AGENTS.md` — consignes pour les agents IA


## Skills IA

Les skills HyperFrames sont versionnés dans `.claude/skills/` et chargés automatiquement par Claude Code. Pour les mettre à jour : `npx hyperframes skills update`, puis recopier `~/.claude/skills/<nom>` dans `.claude/skills/`.
