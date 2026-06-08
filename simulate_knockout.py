from app import app, db, KnockoutMatch, generate_next_round
import random

with app.app_context():

    rounds = [
        ("16es de finale", "8es de finale"),
        ("8es de finale", "Quarts de finale"),
        ("Quarts de finale", "Demi-finales"),
        ("Demi-finales", "Finale")
    ]

    for current_round, next_round in rounds:

        matches = KnockoutMatch.query.filter_by(
            round_name=current_round
        ).all()

        for match in matches:
            score1 = random.randint(1, 5)
            score2 = random.randint(0, 4)

            while score1 == score2:
                score2 = random.randint(0, 4)

            match.score1 = score1
            match.score2 = score2
            match.winner = match.team1 if score1 > score2 else match.team2

        db.session.commit()

        generate_next_round(current_round, next_round)

    print("Phase finale simulée avec succès.")