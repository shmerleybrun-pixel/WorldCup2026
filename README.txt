FoziFoot - Animation de but en direct

Fichiers inclus :
- app.py : ajoute /api/today-matches + correction MATCH_TIMEZONE si nécessaire.
- index.html : ajoute détection de nouveau but, animation GOOOAL, son léger et mise à jour automatique du score.

Installation :
1. Remplacer app.py à la racine du projet.
2. Remplacer templates/index.html par index.html.
3. Commit/push :
   git add .
   git commit -m "Add live goal alert on home page"
   git push

Fonctionnement :
- La page d'accueil appelle /api/today-matches toutes les 15 secondes.
- Si un score augmente, elle affiche une animation GOOOAL et met le match en surbrillance.
- Les scores doivent être mis à jour dans PostgreSQL par l'admin ou par ta synchronisation API-Football.
