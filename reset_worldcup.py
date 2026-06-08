from app import app, db, Match, KnockoutMatch

with app.app_context():

    for match in Match.query.all():
        match.score1 = None
        match.score2 = None

    KnockoutMatch.query.delete()

    db.session.commit()

    print("Coupe du Monde réinitialisée.")