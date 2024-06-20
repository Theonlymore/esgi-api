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
        
        equipe_locale_id = new_match_data.get('equipe_locale_id')
        equipe_visiteur_id = new_match_data.get('equipe_visiteur_id')
        
        # Vérifier si les équipes spécifiées existent
        equipe_locale = Equipe.query.get(equipe_locale_id)
        equipe_visiteur = Equipe.query.get(equipe_visiteur_id)
        
        if not equipe_locale:
            return jsonify({'error': f"L'équipe avec l'id {equipe_locale_id} n'existe pas."}), 400
        
        if not equipe_visiteur:
            return jsonify({'error': f"L'équipe avec l'id {equipe_visiteur_id} n'existe pas."}), 400
        
        new_match = Match(date=date_obj,
                            equipe_locale_id=new_match_data['equipe_locale_id'],
                            equipe_visiteur_id=new_match_data['equipe_visiteur_id'],
                            score_locale=new_match_data.get('score_locale'),
                            score_visiteur=new_match_data.get('score_visiteur'))

        try:
            db.session.add(new_match)
            db.session.commit()
            return jsonify({'message': 'Match ajouté avec succès'}), 201

        except Exception as e:
            db.session.rollback()  # Annuler les changements en cas d'erreur
            return jsonify({'error': str(e)}), 500

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


@app.route('/api/equipes', methods=['POST'])
def add_equipe():
    nom = request.json.get('nom')
    # Assurez-vous que le nom de l'équipe est fourni
    if not nom:
        return jsonify({'error': 'Le nom de l\'équipe est requis'}), 400
    
    nouvelle_equipe = Equipe(nom=nom)

    try:
        db.session.add(nouvelle_equipe)
        db.session.commit()
        return jsonify({'message': 'Équipe ajoutée avec succès'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/equipes/<int:equipe_id>', methods=['GET', 'DELETE'])
def manage_equipe(equipe_id):
    equipe = Equipe.query.get_or_404(equipe_id)

    if request.method == 'GET':
        return jsonify(equipe.serialize())
    
    elif request.method == 'DELETE':
        db.session.delete(equipe)
        db.session.commit()
        return jsonify({'message': 'Equipe supprimé avec succès'})
        
@app.route('/api/equipes/<int:equipe_id>', methods=['PUT'])
def update_equipe(equipe_id):
    equipe = Equipe.query.get_or_404(equipe_id)
    data = request.json
    
    # Mettre à jour les champs de l'équipe si les données sont fournies
    if 'nom' in data:
        equipe.nom = data['nom']

    try:
        db.session.commit()
        return jsonify({'message': 'Équipe mise à jour avec succès'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500






# Autres routes pour la gestion des joueurs, coachs, équipes, etc. à implémenter


if __name__ == '__main__':
    # Assurez-vous d'importer ici les modèles après avoir configuré app
    from models import *
    # Créez la base de données avec toutes les tables définies dans models.py
    db.create_all()
    print("db created")


if __name__ == '__main__':
    app.run(debug=True)
