import os
import random
import string
import smtplib
from datetime import timedelta, date, datetime
from functools import wraps
from io import BytesIO
from email.message import EmailMessage

from zoneinfo import ZoneInfo

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    send_file,
    Response
)

from flask_babel import Babel, gettext as _
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.titan.email")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "465"))
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "custpriority@fozifoot.com")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MATCH_TIMEZONE = os.environ.get("MATCH_TIMEZONE", "America/New_York")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///worldcup.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = os.environ.get("SECRET_KEY", "worldcup2026_secret")
app.permanent_session_lifetime = timedelta(days=30)

app.config["BABEL_DEFAULT_LOCALE"] = "fr"
app.config["BABEL_SUPPORTED_LOCALES"] = ["fr", "en", "es"]

def get_locale():
    return session.get("lang", "fr")

babel = Babel(app, locale_selector=get_locale)

db = SQLAlchemy(app)


COUNTRY_CODES = {
    "Mexico": "mx",
    "South Africa": "za",
    "Korea Republic": "kr",
    "Czechia": "cz",
    "Canada": "ca",
    "Bosnia and Herzegovina": "ba",
    "Qatar": "qa",
    "Switzerland": "ch",
    "Brazil": "br",
    "Morocco": "ma",
    "Haiti": "ht",
    "Scotland": "gb-sct",
    "Germany": "de",
    "Curaçao": "cw",
    "Curacao": "cw",
    "Côte d'Ivoire": "ci",
    "Ecuador": "ec",
    "Argentina": "ar",
    "Algeria": "dz",
    "Austria": "at",
    "Jordan": "jo",
    "France": "fr",
    "Senegal": "sn",
    "Norway": "no",
    "New Zealand": "nz",
    "Belgium": "be",
    "Egypt": "eg",
    "Iran": "ir",
    "Chile": "cl",
    "Spain": "es",
    "Saudi Arabia": "sa",
    "Japan": "jp",
    "Uruguay": "uy",
    "England": "gb-eng",
    "Croatia": "hr",
    "Ghana": "gh",
    "Panama": "pa",
    "Portugal": "pt",
    "Uzbekistan": "uz",
    "Colombia": "co",
    "United Arab Emirates": "ae",
    "Netherlands": "nl",
    "Tunisia": "tn",
    "Paraguay": "py",
    "United States": "us",
    "USA": "us",
    "Australia": "au",
    "Türkiye": "tr",
    "Turkey": "tr",
    "Turkiye": "tr",
    "Iraq": "iq",
    "Sweden": "se",
    "Cabo Verde": "cv",
    "DR Congo": "cd",
    "Congo DR": "cd",
}


TEAMS = [
    "Canada", "Curaçao", "United States", "Haiti", "Mexico", "Panama",
    "Saudi Arabia", "Australia", "Iraq", "Japan", "Jordan", "Uzbekistan",
    "Qatar", "Korea Republic", "Iran",
    "South Africa", "Algeria", "Cabo Verde", "Côte d'Ivoire", "Egypt",
    "Ghana", "Morocco", "DR Congo", "Senegal", "Tunisia",
    "Argentina", "Brazil", "Colombia", "Ecuador", "Paraguay", "Uruguay",
    "New Zealand",
    "Germany", "England", "Austria", "Belgium", "Bosnia and Herzegovina",
    "Croatia", "Scotland", "France", "Spain", "Norway", "Netherlands",
    "Portugal", "Sweden", "Switzerland", "Czechia", "Türkiye",
]


TEAM_INFOS = {
    "Canada": {"capitale": "Ottawa", "langue": "Anglais, Français", "zone": "CONCACAF"},
    "Curaçao": {"capitale": "Willemstad", "langue": "Néerlandais, Papiamento", "zone": "CONCACAF"},
    "Curacao": {"capitale": "Willemstad", "langue": "Néerlandais, Papiamento", "zone": "CONCACAF"},
    "United States": {"capitale": "Washington D.C.", "langue": "Anglais", "zone": "CONCACAF"},
    "USA": {"capitale": "Washington D.C.", "langue": "Anglais", "zone": "CONCACAF"},
    "Haiti": {"capitale": "Port-au-Prince", "langue": "Créole haïtien, Français", "zone": "CONCACAF"},
    "Mexico": {"capitale": "Mexico", "langue": "Espagnol", "zone": "CONCACAF"},
    "Panama": {"capitale": "Panama", "langue": "Espagnol", "zone": "CONCACAF"},

    "Saudi Arabia": {"capitale": "Riyad", "langue": "Arabe", "zone": "AFC"},
    "Australia": {"capitale": "Canberra", "langue": "Anglais", "zone": "AFC"},
    "Iraq": {"capitale": "Bagdad", "langue": "Arabe, Kurde", "zone": "AFC"},
    "Japan": {"capitale": "Tokyo", "langue": "Japonais", "zone": "AFC"},
    "Jordan": {"capitale": "Amman", "langue": "Arabe", "zone": "AFC"},
    "Uzbekistan": {"capitale": "Tachkent", "langue": "Ouzbek", "zone": "AFC"},
    "Qatar": {"capitale": "Doha", "langue": "Arabe", "zone": "AFC"},
    "Korea Republic": {"capitale": "Séoul", "langue": "Coréen", "zone": "AFC"},
    "Iran": {"capitale": "Téhéran", "langue": "Persan", "zone": "AFC"},

    "South Africa": {"capitale": "Pretoria", "langue": "Anglais, Zoulou, Xhosa", "zone": "CAF"},
    "Algeria": {"capitale": "Alger", "langue": "Arabe, Amazigh", "zone": "CAF"},
    "Cabo Verde": {"capitale": "Praia", "langue": "Portugais", "zone": "CAF"},
    "Côte d'Ivoire": {"capitale": "Yamoussoukro", "langue": "Français", "zone": "CAF"},
    "Ivory Coast": {"capitale": "Yamoussoukro", "langue": "Français", "zone": "CAF"},
    "Egypt": {"capitale": "Le Caire", "langue": "Arabe", "zone": "CAF"},
    "Ghana": {"capitale": "Accra", "langue": "Anglais", "zone": "CAF"},
    "Morocco": {"capitale": "Rabat", "langue": "Arabe, Amazigh", "zone": "CAF"},
    "DR Congo": {"capitale": "Kinshasa", "langue": "Français", "zone": "CAF"},
    "Congo DR": {"capitale": "Kinshasa", "langue": "Français", "zone": "CAF"},
    "Democratic Republic of Congo": {"capitale": "Kinshasa", "langue": "Français", "zone": "CAF"},
    "Senegal": {"capitale": "Dakar", "langue": "Français", "zone": "CAF"},
    "Tunisia": {"capitale": "Tunis", "langue": "Arabe", "zone": "CAF"},

    "Argentina": {"capitale": "Buenos Aires", "langue": "Espagnol", "zone": "CONMEBOL"},
    "Brazil": {"capitale": "Brasília", "langue": "Portugais", "zone": "CONMEBOL"},
    "Colombia": {"capitale": "Bogotá", "langue": "Espagnol", "zone": "CONMEBOL"},
    "Ecuador": {"capitale": "Quito", "langue": "Espagnol", "zone": "CONMEBOL"},
    "Paraguay": {"capitale": "Asunción", "langue": "Espagnol, Guarani", "zone": "CONMEBOL"},
    "Uruguay": {"capitale": "Montevideo", "langue": "Espagnol", "zone": "CONMEBOL"},

    "New Zealand": {"capitale": "Wellington", "langue": "Anglais, Maori", "zone": "OFC"},

    "Germany": {"capitale": "Berlin", "langue": "Allemand", "zone": "UEFA"},
    "England": {"capitale": "Londres", "langue": "Anglais", "zone": "UEFA"},
    "Austria": {"capitale": "Vienne", "langue": "Allemand", "zone": "UEFA"},
    "Belgium": {"capitale": "Bruxelles", "langue": "Français, Néerlandais, Allemand", "zone": "UEFA"},
    "Bosnia and Herzegovina": {"capitale": "Sarajevo", "langue": "Bosnien, Croate, Serbe", "zone": "UEFA"},
    "Croatia": {"capitale": "Zagreb", "langue": "Croate", "zone": "UEFA"},
    "Scotland": {"capitale": "Édimbourg", "langue": "Anglais, Gaélique", "zone": "UEFA"},
    "France": {"capitale": "Paris", "langue": "Français", "zone": "UEFA"},
    "Spain": {"capitale": "Madrid", "langue": "Espagnol", "zone": "UEFA"},
    "Norway": {"capitale": "Oslo", "langue": "Norvégien", "zone": "UEFA"},
    "Netherlands": {"capitale": "Amsterdam", "langue": "Néerlandais", "zone": "UEFA"},
    "Portugal": {"capitale": "Lisbonne", "langue": "Portugais", "zone": "UEFA"},
    "Sweden": {"capitale": "Stockholm", "langue": "Suédois", "zone": "UEFA"},
    "Switzerland": {"capitale": "Berne", "langue": "Allemand, Français, Italien", "zone": "UEFA"},
    "Czechia": {"capitale": "Prague", "langue": "Tchèque", "zone": "UEFA"},
    "Türkiye": {"capitale": "Ankara", "langue": "Turc", "zone": "UEFA"},
    "Turkey": {"capitale": "Ankara", "langue": "Turc", "zone": "UEFA"},
    "Turkiye": {"capitale": "Ankara", "langue": "Turc", "zone": "UEFA"},
}


