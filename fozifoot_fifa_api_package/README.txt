FOZIFOOT - Intégration API FIFA / Football

1) Remplacer votre app.py par ce fichier app.py.

2) Ajouter ces variables dans Render > Environment :

FOOTBALL_API_PROVIDER=api-football
FOOTBALL_API_KEY=votre_cle_api
FOOTBALL_API_LEAGUE_ID=1
FOOTBALL_API_SEASON=2026
FOOTBALL_API_UPDATE_LIVE=false

3) Déployer :

git add app.py
git commit -m "Add FIFA API sync for FoziFoot matches"
git push

4) Après déploiement, ouvrir :

https://fozifoot.com/admin/sync-fifa

5) Ajouter dans la navbar admin :

<li class="nav-item">
    <a class="nav-link text-success fw-bold {% if active_page == 'admin_sync_fifa' %}active{% endif %}" href="/admin/sync-fifa">
        Sync FIFA
    </a>
</li>

Notes :
- La route est protégée par admin_required.
- Les scores live ne sont pas écrits par défaut. Pour activer le live : FOOTBALL_API_UPDATE_LIVE=true
- L’intégration utilise API-Football/API-Sports v3 : /fixtures?league=1&season=2026
