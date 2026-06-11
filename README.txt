# FoziFoot upgrade package

Contenu :
- app.py : fichier Flask complet corrigé
- templates/admin_users.html : nouvelle page admin utilisateurs

À copier dans le projet :
1. Remplace l'ancien app.py par ce app.py
2. Copie templates/admin_users.html dans ton dossier templates/
3. Fais :
   git add .
   git commit -m "Add FoziFoot admin users and security upgrades"
   git push
4. Render redéploiera automatiquement.

Routes ajoutées/améliorées :
- /admin/users
- /admin/users/export.csv
- /admin/users/delete/<id>
- Email HTML professionnel pour les codes de récupération
- Protection anti-spam reset password
- Force HTTPS sur Render
- Avertissement SECRET_KEY si valeur par défaut
