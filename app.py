from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)
# Modèles importés depuis models.py
from models import Match, Joueur, Coach, Equipe, Statistique

# Routes pour la gestion des matches
@app.route('/api/matches', methods=['GET', 'POST'])
def manage_matches():
    if request.method == 'GET':
        matches = Match.query.all()
        return jsonify([match.serialize() for match in matches])

    elif request.method == 'POST':
        new_match_data = request.json
        
        try:
            date_obj = datetime.strptime(new_match_data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Format de date invalide. Utilisez le format YYYY-MM-DD'}), 400
        
        new_match = Match(date=date_obj,
                          equipe_locale=new_match_data['equipe_locale'],
                          equipe_visiteur=new_match_data['equipe_visiteur'],
                          score_locale=new_match_data.get('score_locale'),
                          score_visiteur=new_match_data.get('score_visiteur'))
        db.session.add(new_match)
        db.session.commit()
        return jsonify({'message': 'Match ajouté avec succès'}), 201

@app.route('/api/matches/<int:match_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_match(match_id):
    match = Match.query.get_or_404(match_id)

    if request.method == 'GET':
        return jsonify(match.serialize())

    elif request.method == 'PUT':
        data = request.json
        match.date = data['date']
        match.equipe_locale = data['equipe_locale']
        match.equipe_visiteur = data['equipe_visiteur']
        match.score_locale = data.get('score_locale')
        match.score_visiteur = data.get('score_visiteur')
        db.session.commit()
        return jsonify({'message': 'Match mis à jour avec succès'})

    elif request.method == 'DELETE':
        db.session.delete(match)
        db.session.commit()
        return jsonify({'message': 'Match supprimé avec succès'})

# Autres routes pour la gestion des joueurs, coachs, équipes, etc. à implémenter


if __name__ == '__main__':
    # Assurez-vous d'importer ici les modèles après avoir configuré app
    from models import *
    # Créez la base de données avec toutes les tables définies dans models.py
    db.create_all()
    print("db created")


if __name__ == '__main__':
    app.run(debug=True)