TEAM_ALIASES = {
    "Curaçao": ["Curaçao", "Curacao"],
    "Curacao": ["Curaçao", "Curacao"],
    "Türkiye": ["Türkiye", "Turkey", "Turkiye"],
    "Turkey": ["Türkiye", "Turkey", "Turkiye"],
    "Turkiye": ["Türkiye", "Turkey", "Turkiye"],
    "Côte d'Ivoire": ["Côte d'Ivoire", "Ivory Coast"],
    "Ivory Coast": ["Côte d'Ivoire", "Ivory Coast"],
    "DR Congo": ["DR Congo", "Congo DR", "Democratic Republic of Congo"],
    "Congo DR": ["DR Congo", "Congo DR", "Democratic Republic of Congo"],
    "United States": ["United States", "USA"],
    "USA": ["United States", "USA"],
    "Korea Republic": ["Korea Republic", "South Korea"],
    "South Korea": ["Korea Republic", "South Korea"],
}

def prediction_points(prediction):
    match = prediction.match

    if match.score1 is None or match.score2 is None:
        return 0

    if prediction.score1 == match.score1 and prediction.score2 == match.score2:
        return 3

    prediction_result = "draw"
    match_result = "draw"

    if prediction.score1 > prediction.score2:
        prediction_result = "team1"
    elif prediction.score2 > prediction.score1:
        prediction_result = "team2"

    if match.score1 > match.score2:
        match_result = "team1"
    elif match.score2 > match.score1:
        match_result = "team2"

    if prediction_result == match_result:
        return 1

    return 0


def match_is_open(match):
    """
    Retourne True si le match est encore ouvert aux pronostics.
    Règle FoziFoot : chaque match ferme 20 minutes avant son coup d'envoi.

    Les dates/heures des matchs sont lues depuis match.match_date et match.match_time.
    Par défaut, elles sont interprétées dans le fuseau America/New_York.
    Vous pouvez changer ce fuseau dans Render avec la variable MATCH_TIMEZONE.
    """

    try:
        if not match.match_date or not match.match_time:
            return False

        match_datetime = datetime.strptime(
            f"{match.match_date} {match.match_time}",
            "%Y-%m-%d %H:%M"
        )

        timezone = ZoneInfo(MATCH_TIMEZONE)
        match_datetime = match_datetime.replace(tzinfo=timezone)

        closing_datetime = match_datetime - timedelta(minutes=20)
        now = datetime.now(timezone)

        return now < closing_datetime

    except Exception:
        return False


@app.context_processor
def inject_global_template_data():
    """
    Données disponibles automatiquement dans toutes les pages
    qui incluent navbar.html.
    """

    total_points = 0
    pronostiqueurs_count = 0

    try:
        pronostiqueurs_count = db.session.query(
            Prediction.visitor_id
        ).distinct().count()
    except Exception:
        pronostiqueurs_count = 0

    if session.get("role") == "visitor":
        visitor = Visitor.query.get(session.get("visitor_id"))

        if visitor:
            for prediction in visitor.predictions:
                total_points += prediction_points(prediction)

    return dict(
        user_points=total_points,
        pronostiqueurs_count=pronostiqueurs_count,
        match_is_open=match_is_open
    )


@app.template_filter("country_code")
def country_code(team_name):
    return COUNTRY_CODES.get(str(team_name).strip(), "un")


@app.template_filter("date_fr")
def date_fr(date_string):
    mois = {
        "01": "janvier", "02": "février", "03": "mars",
        "04": "avril", "05": "mai", "06": "juin",
        "07": "juillet", "08": "août", "09": "septembre",
        "10": "octobre", "11": "novembre", "12": "décembre",
    }

    if not date_string:
        return ""

    try:
        annee = date_string[0:4]
        mois_num = date_string[5:7]
        jour = date_string[8:10]
        return f"{jour} {mois.get(mois_num, mois_num)} {annee}"
    except Exception:
        return date_string


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(2))
    match_number = db.Column(db.Integer)
    team1 = db.Column(db.String(100))
    team2 = db.Column(db.String(100))
    score1 = db.Column(db.Integer, nullable=True)
    score2 = db.Column(db.Integer, nullable=True)
    match_date = db.Column(db.String(30))
    match_time = db.Column(db.String(10))
    stadium = db.Column(db.String(150))
    city = db.Column(db.String(100))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))


class KnockoutMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_name = db.Column(db.String(50))
    team1 = db.Column(db.String(100))
    team2 = db.Column(db.String(100))
    score1 = db.Column(db.Integer, nullable=True)
    score2 = db.Column(db.Integer, nullable=True)
    winner = db.Column(db.String(100), nullable=True)
    match_order = db.Column(db.Integer)

class PlayerGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    player_name = db.Column(db.String(100))
    team = db.Column(db.String(100))

    goals = db.Column(db.Integer, default=0)

class PlayerAssist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    player_name = db.Column(db.String(100))
    team = db.Column(db.String(100))

    assists = db.Column(db.Integer, default=0)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    link = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))


class PrivateGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(120))
    creator_id = db.Column(db.Integer, db.ForeignKey("visitor.id"))


class PrivateGroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("private_group.id"))
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitor.id"))


class PredictionReceipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitor.id"))
    week_number = db.Column(db.Integer)
    created_at = db.Column(db.String(50))


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    visitor_id = db.Column(db.Integer, db.ForeignKey("visitor.id"))
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"))

    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)

    prediction_type = db.Column(db.String(20), default="public")
    private_group_id = db.Column(db.Integer, db.ForeignKey("private_group.id"), nullable=True)
    receipt_number = db.Column(db.String(50), nullable=True)

    visitor = db.relationship("Visitor", backref="predictions")
    match = db.relationship("Match", backref="predictions")

class PasswordResetCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitor.id"))
    code = db.Column(db.String(10))
    created_at = db.Column(db.String(50))

class LiveVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    embed_url = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=False)

def group_stage_complete():
    matchs_restants = Match.query.filter(
        (Match.score1 == None) | (Match.score2 == None)
    ).count()

    return matchs_restants == 0


def reset_knockout_table():
    KnockoutMatch.query.delete()
    db.session.commit()

def generate_group_code():
    while True:
        code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8
            )
        )

        existing_group = PrivateGroup.query.filter_by(code=code).first()

        if existing_group is None:
            return code

def send_reset_email(to_email, code):

    sender_email = os.environ.get("MAIL_USERNAME", MAIL_USERNAME)
    sender_password = os.environ.get("MAIL_PASSWORD", MAIL_PASSWORD)
    mail_server = os.environ.get("MAIL_SERVER", MAIL_SERVER)
    mail_port = int(os.environ.get("MAIL_PORT", MAIL_PORT))

    if not sender_email or not sender_password:
        print("ERREUR EMAIL : MAIL_USERNAME ou MAIL_PASSWORD manquant.")
        return False

    message = EmailMessage()
    message["Subject"] = "World Cup 2026 - Code de récupération"
    message["From"] = sender_email
    message["To"] = to_email

    message.set_content(f"""
Bonjour,

Votre code de récupération World Cup 2026 est :

{code}

Si vous n'avez pas demandé ce code, ignorez simplement cet email.

World Cup 2026
Contact : custpriority@fozifoot.com
WaZisTour LTD
""")

    try:
        with smtplib.SMTP_SSL(mail_server, mail_port) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)

        return True

    except Exception as e:
        print("ERREUR EMAIL :", e)
        return False

