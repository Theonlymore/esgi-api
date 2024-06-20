from app import db

# Modèles de données avec SQLAlchemy
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    equipe_locale = db.Column(db.String(100), nullable=False)
    equipe_visiteur = db.Column(db.String(100), nullable=False)
    score_locale = db.Column(db.Integer)
    score_visiteur = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'equipe_locale': self.equipe_locale,
            'equipe_visiteur': self.equipe_visiteur,
            'score_locale': self.score_locale,
            'score_visiteur': self.score_visiteur
        }

class Joueur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    equipe = db.Column(db.String(100), nullable=False)

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    equipe_geree = db.Column(db.String(100), nullable=False)

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(100), nullable=False)

class Statistique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    joueur_id = db.Column(db.Integer, db.ForeignKey('joueur.id'), nullable=False)
    buts_marques = db.Column(db.Integer, default=0)
    passes_decisives = db.Column(db.Integer, default=0)
    cartons_jaunes = db.Column(db.Integer, default=0)
    cartons_rouges = db.Column(db.Integer, default=0)

    match = db.relationship('Match', backref=db.backref('statistiques', cascade='all, delete-orphan'))
    joueur = db.relationship('Joueur', backref=db.backref('statistiques', cascade='all, delete-orphan'))
