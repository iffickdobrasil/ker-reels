# ker-reels — médias vidéo Kermenhir pour Metricool

Repo **public** : les fichiers servent d'URL média à Metricool. **Rien de sensible.**

## Règles
- Vidéos : **MP4 (H.264 + AAC)**, vertical **1080×1920 (9:16)**.
- **Max ~50 Mo par fichier** (GitHub refuse au-delà de 100 Mo). Compresser. Pas de MOV ProRes.
- Nom de fichier **URL-safe** : minuscules, sans espaces ni accents, préfixe date + slug.
  Exemple : `2026-11-15_facade-crepuscule.mp4`
- Pas de visages de clients sans accord, pas de détails de sécurité, pas de zones en chantier.
- **Pas de musique sous copyright incrustée** (l'audio est ajouté in-app à la publication).

## URL du média (via jsDelivr)
```
https://cdn.jsdelivr.net/gh/iffickdobrasil/ker-reels@main/<fichier>
```
Exemple : `https://cdn.jsdelivr.net/gh/iffickdobrasil/ker-reels@main/2026-11-15_facade-crepuscule.mp4`

Le calendrier éditorial se tient dans `posts.csv` (une ligne par média). Laisser
`legende_fr` / `hashtags` vides pour que Claude les rédige.