@app.route("/")
def home():
    today_db = date.today().isoformat()

    matchs_du_jour = Match.query.filter_by(
        match_date=today_db
    ).order_by(
        Match.match_time
    ).all()

    champion, finaliste, troisieme = get_podium()

    meilleur_buteur = PlayerGoal.query.order_by(
        PlayerGoal.goals.desc()
    ).first()

    meilleur_passeur = PlayerAssist.query.order_by(
        PlayerAssist.assists.desc()
    ).first()
    
    live_video = LiveVideo.query.filter_by(is_active=True).first()
    news = News.query.order_by(News.id.desc()).limit(3).all()

    return render_template(
        "index.html",
        matchs_du_jour=matchs_du_jour,
        today=date_fr(today_db),
        champion=champion,
        finaliste=finaliste,
        troisieme=troisieme,
        meilleur_buteur=meilleur_buteur,
        meilleur_passeur=meilleur_passeur,
        news=news,
        live_video=live_video,
        active_page="home"
    )


@app.route("/count")
def count():
    return str(Match.query.count())


@app.route("/groups")
def groups():
    matchs = Match.query.order_by(
        Match.group_name,
        Match.match_number
    ).all()

    groups = {}

    for match in matchs:
        groups.setdefault(match.group_name, []).append(match)

    return render_template("groups.html", groups=groups,
       active_page="groups"
    )

@app.route("/matches")
def matches():
    matchs = Match.query.order_by(Match.match_number).all()

    calendrier = {}

    matchs_calendrier = Match.query.order_by(
        Match.match_date,
        Match.match_time
    ).all()

    for match in matchs_calendrier:
        calendrier.setdefault(match.match_date, []).append(match)

    return render_template(
        "matches.html",
        matchs=matchs,
        calendrier=calendrier,
        active_page="matches"
    )


def get_group_rankings():
    matchs = Match.query.order_by(
        Match.group_name,
        Match.match_number
    ).all()

    groupes = {}

    for m in matchs:
        group = m.group_name
        groupes.setdefault(group, {})

        for team in [m.team1, m.team2]:
            if team not in groupes[group]:
                groupes[group][team] = {
                    "points": 0,
                    "played": 0,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "goals_for": 0,
                    "goals_against": 0,
                }

        if m.score1 is None or m.score2 is None:
            continue

        groupes[group][m.team1]["played"] += 1
        groupes[group][m.team2]["played"] += 1

        groupes[group][m.team1]["goals_for"] += m.score1
        groupes[group][m.team1]["goals_against"] += m.score2

        groupes[group][m.team2]["goals_for"] += m.score2
        groupes[group][m.team2]["goals_against"] += m.score1

        if m.score1 > m.score2:
            groupes[group][m.team1]["wins"] += 1
            groupes[group][m.team1]["points"] += 3
            groupes[group][m.team2]["losses"] += 1

        elif m.score2 > m.score1:
            groupes[group][m.team2]["wins"] += 1
            groupes[group][m.team2]["points"] += 3
            groupes[group][m.team1]["losses"] += 1

        else:
            groupes[group][m.team1]["draws"] += 1
            groupes[group][m.team2]["draws"] += 1
            groupes[group][m.team1]["points"] += 1
            groupes[group][m.team2]["points"] += 1

    groupes_sorted = {}

    for group, teams in groupes.items():
        groupes_sorted[group] = sorted(
            teams.items(),
            key=lambda x: (
                x[1]["points"],
                x[1]["goals_for"] - x[1]["goals_against"],
                x[1]["goals_for"],
            ),
            reverse=True
        )

    return groupes_sorted


@app.route("/standings")
def standings():
    groupes_sorted = get_group_rankings()
    return render_template("standings.html", groupes=groupes_sorted,
       active_page="standings"
    )

def get_qualified_teams():
    groupes = get_group_rankings()

    premiers = []
    deuxiemes = []
    troisiemes = []

    for group, teams in groupes.items():

        # Vérifier si tous les matchs du groupe sont joués
        matchs_groupe = Match.query.filter_by(group_name=group).all()

        groupe_termine = all(
            m.score1 is not None and m.score2 is not None
            for m in matchs_groupe
        )

        # Si le groupe n'est pas terminé, on ne qualifie personne
        if not groupe_termine:
            continue

        if len(teams) >= 1:
            premiers.append((group, teams[0][0], teams[0][1]))

        if len(teams) >= 2:
            deuxiemes.append((group, teams[1][0], teams[1][1]))

        if len(teams) >= 3:
            troisiemes.append((group, teams[2][0], teams[2][1]))

    meilleurs_troisiemes = sorted(
        troisiemes,
        key=lambda x: (
            x[2]["points"],
            x[2]["goals_for"] - x[2]["goals_against"],
            x[2]["goals_for"],
        ),
        reverse=True
    )[:8]

    qualifies = premiers + deuxiemes + meilleurs_troisiemes

    return premiers, deuxiemes, meilleurs_troisiemes, qualifies


def generate_knockout_matches():
    if not group_stage_complete():
        return

    if KnockoutMatch.query.count() > 0:
        return

    premiers, deuxiemes, meilleurs_troisiemes, qualifies = get_qualified_teams()

    if len(qualifies) < 32:
        return

    match_order = 1

    for i in range(0, 32, 2):
        match = KnockoutMatch(
            round_name="16es de finale",
            team1=qualifies[i][1],
            team2=qualifies[i + 1][1],
            match_order=match_order,
        )

        db.session.add(match)
        match_order += 1

    db.session.commit()

def get_prediction_weeks():
    matchs = Match.query.order_by(
        Match.match_date,
        Match.match_time
    ).all()

    dates = []

    for match in matchs:
        if match.match_date:
            try:
                dates.append(
                    datetime.strptime(match.match_date, "%Y-%m-%d").date()
                )
            except ValueError:
                pass

    if not dates:
        return []

    start_date = min(dates)
    end_date = max(dates)

    weeks = []
    week_number = 1
    current_start = start_date

    while current_start <= end_date:
        current_end = current_start + timedelta(days=6)

        weeks.append({
            "number": week_number,
            "start": current_start,
            "end": current_end,
            "start_str": current_start.isoformat(),
            "end_str": current_end.isoformat()
        })

        week_number += 1
        current_start = current_end + timedelta(days=1)

    return weeks


def generate_next_round(current_round, next_round):
    current_matches = KnockoutMatch.query.filter_by(
        round_name=current_round
    ).order_by(
        KnockoutMatch.match_order
    ).all()

    if not current_matches:
        return

    for match in current_matches:
        if not match.winner:
            return

    if KnockoutMatch.query.filter_by(round_name=next_round).count() > 0:
        return

    winners = [match.winner for match in current_matches]

    match_order = 1

    for i in range(0, len(winners), 2):
        if i + 1 >= len(winners):
            return

        new_match = KnockoutMatch(
            round_name=next_round,
            team1=winners[i],
            team2=winners[i + 1],
            match_order=match_order,
        )

        db.session.add(new_match)
        match_order += 1

    db.session.commit()


def generate_third_place_match():
    demi_matches = KnockoutMatch.query.filter_by(
        round_name="Demi-finales"
    ).order_by(
        KnockoutMatch.match_order
    ).all()

    if len(demi_matches) < 2:
        return

    for match in demi_matches:
        if not match.winner:
            return

    if KnockoutMatch.query.filter_by(
        round_name="Match pour la 3e place"
    ).count() > 0:
        return

    losers = []

    for match in demi_matches:
        if match.winner == match.team1:
            losers.append(match.team2)
        elif match.winner == match.team2:
            losers.append(match.team1)

    if len(losers) == 2:
        third_place = KnockoutMatch(
            round_name="Match pour la 3e place",
            team1=losers[0],
            team2=losers[1],
            match_order=1,
        )

        db.session.add(third_place)
        db.session.commit()

def get_podium():
    champion = None
    finaliste = None
    troisieme = None

    finale = KnockoutMatch.query.filter_by(
        round_name="Finale"
    ).first()

    if finale and finale.winner:
        champion = finale.winner

        if finale.winner == finale.team1:
            finaliste = finale.team2
        else:
            finaliste = finale.team1

    match_3e = KnockoutMatch.query.filter_by(
        round_name="Match pour la 3e place"
    ).first()

    if match_3e and match_3e.winner:
        troisieme = match_3e.winner

    return champion, finaliste, troisieme

def prediction_points(prediction):
    match = prediction.match

    if match.score1 is None or match.score2 is None:
        return 0

    # Score exact
    if prediction.score1 == match.score1 and prediction.score2 == match.score2:
        return 3

    # Bon résultat : victoire équipe 1
    if prediction.score1 > prediction.score2 and match.score1 > match.score2:
        return 1

    # Bon résultat : victoire équipe 2
    if prediction.score2 > prediction.score1 and match.score2 > match.score1:
        return 1

    # Bon résultat : match nul
    if prediction.score1 == prediction.score2 and match.score1 == match.score2:
        return 1

    return 0

