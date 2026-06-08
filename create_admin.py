from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():

    admin = Admin.query.first()

    if admin:
        admin.username = "admin"
        admin.password = generate_password_hash("2026")
        print("Administrateur réinitialisé")

    else:
        admin = Admin(
            username="admin",
            password=generate_password_hash("2026")
        )

        db.session.add(admin)
        print("Administrateur créé")

    db.session.commit()

print("Terminé")