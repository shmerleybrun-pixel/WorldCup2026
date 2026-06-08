from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():

    admin = Admin.query.first()

    if admin:
        admin.password = generate_password_hash("2026")

        db.session.commit()

        print("Mot de passe chiffré avec succès.")
    else:
        print("Aucun administrateur trouvé.")