def generate_receipt_number():

    last_receipt = PredictionReceipt.query.order_by(
        PredictionReceipt.id.desc()
    ).first()

    if not last_receipt:
        return "WC2026-000001"

    last_number = int(
        last_receipt.receipt_number.split("-")[1]
    )

    return f"WC2026-{last_number + 1:06d}"


@app.route("/knockout")
def knockout():
    matchs_restants = Match.query.filter(
        (Match.score1 == None) | (Match.score2 == None)
    ).count()

    premiers, deuxiemes, meilleurs_troisiemes, qualifies = get_qualified_teams()

    if matchs_restants == 0:
        generate_knockout_matches()

    knockout_matches = KnockoutMatch.query.order_by(
        KnockoutMatch.id
    ).all()

    champion, finaliste, troisieme = get_podium()

    return render_template(
        "knockout.html",
        premiers=premiers,
        deuxiemes=deuxiemes,
        meilleurs_troisiemes=meilleurs_troisiemes,
        knockout_matches=knockout_matches,
        champion=champion,
        finaliste=finaliste,
        troisieme=troisieme,
        matchs_restants=matchs_restants,
        active_page="knockout"
    )


@app.route("/stadiums")
def stadiums():
    stadiums = [
        {
            "name": "BC Place",
            "city": "Vancouver",
            "country": "Canada",
            "capacity": "54 000",
            "opened": "1983",
            "surface": "Pelouse naturelle FIFA 2026",
            "matches": "Phase de groupes, 16es et 8es de finale",
            "description": "Stade moderne doté d'un toit rétractable situé au cœur de Vancouver."
        },
        {
            "name": "Toronto Stadium (BMO Field)",
            "city": "Toronto",
            "country": "Canada",
            "capacity": "45 000",
            "opened": "2007",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes et 16es de finale",
            "description": "Principal stade de football de Toronto situé au bord du lac Ontario."
        },
        {
            "name": "Estadio Azteca",
            "city": "Mexico",
            "country": "Mexique",
            "capacity": "83 000",
            "opened": "1966",
            "surface": "Pelouse naturelle",
            "matches": "Match d'ouverture et phase de groupes",
            "description": "Stade légendaire ayant accueilli les finales des Coupes du Monde 1970 et 1986."
        },
        {
            "name": "Estadio BBVA",
            "city": "Monterrey",
            "country": "Mexique",
            "capacity": "53 500",
            "opened": "2015",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes et 16es de finale",
            "description": "L'un des stades les plus modernes d'Amérique du Nord."
        },
        {
            "name": "Estadio Akron",
            "city": "Guadalajara",
            "country": "Mexique",
            "capacity": "48 000",
            "opened": "2010",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes",
            "description": "Stade moderne à l'architecture inspirée des paysages volcaniques mexicains."
        },
        {
            "name": "MetLife Stadium",
            "city": "New York / New Jersey",
            "country": "États-Unis",
            "capacity": "82 500",
            "opened": "2010",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Finale",
            "description": "Stade choisi pour accueillir la grande finale du Mondial 2026."
        },
        {
            "name": "AT&T Stadium",
            "city": "Dallas",
            "country": "États-Unis",
            "capacity": "80 000",
            "opened": "2009",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Phase finale",
            "description": "Immense stade moderne situé à Arlington, Texas."
        },
        {
            "name": "SoFi Stadium",
            "city": "Los Angeles",
            "country": "États-Unis",
            "capacity": "70 000",
            "opened": "2020",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade ultramoderne situé à Inglewood, Californie."
        },
        {
            "name": "Mercedes-Benz Stadium",
            "city": "Atlanta",
            "country": "États-Unis",
            "capacity": "71 000",
            "opened": "2017",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade moderne connu pour son toit circulaire rétractable."
        },
        {
            "name": "NRG Stadium",
            "city": "Houston",
            "country": "États-Unis",
            "capacity": "72 000",
            "opened": "2002",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade texan doté d'un toit rétractable."
        },
        {
            "name": "Lincoln Financial Field",
            "city": "Philadelphia",
            "country": "États-Unis",
            "capacity": "69 000",
            "opened": "2003",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes et 16es de finale",
            "description": "Stade emblématique de Philadelphie."
        },
        {
            "name": "Lumen Field",
            "city": "Seattle",
            "country": "États-Unis",
            "capacity": "68 000",
            "opened": "2002",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade réputé pour son ambiance exceptionnelle."
        },
        {
            "name": "Levi's Stadium",
            "city": "San Francisco Bay Area",
            "country": "États-Unis",
            "capacity": "68 500",
            "opened": "2014",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade moderne situé à Santa Clara."
        },
        {
            "name": "Arrowhead Stadium",
            "city": "Kansas City",
            "country": "États-Unis",
            "capacity": "76 000",
            "opened": "1972",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes",
            "description": "Stade célèbre pour l'intensité de son public."
        },
        {
            "name": "Gillette Stadium",
            "city": "Boston",
            "country": "États-Unis",
            "capacity": "65 000",
            "opened": "2002",
            "surface": "Pelouse naturelle FIFA",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade situé à Foxborough, près de Boston."
        },
        {
            "name": "Hard Rock Stadium",
            "city": "Miami",
            "country": "États-Unis",
            "capacity": "65 000",
            "opened": "1987",
            "surface": "Pelouse naturelle",
            "matches": "Phase de groupes et phase finale",
            "description": "Stade majeur de Miami Gardens, en Floride."
        },
    ]

    return render_template("stadiums.html", stadiums=stadiums,
         active_page="stadiums"
    )
   

@app.route("/equipes")
def equipes():
    return render_template(
        "equipes.html",
        teams=TEAMS,
        team_infos=TEAM_INFOS,
        active_page="equipes"
    )


@app.route("/equipe/<team_name>")
def equipe_detail(team_name):
    noms_possibles = TEAM_ALIASES.get(team_name, [team_name])

    matchs = Match.query.filter(
        (Match.team1.in_(noms_possibles)) | (Match.team2.in_(noms_possibles))
    ).order_by(Match.match_number).all()

    infos = TEAM_INFOS.get(team_name, {
        "capitale": "Non disponible",
        "langue": "Non disponible",
        "zone": "Non disponible"
    })

    played = 0
    wins = 0
    draws = 0
    losses = 0
    goals_for = 0
    goals_against = 0
    points = 0

    for match in matchs:
        if match.score1 is None or match.score2 is None:
            continue

        played += 1

        if match.team1 in noms_possibles:
            gf = match.score1
            ga = match.score2
        else:
            gf = match.score2
            ga = match.score1

        goals_for += gf
        goals_against += ga

        if gf > ga:
            wins += 1
            points += 3
        elif gf == ga:
            draws += 1
            points += 1
        else:
            losses += 1

    stats = {
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "difference": goals_for - goals_against,
        "points": points
    }

    return render_template(
        "equipe_detail.html",
        team_name=team_name,
        infos=infos,
        matchs=matchs,
        stats=stats
    )


