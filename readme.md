# Projet ESGI - API
## Description
Ce projet vise à déployer une API REST avec Flask sur le serveur rocheralexandre.com à chaque commit sur la branche main. L'API permet de gérer des équipes et des matchs entre ces équipes.

## Fonctionnalités de l'API
Ajouter une équipe
URL: POST http://rocheralexandre.com:4321/api/equipes

## Requête:

```json
{
    "id": X,
    "nom": X
}
```

## Obtenir une équipe
URL: GET http://rocheralexandre.com:4321/api/equipes/(id)

## Ajouter un match
Remarque: Un match ne peut pas être ajouté si les équipes n'existent pas.

URL: POST http://rocheralexandre.com:4321/api/matchs

Requête:

```json
{
    "date": "2024-06-25",
    "equipe_locale_id": "1",
    "equipe_visiteur_id": "3",
    "score_locale": 3,
    "score_visiteur": 1
}
```
## Obtenir un match

URL: GET http://rocheralexandre.com:4321/api/matchs/(id)
