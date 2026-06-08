from app import app, db, Match

matches = [

# Groupe A
("Mexico","South Africa",0,0),
("Korea Republic","Czechia",0,0),
("Czechia","South Africa",0,0),
("Mexico","Korea Republic",0,0),
("Czechia","Mexico",0,0),
("South Africa","Korea Republic",0,0),

# Groupe B
("Canada","Bosnia and Herzegovina",0,0),
("Qatar","Switzerland",0,0),
("Switzerland","Bosnia and Herzegovina",0,0),
("Canada","Qatar",0,0),
("Switzerland","Canada",0,0),
("Bosnia and Herzegovina","Qatar",0,0),

# Groupe C
("Brazil","Morocco",0,0),
("Haiti","Scotland",0,0),
("Scotland","Morocco",0,0),
("Brazil","Haiti",0,0),
("Scotland","Brazil",0,0),
("Morocco","Haiti",0,0),

# Groupe D
("USA","Paraguay",0,0),
("Australia","Türkiye",0,0),
("USA","Australia",0,0),
("Türkiye","Paraguay",0,0),
("Türkiye","USA",0,0),
("Paraguay","Australia",0,0),

# Groupe E
("Germany","Curaçao",0,0),
("Côte d'Ivoire","Ecuador",0,0),
("Germany","Côte d'Ivoire",0,0),
("Ecuador","Curaçao",0,0),
("Curaçao","Côte d'Ivoire",0,0),
("Ecuador","Germany",0,0),
]

with app.app_context():

    for team1, team2, score1, score2 in matches:

        match = Match(
            team1=team1,
            team2=team2,
            score1=score1,
            score2=score2
        )

        db.session.add(match)

    db.session.commit()

print("Matchs importés avec succès")