@app.route("/statistiques")
def statistiques():
    matchs = Match.query.all()

    matchs_joues = [
        m for m in matchs
        if m.score1 is not None and m.score2 is not None
    ]

    total_matchs = len(matchs)
    matchs_joues_count = len(matchs_joues)
    matchs_non_joues = total_matchs - matchs_joues_count
    total_buts = sum(m.score1 + m.score2 for m in matchs_joues)

    moyenne_buts = 0
    if matchs_joues_count > 0:
        moyenne_buts = round(total_buts / matchs_joues_count, 2)

    stats_equipes = {}

    for match in matchs_joues:
        for team in [match.team1, match.team2]:
            if team not in stats_equipes:
                stats_equipes[team] = {
                    "buts_marques": 0,
                    "buts_encaisses": 0,
                    "points": 0,
                    "victoires": 0,
                    "nuls": 0,
                    "defaites": 0,
                }

        stats_equipes[match.team1]["buts_marques"] += match.score1
        stats_equipes[match.team1]["buts_encaisses"] += match.score2

        stats_equipes[match.team2]["buts_marques"] += match.score2
        stats_equipes[match.team2]["buts_encaisses"] += match.score1

        if match.score1 > match.score2:
            stats_equipes[match.team1]["points"] += 3
            stats_equipes[match.team1]["victoires"] += 1
            stats_equipes[match.team2]["defaites"] += 1

        elif match.score2 > match.score1:
            stats_equipes[match.team2]["points"] += 3
            stats_equipes[match.team2]["victoires"] += 1
            stats_equipes[match.team1]["defaites"] += 1

        else:
            stats_equipes[match.team1]["points"] += 1
            stats_equipes[match.team2]["points"] += 1
            stats_equipes[match.team1]["nuls"] += 1
            stats_equipes[match.team2]["nuls"] += 1

    meilleure_attaque = sorted(
        stats_equipes.items(),
        key=lambda x: x[1]["buts_marques"],
        reverse=True
    )[:10]

    meilleure_defense = sorted(
        stats_equipes.items(),
        key=lambda x: x[1]["buts_encaisses"]
    )[:10]

    plus_de_points = sorted(
        stats_equipes.items(),
        key=lambda x: x[1]["points"],
        reverse=True
    )[:10]

    plus_de_victoires = sorted(
        stats_equipes.items(),
        key=lambda x: x[1]["victoires"],
        reverse=True
    )[:10]

    match_plus_buts = None

    if matchs_joues:
        match_plus_buts = max(
            matchs_joues,
            key=lambda m: m.score1 + m.score2
        )

    plus_grosse_victoire = None

    if matchs_joues:
        plus_grosse_victoire = max(
            matchs_joues,
            key=lambda m: abs(m.score1 - m.score2)
        )
    
    
    meilleur_buteur = PlayerGoal.query.order_by(
    PlayerGoal.goals.desc()
    ).first()

    meilleur_passeur = PlayerAssist.query.order_by(
    PlayerAssist.assists.desc()
    ).first()
    
    classement_general = []

    groupes = get_group_rankings()

    for group, teams in groupes.items():
        for team_name, stats in teams:

            classement_general.append({
                "team": team_name,
                "group": group,
                "points": stats["points"],
                "played": stats["played"],
                "wins": stats["wins"],
                "draws": stats["draws"],
                "losses": stats["losses"],
                "goals_for": stats["goals_for"],
                "goals_against": stats["goals_against"],
                "difference": stats["goals_for"] - stats["goals_against"]
            })

    classement_general = sorted(
        classement_general,
        key=lambda x: (
            x["points"],
            x["difference"],
            x["goals_for"]
        ),
        reverse=True
    )

    return render_template(
        "statistiques.html",
        total_matchs=total_matchs,
        matchs_joues_count=matchs_joues_count,
        matchs_non_joues=matchs_non_joues,
        total_buts=total_buts,
        moyenne_buts=moyenne_buts,
        meilleure_attaque=meilleure_attaque,
        meilleure_defense=meilleure_defense,
        plus_de_points=plus_de_points,
        plus_de_victoires=plus_de_victoires,
        match_plus_buts=match_plus_buts,
        meilleur_buteur=meilleur_buteur,
        meilleur_passeur=meilleur_passeur,
        classement_general=classement_general,
        plus_grosse_victoire=plus_grosse_victoire,
        active_page="statistiques"
    )


