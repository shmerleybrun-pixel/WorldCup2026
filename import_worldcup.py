from app import app, db, Match

print("Début import...")

matches = [

 # ======================
# GROUP A
# ======================

{
    "group_name":"A","match_number":1,
    "team1":"Mexico","team2":"South Africa",
    "match_date":"2026-06-11","match_time":"14:00",
    "stadium":"Mexico City Stadium","city":"Mexico City"
},
{
    "group_name":"A","match_number":2,
    "team1":"Korea Republic","team2":"Czechia",
    "match_date":"2026-06-11","match_time":"21:00",
    "stadium":"Guadalajara Stadium","city":"Guadalajara"
},
{
    "group_name":"A","match_number":25,
    "team1":"Czechia","team2":"South Africa",
    "match_date":"2026-06-18","match_time":"11:00",
    "stadium":"Atlanta Stadium","city":"Atlanta"
},
{
    "group_name":"A","match_number":28,
    "team1":"Mexico","team2":"Korea Republic",
    "match_date":"2026-06-18","match_time":"20:00",
    "stadium":"Guadalajara Stadium","city":"Guadalajara"
},
{
    "group_name":"A","match_number":53,
    "team1":"Czechia","team2":"Mexico",
    "match_date":"2026-06-24","match_time":"20:00",
    "stadium":"Mexico City Stadium","city":"Mexico City"
},
{
    "group_name":"A","match_number":54,
    "team1":"South Africa","team2":"Korea Republic",
    "match_date":"2026-06-24","match_time":"20:00",
    "stadium":"Monterrey Stadium","city":"Monterrey"
},

# ======================
# GROUP B
# ======================

{
    "group_name":"B","match_number":3,
    "team1":"Canada","team2":"Bosnia and Herzegovina",
    "match_date":"2026-06-12","match_time":"14:00",
    "stadium":"Toronto Stadium","city":"Toronto"
},
{
    "group_name":"B","match_number":8,
    "team1":"Qatar","team2":"Switzerland",
    "match_date":"2026-06-13","match_time":"14:00",
    "stadium":"San Francisco Bay Area Stadium","city":"San Francisco Bay Area"
},
{
    "group_name":"B","match_number":26,
    "team1":"Switzerland","team2":"Bosnia and Herzegovina",
    "match_date":"2026-06-18","match_time":"14:00",
    "stadium":"Los Angeles Stadium","city":"Los Angeles"
},
{
    "group_name":"B","match_number":27,
    "team1":"Canada","team2":"Qatar",
    "match_date":"2026-06-18","match_time":"17:00",
    "stadium":"BC Place Vancouver","city":"Vancouver"
},
{
    "group_name":"B","match_number":51,
    "team1":"Switzerland","team2":"Canada",
    "match_date":"2026-06-24","match_time":"14:00",
    "stadium":"BC Place Vancouver","city":"Vancouver"
},
{
    "group_name":"B","match_number":52,
    "team1":"Bosnia and Herzegovina","team2":"Qatar",
    "match_date":"2026-06-24","match_time":"14:00",
    "stadium":"Seattle Stadium","city":"Seattle"
},

# ======================
# GROUP C
# ======================

{
    "group_name":"C","match_number":7,
    "team1":"Brazil","team2":"Morocco",
    "match_date":"2026-06-13","match_time":"17:00",
    "stadium":"New York/New Jersey Stadium","city":"New York"
},
{
    "group_name":"C","match_number":5,
    "team1":"Haiti","team2":"Scotland",
    "match_date":"2026-06-13","match_time":"20:00",
    "stadium":"Boston Stadium","city":"Boston"
},
{
    "group_name":"C","match_number":30,
    "team1":"Scotland","team2":"Morocco",
    "match_date":"2026-06-19","match_time":"17:00",
    "stadium":"Boston Stadium","city":"Boston"
},
{
    "group_name":"C","match_number":29,
    "team1":"Brazil","team2":"Haiti",
    "match_date":"2026-06-19","match_time":"19:30",
    "stadium":"Philadelphia Stadium","city":"Philadelphia"
},
{
    "group_name":"C","match_number":49,
    "team1":"Scotland","team2":"Brazil",
    "match_date":"2026-06-24","match_time":"17:00",
    "stadium":"Miami Stadium","city":"Miami"
},
{
    "group_name":"C","match_number":50,
    "team1":"Morocco","team2":"Haiti",
    "match_date":"2026-06-24","match_time":"17:00",
    "stadium":"Atlanta Stadium","city":"Atlanta"
},

# ======================
# GROUP D
# ======================

{
    "group_name":"D","match_number":4,
    "team1":"USA","team2":"Paraguay",
    "match_date":"2026-06-12","match_time":"20:00",
    "stadium":"Los Angeles Stadium","city":"Los Angeles"
},
{
    "group_name":"D","match_number":6,
    "team1":"Australia","team2":"Türkiye",
    "match_date":"2026-06-13","match_time":"23:00",
    "stadium":"BC Place Vancouver","city":"Vancouver"
},
{
    "group_name":"D","match_number":32,
    "team1":"USA","team2":"Australia",
    "match_date":"2026-06-19","match_time":"14:00",
    "stadium":"Seattle Stadium","city":"Seattle"
},
{
    "group_name":"D","match_number":31,
    "team1":"Türkiye","team2":"Paraguay",
    "match_date":"2026-06-19","match_time":"22:00",
    "stadium":"San Francisco Bay Area Stadium","city":"San Francisco Bay Area"
},
{
    "group_name":"D","match_number":59,
    "team1":"Türkiye","team2":"USA",
    "match_date":"2026-06-25","match_time":"21:00",
    "stadium":"Los Angeles Stadium","city":"Los Angeles"
},
{
    "group_name":"D","match_number":60,
    "team1":"Paraguay","team2":"Australia",
    "match_date":"2026-06-25","match_time":"21:00",
    "stadium":"San Francisco Bay Area Stadium","city":"San Francisco Bay Area"
},
# ======================
# GROUP E
# ======================

{
    "group_name":"E","match_number":10,
    "team1":"Germany","team2":"Curaçao",
    "match_date":"2026-06-14","match_time":"12:00",
    "stadium":"Houston Stadium","city":"Houston"
},
{
    "group_name":"E","match_number":9,
    "team1":"Côte d'Ivoire","team2":"Ecuador",
    "match_date":"2026-06-14","match_time":"18:00",
    "stadium":"Philadelphia Stadium","city":"Philadelphia"
},
{
    "group_name":"E","match_number":33,
    "team1":"Germany","team2":"Côte d'Ivoire",
    "match_date":"2026-06-20","match_time":"15:00",
    "stadium":"Toronto Stadium","city":"Toronto"
},
{
    "group_name":"E","match_number":34,
    "team1":"Ecuador","team2":"Curaçao",
    "match_date":"2026-06-20","match_time":"19:00",
    "stadium":"Kansas City Stadium","city":"Kansas City"
},
{
    "group_name":"E","match_number":55,
    "team1":"Curaçao","team2":"Côte d'Ivoire",
    "match_date":"2026-06-25","match_time":"15:00",
    "stadium":"Philadelphia Stadium","city":"Philadelphia"
},
{
    "group_name":"E","match_number":56,
    "team1":"Ecuador","team2":"Germany",
    "match_date":"2026-06-25","match_time":"15:00",
    "stadium":"New York/New Jersey Stadium","city":"New York"
},

# ======================
# GROUP F
# ======================

{
    "group_name":"F","match_number":11,
    "team1":"Netherlands","team2":"Japan",
    "match_date":"2026-06-14","match_time":"15:00",
    "stadium":"Dallas Stadium","city":"Dallas"
},
{
    "group_name":"F","match_number":12,
    "team1":"Sweden","team2":"Tunisia",
    "match_date":"2026-06-14","match_time":"21:00",
    "stadium":"Monterrey Stadium","city":"Monterrey"
},
{
    "group_name":"F","match_number":35,
    "team1":"Netherlands","team2":"Sweden",
    "match_date":"2026-06-20","match_time":"12:00",
    "stadium":"Houston Stadium","city":"Houston"
},
{
    "group_name":"F","match_number":36,
    "team1":"Tunisia","team2":"Japan",
    "match_date":"2026-06-20","match_time":"23:00",
    "stadium":"Monterrey Stadium","city":"Monterrey"
},
{
    "group_name":"F","match_number":57,
    "team1":"Japan","team2":"Sweden",
    "match_date":"2026-06-25","match_time":"18:00",
    "stadium":"Dallas Stadium","city":"Dallas"
},
{
    "group_name":"F","match_number":58,
    "team1":"Tunisia","team2":"Netherlands",
    "match_date":"2026-06-25","match_time":"18:00",
    "stadium":"Kansas City Stadium","city":"Kansas City"
},

# ======================
# GROUP G
# ======================

{
    "group_name":"G","match_number":16,
    "team1":"Belgium","team2":"Egypt",
    "match_date":"2026-06-15","match_time":"14:00",
    "stadium":"Seattle Stadium","city":"Seattle"
},
{
    "group_name":"G","match_number":15,
    "team1":"IR Iran","team2":"New Zealand",
    "match_date":"2026-06-15","match_time":"20:00",
    "stadium":"Los Angeles Stadium","city":"Los Angeles"
},
{
    "group_name":"G","match_number":39,
    "team1":"Belgium","team2":"IR Iran",
    "match_date":"2026-06-21","match_time":"14:00",
    "stadium":"Los Angeles Stadium","city":"Los Angeles"
},
{
    "group_name":"G","match_number":40,
    "team1":"New Zealand","team2":"Egypt",
    "match_date":"2026-06-21","match_time":"20:00",
    "stadium":"BC Place Vancouver","city":"Vancouver"
},
{
    "group_name":"G","match_number":63,
    "team1":"Egypt","team2":"IR Iran",
    "match_date":"2026-06-26","match_time":"22:00",
    "stadium":"Seattle Stadium","city":"Seattle"
},
{
    "group_name":"G","match_number":64,
    "team1":"New Zealand","team2":"Belgium",
    "match_date":"2026-06-26","match_time":"22:00",
    "stadium":"BC Place Vancouver","city":"Vancouver"
},

# ======================
# GROUP H
# ======================

{
    "group_name":"H","match_number":14,
    "team1":"Spain","team2":"Cabo Verde",
    "match_date":"2026-06-15","match_time":"11:00",
    "stadium":"Atlanta Stadium","city":"Atlanta"
},
{
    "group_name":"H","match_number":13,
    "team1":"Saudi Arabia","team2":"Uruguay",
    "match_date":"2026-06-15","match_time":"17:00",
    "stadium":"Miami Stadium","city":"Miami"
},
{
    "group_name":"H","match_number":38,
    "team1":"Spain","team2":"Saudi Arabia",
    "match_date":"2026-06-21","match_time":"11:00",
    "stadium":"Atlanta Stadium","city":"Atlanta"
},
{
    "group_name":"H","match_number":37,
    "team1":"Uruguay","team2":"Cabo Verde",
    "match_date":"2026-06-21","match_time":"17:00",
    "stadium":"Miami Stadium","city":"Miami"
},
{
    "group_name":"H","match_number":65,
    "team1":"Cabo Verde","team2":"Saudi Arabia",
    "match_date":"2026-06-26","match_time":"19:00",
    "stadium":"Houston Stadium","city":"Houston"
},
{
    "group_name":"H","match_number":66,
    "team1":"Uruguay","team2":"Spain",
    "match_date":"2026-06-26","match_time":"19:00",
    "stadium":"Guadalajara Stadium","city":"Guadalajara"
},
# ======================
# GROUP I
# ======================

{
    "group_name":"I","match_number":17,
    "team1":"France","team2":"Senegal",
    "match_date":"2026-06-16","match_time":"14:00",
    "stadium":"New York/New Jersey Stadium","city":"New York"
},
{
    "group_name":"I","match_number":18,
    "team1":"Iraq","team2":"Norway",
    "match_date":"2026-06-16","match_time":"17:00",
    "stadium":"Boston Stadium","city":"Boston"
},
{
    "group_name":"I","match_number":42,
    "team1":"France","team2":"Iraq",
    "match_date":"2026-06-22","match_time":"16:00",
    "stadium":"Philadelphia Stadium","city":"Philadelphia"
},
{
    "group_name":"I","match_number":41,
    "team1":"Norway","team2":"Senegal",
    "match_date":"2026-06-22","match_time":"19:00",
    "stadium":"New York/New Jersey Stadium","city":"New York"
},
{
    "group_name":"I","match_number":61,
    "team1":"Norway","team2":"France",
    "match_date":"2026-06-26","match_time":"14:00",
    "stadium":"Boston Stadium","city":"Boston"
},
{
    "group_name":"I","match_number":62,
    "team1":"Senegal","team2":"Iraq",
    "match_date":"2026-06-26","match_time":"14:00",
    "stadium":"Toronto Stadium","city":"Toronto"
},

# ======================
# GROUP J
# ======================

{
    "group_name":"J","match_number":19,
    "team1":"Argentina","team2":"Algeria",
    "match_date":"2026-06-16","match_time":"20:00",
    "stadium":"Kansas City Stadium","city":"Kansas City"
},
{
    "group_name":"J","match_number":20,
    "team1":"Austria","team2":"Jordan",
    "match_date":"2026-06-16","match_time":"23:00",
    "stadium":"San Francisco Bay Area Stadium","city":"San Francisco Bay Area"
},
{
    "group_name":"J","match_number":43,
    "team1":"Argentina","team2":"Austria",
    "match_date":"2026-06-22","match_time":"12:00",
    "stadium":"Dallas Stadium","city":"Dallas"
},
{
    "group_name":"J","match_number":44,
    "team1":"Jordan","team2":"Algeria",
    "match_date":"2026-06-22","match_time":"22:00",
    "stadium":"San Francisco Bay Area Stadium","city":"San Francisco Bay Area"
},
{
    "group_name":"J","match_number":69,
    "team1":"Algeria","team2":"Austria",
    "match_date":"2026-06-27","match_time":"21:00",
    "stadium":"Kansas City Stadium","city":"Kansas City"
},
{
    "group_name":"J","match_number":70,
    "team1":"Jordan","team2":"Argentina",
    "match_date":"2026-06-27","match_time":"21:00",
    "stadium":"Dallas Stadium","city":"Dallas"
},

# ======================
# GROUP K
# ======================

{
    "group_name":"K","match_number":23,
    "team1":"Portugal","team2":"Congo DR",
    "match_date":"2026-06-17","match_time":"12:00",
    "stadium":"Houston Stadium","city":"Houston"
},
{
    "group_name":"K","match_number":24,
    "team1":"Uzbekistan","team2":"Colombia",
    "match_date":"2026-06-17","match_time":"21:00",
    "stadium":"Mexico City Stadium","city":"Mexico City"
},
{
    "group_name":"K","match_number":47,
    "team1":"Portugal","team2":"Uzbekistan",
    "match_date":"2026-06-23","match_time":"12:00",
    "stadium":"Houston Stadium","city":"Houston"
},
{
    "group_name":"K","match_number":48,
    "team1":"Colombia","team2":"Congo DR",
    "match_date":"2026-06-23","match_time":"21:00",
    "stadium":"Guadalajara Stadium","city":"Guadalajara"
},
{
    "group_name":"K","match_number":71,
    "team1":"Colombia","team2":"Portugal",
    "match_date":"2026-06-27","match_time":"18:30",
    "stadium":"Miami Stadium","city":"Miami"
},
{
    "group_name":"K","match_number":72,
    "team1":"Congo DR","team2":"Uzbekistan",
    "match_date":"2026-06-27","match_time":"18:30",
    "stadium":"Atlanta Stadium","city":"Atlanta"
},

# ======================
# GROUP L
# ======================

{
    "group_name":"L","match_number":22,
    "team1":"England","team2":"Croatia",
    "match_date":"2026-06-17","match_time":"15:00",
    "stadium":"Dallas Stadium","city":"Dallas"
},
{
    "group_name":"L","match_number":21,
    "team1":"Ghana","team2":"Panama",
    "match_date":"2026-06-17","match_time":"18:00",
    "stadium":"Toronto Stadium","city":"Toronto"
},
{
    "group_name":"L","match_number":45,
    "team1":"England","team2":"Ghana",
    "match_date":"2026-06-23","match_time":"15:00",
    "stadium":"Boston Stadium","city":"Boston"
},
{
    "group_name":"L","match_number":46,
    "team1":"Panama","team2":"Croatia",
    "match_date":"2026-06-23","match_time":"18:00",
    "stadium":"Toronto Stadium","city":"Toronto"
},
{
    "group_name":"L","match_number":67,
    "team1":"Panama","team2":"England",
    "match_date":"2026-06-27","match_time":"16:00",
    "stadium":"New York/New Jersey Stadium","city":"New York"
},
{
    "group_name":"L","match_number":68,
    "team1":"Croatia","team2":"Ghana",
    "match_date":"2026-06-27","match_time":"16:00",
    "stadium":"Philadelphia Stadium","city":"Philadelphia"
},

]

with app.app_context():

    # Facultatif : vide la table avant import
    Match.query.delete()
    db.session.commit()

    for m in matches:

        match = Match(
            group_name=m["group_name"],
            match_number=m["match_number"],
            team1=m["team1"],
            team2=m["team2"],
            score1=None,
            score2=None,
            match_date=m["match_date"],
            match_time=m["match_time"],
            stadium=m["stadium"],
            city=m["city"]
        )

        db.session.add(match)

    db.session.commit()

    print("Nombre de matchs :", Match.query.count())

print("Import terminé")