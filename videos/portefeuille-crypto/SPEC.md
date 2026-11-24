GOAL:    le spectateur sait qu'une appli d'échange n'est pas un portefeuille, et peut nommer les 5 pièces d'une garde sûre.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps
TIME:    71.2 s x 30 = 2136 frames. Voix = horloge (assets/beats.json, assets/transcript.json). Pas de musique (aucune source sans compte HeyGen).
LOOK:    monde 3D low-poly, flatShading, un seul plateau : table en bois #B9824F (planches visibles, 4 lattes),
         mur de fond #CFE0D6 (vert sauge, uni, pas de dégradé), lumière clé chaude #FFE2B8 en haut à gauche (intensité 2.2),
         contre-jour froid #BFD8FF (0.6), hémisphère ciel #F4F1E8 / sol #6B4A2E (0.9). Ombres de contact : disques #000 opacité 0.18.
         Accent or #F2B705 réservé à la clé, aux pièces et au terme nommé. Danger #E5484D réservé aux menaces (verrou, fissure, bug, feu, faux support).
         Validation #2FB673 réservé au tampon « SIGNÉ ».
         Texte : Archivo Black. Sous-titres 1 mot, 104 px, blanc #FFFFFF, contour 10 px #1E1A16, bas du mot à y=1210.
         Terme nommé : Archivo Black 92 px #1E1A16 sur bandeau or #F2B705 (padding 18/36 px, coins 6 px), haut à y=330.
OBJECTS: téléphone (boîtier noir #22252A arrondi 7x15x0.9, écran éclairé avec appli), vitrine de la plateforme (verre + rideau métallique),
         pièces (cylindres or biseautés, 16 faces), clé (anneau + tige + 3 dents, or), coffre (acier #8C96A0, porte + molette),
         24 tuiles de mots (blanc cassé #FAF6EC, chiffre + mot), bug malware (corps rouge, 6 pattes), boîtier matériel (#2B2F36, mini écran + 2 boutons),
         feuille de papier, plaque en acier gravée (#AEB6BD, points poinçonnés), tiroir, bulle de faux « Support ».
MOTION:  entrées : back.out(1.6) 0.5 s ; déplacements : power2.inOut ; sorties : power2.in 0.3 s ; caméra : interpolation cubique (smoothstep) entre clés, aucune coupe.
         Pièces en vol : arcs paraboliques, décalage 0.08 s entre pièces.
SHOTS:   01 0-7.5   vitrine + téléphone ; rideau baisse + verrou rouge sur « ferme » (5.5)            | reads « compte, pas portefeuille »
         02 7.5-13.6 clé or sort du téléphone sur « clé » (9.2) ; pièces volent vers le coffre       | terme AUTO-GARDE à 12.3
         03 13.6-17.2 fissure rouge du téléphone sur « cassé » (15.5) ; clé se dissout en éclats     |
         04 17.2-25.6 24 tuiles en grille (gros plan sur 6) puis reforment la clé                     | terme PHRASE DE RÉCUPÉRATION à 23.7
         05 25.6-29.6 tuiles sur l'écran ; bug rouge grimpe et les aspire sur « malware » (27.5)     |
         06 29.6-38.6 boîtier matériel entre ; clé y entre ; flèche transaction → tampon SIGNÉ (34.3)  | terme PORTEFEUILLE MATÉRIEL à 36.8
         07 38.6-41.6 feuille de papier : flammes puis gouttes                                       |
         08 41.6-47.7 plaque acier gravée glisse au tiroir loin du boîtier                             | terme SAUVEGARDE MÉTAL à 46.0
         09 47.7-54.0 25e tuile apparaît (50.3) et s'envole hors champ                                | terme PASSPHRASE à 52.7
         10 54.0-58.3 vue éclatée : 5 pièces en colonne, étiquettes une à une sur leur mot            |
         11 58.3-64.6 bulle « Support » demande les 24 mots ; barrée rouge sur « demande » (62.9)    |
         12 64.6-71.2 recul : coffre fermé, boîtier, plaque ; titre final                             | « C'est un coffre dont toi seul as la clé. »
BANNED:  fond noir/bleu nuit, glow/bloom/néon, particules décoratives, dégradés violets, cartes vitrées, chips en pilule,
         trois cartes en ligne, tout centré-flottant, texte qui bouge pendant la lecture, logos de vraies plateformes, une vraie phrase de récupération.
QA:      frames 2.0, 5.8, 9.5, 15.6, 21.0, 27.6, 34.5, 40.0, 46.2, 51.0, 56.5, 63.0, 69.5 : objet héros ≥ 40 % de la largeur,
         sous-titre lisible dans la zone sûre (y ≤ 1248), terme nommé lisible, aucune image noire.