# =====================================================
# PROTECTION ADMIN
# =====================================================

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# =====================================================
# PROTECTION UTILISATEUR CONNECTÉ
# =====================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") not in ["admin", "visitor"]:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# =====================================================
# CONNEXION UNIQUE ADMIN + VISITEUR
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["email_or_username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session.clear()
            session.permanent = True
            session["role"] = "admin"
            session["admin"] = True
            return redirect("/admin/matchs")

        visitor = Visitor.query.filter_by(email=username).first()

        if visitor and check_password_hash(visitor.password, password):
            session.clear()
            session.permanent = True
            session["role"] = "visitor"
            session["visitor_id"] = visitor.id
            session["visitor_name"] = visitor.full_name
            return redirect("/predictions")
 
        return "Identifiant ou mot de passe incorrect."

    return render_template("login.html")


@app.route("/admin")
def admin_redirect():
    return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/logout-visiteur")
def logout_visiteur():
    return redirect("/logout")


# =====================================================
# ADMIN MATCHS
# =====================================================

@app.route("/admin/matchs", methods=["GET", "POST"])
@admin_required
def admin_matchs():
    matchs = Match.query.order_by(Match.match_number).all()

    if request.method == "POST":
        scores_changed = False

        for match in matchs:
            score1 = request.form.get(f"score1_{match.id}")
            score2 = request.form.get(f"score2_{match.id}")

            old_score1 = match.score1
            old_score2 = match.score2

            if score1 != "" and score2 != "":
                try:
                    match.score1 = int(score1)
                    match.score2 = int(score2)
                except ValueError:
                    continue

            elif score1 == "" and score2 == "":
                match.score1 = None
                match.score2 = None

            if old_score1 != match.score1 or old_score2 != match.score2:
                scores_changed = True

        db.session.commit()

        if scores_changed:
            reset_knockout_table()

        return redirect("/admin/matchs")

    return render_template(
        "admin_matchs.html",
        matchs=matchs,
        active_page="admin_matchs"
    )


# =====================================================
# ADMIN SETTINGS
# =====================================================

@app.route("/admin/settings", methods=["GET", "POST"])
@admin_required
def admin_settings():
    admin_user = Admin.query.first()

    if admin_user is None:
        admin_user = Admin(
            username="admin",
            password=generate_password_hash("admin123"),
        )
        db.session.add(admin_user)
        db.session.commit()

    if request.method == "POST":
        admin_user.username = request.form["username"]
        new_password = request.form["password"]

        if new_password:
            admin_user.password = generate_password_hash(new_password)

        db.session.commit()
        return redirect("/admin/settings")

    return render_template(
        "admin_settings.html",
        admin=admin_user,
        active_page="admin_settings"
    )


# =====================================================
# ADMIN PHASE FINALE
# =====================================================

@app.route("/admin/knockout", methods=["GET", "POST"])
@admin_required
def admin_knockout():
    matchs_restants = Match.query.filter(
        (Match.score1 == None) | (Match.score2 == None)
    ).count()

    if matchs_restants == 0:
        generate_knockout_matches()

    knockout_matches = KnockoutMatch.query.order_by(
        KnockoutMatch.id
    ).all()

    if request.method == "POST":
        for match in knockout_matches:
            score1 = request.form.get(f"score1_{match.id}")
            score2 = request.form.get(f"score2_{match.id}")
            winner_manual = request.form.get(f"winner_{match.id}")

            if score1 != "" and score2 != "":
                try:
                    match.score1 = int(score1)
                    match.score2 = int(score2)
                except ValueError:
                    continue

                if match.score1 > match.score2:
                    match.winner = match.team1

                elif match.score2 > match.score1:
                    match.winner = match.team2

                else:
                    if winner_manual in [match.team1, match.team2]:
                        match.winner = winner_manual
                    else:
                        match.winner = None

            elif score1 == "" and score2 == "":
                match.score1 = None
                match.score2 = None
                match.winner = None

        db.session.commit()

        generate_next_round("16es de finale", "8es de finale")
        generate_next_round("8es de finale", "Quarts de finale")
        generate_next_round("Quarts de finale", "Demi-finales")
        generate_next_round("Demi-finales", "Finale")
        generate_third_place_match()

        return redirect("/admin/knockout")

    return render_template(
        "admin_knockout.html",
        knockout_matches=knockout_matches,
        active_page="admin_knockout"
    )


@app.route("/admin/reset-knockout")
@admin_required
def reset_knockout():
    reset_knockout_table()
    return redirect("/admin/knockout")


# =====================================================
# BUTEURS
# =====================================================

@app.route("/buteurs")
def buteurs():
    joueurs = PlayerGoal.query.order_by(
        PlayerGoal.goals.desc(),
        PlayerGoal.player_name
    ).all()

    return render_template(
        "buteurs.html",
        joueurs=joueurs,
        active_page="buteurs"
    )


@app.route("/admin/buteurs", methods=["GET", "POST"])
@admin_required
def admin_buteurs():
    if request.method == "POST":
        player_name = request.form["player_name"]
        team = request.form["team"]
        goals = request.form["goals"]

        if player_name and team:
            joueur = PlayerGoal(
                player_name=player_name,
                team=team,
                goals=int(goals)
            )

            db.session.add(joueur)
            db.session.commit()

        return redirect("/admin/buteurs")

    joueurs = PlayerGoal.query.order_by(
        PlayerGoal.goals.desc()
    ).all()

    return render_template(
        "admin_buteurs.html",
        joueurs=joueurs,
        teams=TEAMS,
        active_page="admin_buteurs"
    )


@app.route("/admin/buteurs/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_buteur(id):
    joueur = PlayerGoal.query.get_or_404(id)

    if request.method == "POST":
        joueur.player_name = request.form["player_name"]
        joueur.team = request.form["team"]
        joueur.goals = int(request.form["goals"])

        db.session.commit()
        return redirect("/admin/buteurs")

    return render_template("edit_buteur.html", joueur=joueur)


@app.route("/admin/buteurs/delete/<int:id>")
@admin_required
def delete_buteur(id):
    joueur = PlayerGoal.query.get_or_404(id)

    db.session.delete(joueur)
    db.session.commit()

    return redirect("/admin/buteurs")


# =====================================================
# PASSEURS
# =====================================================

@app.route("/passeurs")
def passeurs():
    joueurs = PlayerAssist.query.order_by(
        PlayerAssist.assists.desc(),
        PlayerAssist.player_name
    ).all()

    return render_template(
        "passeurs.html",
        joueurs=joueurs,
        active_page="passeurs"
    )


@app.route("/admin/passeurs", methods=["GET", "POST"])
@admin_required
def admin_passeurs():
    if request.method == "POST":
        joueur = PlayerAssist(
            player_name=request.form["player_name"],
            team=request.form["team"],
            assists=int(request.form["assists"])
        )

        db.session.add(joueur)
        db.session.commit()

        return redirect("/admin/passeurs")

    joueurs = PlayerAssist.query.order_by(
        PlayerAssist.assists.desc()
    ).all()

    return render_template(
        "admin_passeurs.html",
        joueurs=joueurs,
        teams=TEAMS,
        active_page="admin_passeurs"
    )


@app.route("/admin/passeurs/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_passeur(id):
    joueur = PlayerAssist.query.get_or_404(id)

    if request.method == "POST":
        joueur.player_name = request.form["player_name"]
        joueur.team = request.form["team"]
        joueur.assists = int(request.form["assists"])

        db.session.commit()
        return redirect("/admin/passeurs")

    return render_template(
        "edit_passeur.html",
        joueur=joueur
    )


@app.route("/admin/passeurs/delete/<int:id>")
@admin_required
def delete_passeur(id):
    joueur = PlayerAssist.query.get_or_404(id)

    db.session.delete(joueur)
    db.session.commit()

    return redirect("/admin/passeurs")


# =====================================================
# PAGES HISTOIRE / ANECDOTES
# =====================================================

@app.route("/cup1")
def cup1():
    return render_template("cup1.html")


@app.route("/anecdotes")
def anecdotes():
    return render_template("anecdotes.html")


# =====================================================
# INSCRIPTION VISITEUR
# =====================================================

@app.route("/register", methods=["GET", "POST"])
def visitor_register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_visitor = Visitor.query.filter_by(
            email=email
        ).first()

        if existing_visitor:
            return render_template(
                "register.html",
                error="Cet email est déjà utilisé."
            )

        visitor = Visitor(
            full_name=full_name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(visitor)
        db.session.commit()

        session.clear()
        session.permanent = True

        session["role"] = "visitor"
        session["visitor_id"] = visitor.id
        session["visitor_name"] = visitor.full_name

        return redirect("/predictions")

    return render_template(
        "register.html",
        active_page="register"
    )

# =====================================================
# PRÉDICTIONS
# =====================================================

@app.route("/predictions", methods=["GET", "POST"])
@login_required
def predictions():
    weeks = get_prediction_weeks()

    selected_week = request.args.get("week", "1")
    prediction_type = request.args.get("type", "public")

    try:
        selected_week = int(selected_week)
    except ValueError:
        selected_week = 1

    current_week = None
    matchs = []

    if weeks:
        current_week = next(
            (week for week in weeks if week["number"] == selected_week),
            weeks[0]
        )

        matchs = Match.query.filter(
            Match.match_date >= current_week["start_str"],
            Match.match_date <= current_week["end_str"]
        ).order_by(
            Match.match_date,
            Match.match_time,
            Match.match_number
        ).all()

    today = date.today()
    week_is_open = False
    opening_date = None
    closing_date = None

    if current_week:
        opening_date = current_week["start"] - timedelta(days=3)
        closing_date = current_week["end"]
        week_is_open = opening_date <= today <= closing_date

    if session.get("role") == "admin":
        visitor_id = None
    else:
        visitor_id = session.get("visitor_id")

    if session.get("role") == "visitor" and not visitor_id:
        session.clear()
        return redirect("/login")

    if request.method == "POST":
        if session.get("role") == "admin":
            return redirect(f"/predictions?week={selected_week}&type=public")

        if not week_is_open:
            return redirect(f"/predictions?week={selected_week}&type=public")

        receipt_number = generate_receipt_number()
        has_prediction = False

        for match in matchs:
            if not match_is_open(match):
                continue

            score1 = request.form.get(f"score1_{match.id}")
            score2 = request.form.get(f"score2_{match.id}")

            if not score1 or not score2:
                continue

            prediction = Prediction.query.filter_by(
                visitor_id=visitor_id,
                match_id=match.id,
                prediction_type="public"
            ).first()

            if prediction is None:
                prediction = Prediction(
                    visitor_id=visitor_id,
                    match_id=match.id,
                    prediction_type="public",
                    private_group_id=None
                )
                db.session.add(prediction)

            prediction.score1 = int(score1)
            prediction.score2 = int(score2)
            prediction.receipt_number = receipt_number
            has_prediction = True

        if not has_prediction:
            return redirect(f"/predictions?week={selected_week}&type=public")

        receipt = PredictionReceipt(
            receipt_number=receipt_number,
            visitor_id=visitor_id,
            week_number=selected_week,
            created_at=str(datetime.now())
        )

        db.session.add(receipt)
        db.session.commit()

        return redirect(f"/receipt/{receipt.id}")

    if visitor_id:
        predictions_saved = Prediction.query.filter_by(
            visitor_id=visitor_id,
            prediction_type="public"
        ).all()
    else:
        predictions_saved = []

    prediction_map = {
        prediction.match_id: prediction
        for prediction in predictions_saved
    }

    return render_template(
        "predictions.html",
        matchs=matchs,
        prediction_map=prediction_map,
        visitor_name=session.get("visitor_name"),
        weeks=weeks,
        current_week=current_week,
        selected_week=selected_week,
        week_is_open=week_is_open,
        opening_date=opening_date,
        closing_date=closing_date,
        prediction_type=prediction_type,
        active_page="predictions"
    )

@app.route("/admin/dashboard")
def admin_dashboard():

    if session.get("role") != "admin":
        return redirect("/login")

    total_visitors = Visitor.query.count()

    total_predictions = Prediction.query.count()

    total_groups = PrivateGroup.query.count()

    total_matches = Match.query.count()

    matches_played = Match.query.filter(
        Match.score1.isnot(None),
        Match.score2.isnot(None)
    ).count()

    return render_template(
        "admin_dashboard.html",
        total_visitors=total_visitors,
        total_predictions=total_predictions,
        total_groups=total_groups,
        total_matches=total_matches,
        matches_played=matches_played,
        active_page="admin_dashboard"
    )

@app.route("/pronostics")
@login_required
def pronostics_home():
    return render_template(
        "pronostics_home.html",
        active_page="predictions"
    )

@app.route("/groupes-prives", methods=["GET", "POST"])
@login_required
def groupes_prives():

    if session.get("role") != "visitor":
        return redirect("/login")

    visitor_id = session["visitor_id"]

    if request.method == "POST":
        group_name = request.form.get("group_name")

        if group_name:
            group = PrivateGroup(
                name=group_name,
                code=generate_group_code(),
                creator_id=visitor_id
            )

            db.session.add(group)
            db.session.commit()

            member = PrivateGroupMember(
                group_id=group.id,
                visitor_id=visitor_id
            )

            db.session.add(member)
            db.session.commit()

            return redirect(f"/groupe/{group.code}")

    memberships = PrivateGroupMember.query.filter_by(
        visitor_id=visitor_id
    ).all()

    group_ids = [m.group_id for m in memberships]

    groups = PrivateGroup.query.filter(
        PrivateGroup.id.in_(group_ids)
    ).all() if group_ids else []

    return render_template(
        "groupes_prives.html",
        groups=groups,
        active_page="predictions"
    )

@app.route("/groupe/<code>")
@login_required
def groupe_detail(code):

    if session.get("role") != "visitor":
        return redirect("/login")

    group = PrivateGroup.query.filter_by(code=code).first_or_404()

    visitor_id = session["visitor_id"]

    existing_member = PrivateGroupMember.query.filter_by(
        group_id=group.id,
        visitor_id=visitor_id
    ).first()

    if existing_member is None:
        member = PrivateGroupMember(
            group_id=group.id,
            visitor_id=visitor_id
        )

        db.session.add(member)
        db.session.commit()

    members = PrivateGroupMember.query.filter_by(
        group_id=group.id
    ).all()

    return render_template(
        "groupe_detail.html",
        group=group,
        members=members,
        active_page="predictions"
    )

@app.route("/receipt/<int:receipt_id>")
@login_required
def receipt(receipt_id):

    receipt = PredictionReceipt.query.get_or_404(
        receipt_id
    )

    visitor = Visitor.query.get(
        receipt.visitor_id
    )

    predictions = Prediction.query.filter_by(
        visitor_id=receipt.visitor_id,
        receipt_number=receipt.receipt_number
    ).all()

    return render_template(
        "receipt.html",
        receipt=receipt,
        visitor=visitor,
        predictions=predictions
    )

@app.route("/download-receipt/<int:receipt_id>")
@login_required
def download_receipt(receipt_id):

    receipt = PredictionReceipt.query.get_or_404(receipt_id)

    visitor = Visitor.query.get(receipt.visitor_id)

    weeks = get_prediction_weeks()

    current_week = next(
        (week for week in weeks if week["number"] == receipt.week_number),
        None
    )

    if current_week:
        predictions = Prediction.query.join(Match).filter(
            Prediction.visitor_id == receipt.visitor_id,
            Match.match_date >= current_week["start_str"],
            Match.match_date <= current_week["end_str"],
            Prediction.prediction_type == "public"
        ).order_by(
            Match.match_date,
            Match.match_time,
            Match.match_number
        ).all()
    else:
        predictions = []

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=120,
        leftMargin=120,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
   
    from reportlab.lib.enums import TA_CENTER

    styles["Title"].alignment = TA_CENTER
    styles["Heading2"].alignment = TA_CENTER
    styles["Heading3"].alignment = TA_CENTER
    styles["Heading4"].alignment = TA_CENTER

    elements = []

    elements.append(
        Paragraph(
            "WORLD CUP 2026",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Reçu officiel de pronostic",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"N° : {receipt.receipt_number}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Nom : {visitor.full_name}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Semaine : {receipt.week_number}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Date : {receipt.created_at}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "PRONOSTICS",
            styles["Heading3"]
        )
    )

    elements.append(Spacer(1, 10))

    if predictions:
        for prediction in predictions:

            match = Match.query.get(prediction.match_id)

            if match:

                texte = (
                    f"<b>Match {match.match_number}</b><br/>"
                    f"{match.team1} {prediction.score1} - {prediction.score2} {match.team2}<br/>"
                    f"{match.match_date} | {match.match_time}"
                )

                elements.append(
                    Paragraph(
                        texte,
                        styles["BodyText"]
                    )
                )

                elements.append(Spacer(1, 6))
    else:
        elements.append(
            Paragraph(
                "Aucun pronostic trouvé pour cette semaine.",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Code de vérification : {receipt.receipt_number}",
            styles["Heading4"]
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{receipt.receipt_number}.pdf",
        mimetype="application/pdf"
    )

@app.route("/groupe/<code>/classement")
@login_required
def groupe_classement(code):

    if session.get("role") != "visitor":
        return redirect("/login")

    group = PrivateGroup.query.filter_by(code=code).first_or_404()

    members = PrivateGroupMember.query.filter_by(
        group_id=group.id
    ).all()

    classement = []

    for member in members:
        visitor = Visitor.query.get(member.visitor_id)

        total_points = 0
        exact_scores = 0
        bons_resultats = 0
        total_predictions = 0

        predictions = Prediction.query.filter_by(
            visitor_id=visitor.id,
            prediction_type="private",
            private_group_id=group.id
        ).all()

        for prediction in predictions:
            points = prediction_points(prediction)

            if prediction.match.score1 is not None and prediction.match.score2 is not None:
                total_predictions += 1

                if points == 3:
                    exact_scores += 1
                elif points == 1:
                    bons_resultats += 1

            total_points += points

        classement.append({
            "visitor": visitor,
            "points": total_points,
            "exact_scores": exact_scores,
            "bons_resultats": bons_resultats,
            "total_predictions": total_predictions
        })

    classement = sorted(
        classement,
        key=lambda x: (
            x["points"],
            x["exact_scores"],
            x["bons_resultats"]
        ),
        reverse=True
    )

    return render_template(
        "groupe_classement.html",
        group=group,
        classement=classement,
        active_page="predictions"
    )

@app.route("/groupe/<code>/predictions", methods=["GET", "POST"])
@login_required
def private_group_predictions(code):

    if session.get("role") != "visitor":
        return redirect("/login")

    group = PrivateGroup.query.filter_by(code=code).first_or_404()

    visitor_id = session["visitor_id"]

    member = PrivateGroupMember.query.filter_by(
        group_id=group.id,
        visitor_id=visitor_id
    ).first()

    if member is None:
        member = PrivateGroupMember(
            group_id=group.id,
            visitor_id=visitor_id
        )

        db.session.add(member)
        db.session.commit()

    weeks = get_prediction_weeks()

    selected_week = request.args.get("week", "1")

    try:
        selected_week = int(selected_week)
    except ValueError:
        selected_week = 1

    current_week = None
    matchs = []

    if weeks:
        current_week = next(
            (week for week in weeks if week["number"] == selected_week),
            weeks[0]
        )

        matchs = Match.query.filter(
            Match.match_date >= current_week["start_str"],
            Match.match_date <= current_week["end_str"]
        ).order_by(
            Match.match_date,
            Match.match_time,
            Match.match_number
        ).all()

    today = date.today()

    week_is_open = False
    opening_date = None
    closing_date = None

    if current_week:
        opening_date = current_week["start"] - timedelta(days=3)
        closing_date = current_week["end"]

        week_is_open = opening_date <= today <= closing_date

    if request.method == "POST":

        if not week_is_open:
            return redirect(f"/groupe/{group.code}/predictions?week={selected_week}")

        for match in matchs:
            if not match_is_open(match):
                continue

            score1 = request.form.get(f"score1_{match.id}")
            score2 = request.form.get(f"score2_{match.id}")

            if score1 is None or score2 is None:
                continue

            if score1.strip() == "" or score2.strip() == "":
                continue

            prediction = Prediction.query.filter_by(
                visitor_id=visitor_id,
                match_id=match.id,
                prediction_type="private",
                private_group_id=group.id
            ).first()

            if prediction is None:
                prediction = Prediction(
                    visitor_id=visitor_id,
                    match_id=match.id,
                    prediction_type="private",
                    private_group_id=group.id
                )

                db.session.add(prediction)

            prediction.score1 = int(score1)
            prediction.score2 = int(score2)
            prediction.prediction_type = "private"
            prediction.private_group_id = group.id

        db.session.commit()

        return redirect(f"/groupe/{group.code}/classement")

    predictions_saved = Prediction.query.filter_by(
        visitor_id=visitor_id,
        prediction_type="private",
        private_group_id=group.id
    ).all()

    prediction_map = {
        prediction.match_id: prediction
        for prediction in predictions_saved
    }

    return render_template(
        "private_predictions.html",
        group=group,
        matchs=matchs,
        prediction_map=prediction_map,
        weeks=weeks,
        current_week=current_week,
        selected_week=selected_week,
        week_is_open=week_is_open,
        opening_date=opening_date,
        closing_date=closing_date,
        visitor_name=session.get("visitor_name"),
        active_page="predictions"
    )

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":
        email = request.form.get("email")

        visitor = Visitor.query.filter_by(email=email).first()

        if visitor:
            code = str(random.randint(100000, 999999))

            reset_code = PasswordResetCode(
                visitor_id=visitor.id,
                code=code,
                created_at=str(datetime.now())
            )

            db.session.add(reset_code)
            db.session.commit()

            session["reset_visitor_id"] = visitor.id

            email_sent = send_reset_email(visitor.email, code)

            if not email_sent:
                return render_template(
                    "forgot_password.html",
                    error="Impossible d'envoyer le code. Vérifie le mot de passe application Gmail."
                )

            return redirect("/verify-reset-code")

        return render_template(
            "forgot_password.html",
            error="Aucun compte trouvé avec cet email."
        )

    return render_template("forgot_password.html")


@app.route("/verify-reset-code", methods=["GET", "POST"])
def verify_reset_code():

    visitor_id = session.get("reset_visitor_id")

    if not visitor_id:
        return redirect("/forgot-password")

    if request.method == "POST":
        code = request.form.get("code")

        reset_code = PasswordResetCode.query.filter_by(
            visitor_id=visitor_id,
            code=code
        ).order_by(
            PasswordResetCode.id.desc()
        ).first()

        if reset_code:
            session["reset_code_valid"] = True
            return redirect("/reset-password")

        return render_template(
            "verify_reset_code.html",
            error="Code incorrect."
        )

    return render_template("verify_reset_code.html")


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    visitor_id = session.get("reset_visitor_id")
    code_valid = session.get("reset_code_valid")

    if not visitor_id or not code_valid:
        return redirect("/forgot-password")

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template(
                "reset_password.html",
                error="Les mots de passe ne correspondent pas."
            )

        visitor = Visitor.query.get(visitor_id)

        visitor.password = generate_password_hash(password)

        PasswordResetCode.query.filter_by(
            visitor_id=visitor_id
        ).delete()

        db.session.commit()

        session.pop("reset_visitor_id", None)
        session.pop("reset_code_valid", None)

        return redirect("/login")

    return render_template("reset_password.html")

@app.route("/dashboard")
@login_required
def dashboard():

    if session.get("role") != "visitor":
        return redirect("/")

    visitor_id = session["visitor_id"]

    predictions = Prediction.query.filter_by(
        visitor_id=visitor_id
    ).all()

    total_points = 0
    exact_scores = 0
    good_results = 0

    for prediction in predictions:

        points = prediction_points(prediction)

        total_points += points

        if points == 3:
            exact_scores += 1

        elif points == 1:
            good_results += 1

    all_visitors = Visitor.query.all()

    ranking = []

    for visitor in all_visitors:

        visitor_points = 0

        visitor_predictions = Prediction.query.filter_by(
            visitor_id=visitor.id,
            prediction_type="public"
        ).all()

        for prediction in visitor_predictions:
            visitor_points += prediction_points(prediction)

        ranking.append({
            "visitor_id": visitor.id,
            "points": visitor_points
        })

    ranking = sorted(
        ranking,
        key=lambda x: x["points"],
        reverse=True
    )

    position = 1

    for row in ranking:

        if row["visitor_id"] == visitor_id:
            break

        position += 1

    private_groups = PrivateGroupMember.query.filter_by(
        visitor_id=visitor_id
    ).count()

    receipts = PredictionReceipt.query.filter_by(
        visitor_id=visitor_id
    ).count()

    return render_template(
        "dashboard.html",
        total_points=total_points,
        exact_scores=exact_scores,
        good_results=good_results,
        position=position,
        private_groups=private_groups,
        receipts=receipts,
        active_page="dashboard"
    )


@app.route("/admin/live-video", methods=["GET", "POST"])
@admin_required
def admin_live_video():
    live_video = LiveVideo.query.first()

    if live_video is None:
        live_video = LiveVideo(title="", embed_url="", is_active=False)
        db.session.add(live_video)
        db.session.commit()

    if request.method == "POST":
        live_video.title = request.form["title"]
        live_video.embed_url = request.form["embed_url"]
        live_video.is_active = "is_active" in request.form

        db.session.commit()
        return redirect("/admin/live-video")

    return render_template(
        "admin_live_video.html",
        live_video=live_video,
        active_page="admin_live_video"
    )

@app.route("/classement-pronos")
@login_required
def classement_pronos():
    visitors = Visitor.query.all()

    classement = []

    for visitor in visitors:
        total_points = 0
        exact_scores = 0
        bons_resultats = 0
        total_predictions = 0

        for prediction in visitor.predictions:
            points = prediction_points(prediction)

            if prediction.match.score1 is not None and prediction.match.score2 is not None:
                total_predictions += 1

                if points == 3:
                    exact_scores += 1
                elif points == 1:
                    bons_resultats += 1

            total_points += points

        classement.append({
            "visitor": visitor,
            "points": total_points,
            "exact_scores": exact_scores,
            "bons_resultats": bons_resultats,
            "total_predictions": total_predictions
        })

    classement = sorted(
        classement,
        key=lambda x: (
            x["points"],
            x["exact_scores"],
            x["bons_resultats"]
        ),
        reverse=True
    )

    return render_template(
        "classement_pronos.html",
        classement=classement,
        active_page="classement_pronos"
    )

@app.route("/mes-tickets")
@login_required
def mes_tickets():
    if session.get("role") != "visitor":
        return redirect("/login")

    visitor_id = session.get("visitor_id")

    receipts = PredictionReceipt.query.filter_by(
        visitor_id=visitor_id
    ).order_by(
        PredictionReceipt.id.desc()
    ).all()

    return render_template(
        "mes_tickets.html",
        receipts=receipts,
        active_page="predictions"
    )

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route('/lang/<lang>')
def set_language(lang):

    session['lang'] = lang

    return redirect(request.referrer or url_for('home'))

@app.route("/sponsor")
def sponsor():
    return render_template("sponsor.html", active_page="sponsor")


def send_sponsor_email(subject, body, reply_to=None):
    sender_email = os.environ.get("MAIL_USERNAME", MAIL_USERNAME)
    sender_password = os.environ.get("MAIL_PASSWORD", MAIL_PASSWORD)
    mail_server = os.environ.get("MAIL_SERVER", MAIL_SERVER)
    mail_port = int(os.environ.get("MAIL_PORT", MAIL_PORT))

    if not sender_email or not sender_password:
        print("ERREUR EMAIL SPONSOR : MAIL_USERNAME ou MAIL_PASSWORD manquant.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = "custpriority@fozifoot.com"

    if reply_to:
        message["Reply-To"] = reply_to

    message.set_content(body)

    try:
        with smtplib.SMTP_SSL(mail_server, mail_port) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)
        return True
    except Exception as e:
        print("ERREUR EMAIL SPONSOR :", e)
        return False


@app.route("/sponsor-contact", methods=["POST"])
def sponsor_contact():
    company = request.form.get("company")
    contact_name = request.form.get("contact_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    country = request.form.get("country")
    website = request.form.get("website")
    partnership_type = request.form.get("partnership_type")
    budget = request.form.get("budget")
    message = request.form.get("message")

    subject = f"Nouvelle demande de sponsoring FoziFoot - {company}"

    body = f"""
Nouvelle demande de sponsoring FoziFoot

Entreprise : {company}
Contact : {contact_name}
Email : {email}
Téléphone : {phone}
Pays : {country}
Site Web : {website}

Type de partenariat :
{partnership_type}

Budget :
{budget}

Message :
{message}
"""

    email_sent = send_sponsor_email(subject, body, reply_to=email)

    if email_sent:
        return redirect("/sponsor?success=1")

    return redirect("/sponsor?error=1")

@app.route("/admin/tickets")
@admin_required
def admin_tickets():
    search = request.args.get("search", "").strip()

    query = db.session.query(PredictionReceipt, Visitor).join(
        Visitor,
        PredictionReceipt.visitor_id == Visitor.id
    )

    if search:
        query = query.filter(
            db.or_(
                Visitor.full_name.ilike(f"%{search}%"),
                Visitor.email.ilike(f"%{search}%"),
                PredictionReceipt.receipt_number.ilike(f"%{search}%")
            )
        )

    tickets = query.order_by(
        PredictionReceipt.id.desc()
    ).all()

    return render_template(
        "admin_tickets.html",
        tickets=tickets,
        search=search,
        active_page="admin_tickets"
    )

@app.route("/sitemap.xml")
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

<url>
<loc>https://fozifoot.com/</loc>
<priority>1.0</priority>
</url>

<url>
<loc>https://fozifoot.com/matches</loc>
<priority>0.9</priority>
</url>

<url>
<loc>https://fozifoot.com/groups</loc>
<priority>0.9</priority>
</url>

<url>
<loc>https://fozifoot.com/standings</loc>
<priority>0.9</priority>
</url>

<url>
<loc>https://fozifoot.com/statistiques</loc>
<priority>0.8</priority>
</url>

<url>
<loc>https://fozifoot.com/knockout</loc>
<priority>0.8</priority>
</url>

<url>
<loc>https://fozifoot.com/buteurs</loc>
<priority>0.8</priority>
</url>

<url>
<loc>https://fozifoot.com/passeurs</loc>
<priority>0.8</priority>
</url>

<url>
<loc>https://fozifoot.com/equipes</loc>
<priority>0.8</priority>
</url>

<url>
<loc>https://fozifoot.com/stadiums</loc>
<priority>0.8</priority>
</url>

<url>
<loc>https://fozifoot.com/login</loc>
<priority>0.6</priority>
</url>

<url>
<loc>https://fozifoot.com/register</loc>
<priority>0.6</priority>
</url>

<url>
<loc>https://fozifoot.com/sponsor</loc>
<priority>0.7</priority>
</url>

</urlset>
"""
    return Response(xml, mimetype="application/xml")


@app.route("/robots.txt")
def robots():

    robots_txt = """
User-agent: *
Allow: /

Sitemap: https://fozifoot.com/sitemap.xml
"""

    return Response(
        robots_txt,
        mimetype="text/plain"
    )


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

        admin_user = Admin.query.first()

        if admin_user is None:
            admin_user = Admin(
                username="admin",
                password=generate_password_hash("admin123")
            )

            db.session.add(admin_user)
            db.session.commit()

            print("Admin créé : admin / admin123")
        else:
            print("Admin existant :", admin_user.username)

    app.run(host="0.0.0.0", port=5000, debug=True)