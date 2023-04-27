# SoftDesk

## Installation

```shell
git clone git@github.com:Dastfox/P10_python_SoftDesk.git
```

## Usage

```shell
venv -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Endpoints

| Description                                                                                 | Méthode | Endpoint                                   |
| ------------------------------------------------------------------------------------------- | ------- | ------------------------------------------ |
| Inscription de l'utilisateur                                                                | POST    | `/signup/`                                 |
| Connexion de l'utilisateur                                                                  | POST    | `/login/`                                  |
| Récupérer la liste de tous les projets (projects) rattachés à l'utilisateur (user) connecté | GET     | `/projects/`                               |
| Créer un projet                                                                             | POST    | `/projects/`                               |
| Récupérer les détails d'un projet (project) via son id                                      | GET     | `/projects/{id}/`                          |
| Mettre à jour un projet                                                                     | PUT     | `/projects/{id}/`                          |
| Supprimer un projet et ses problèmes                                                        | DELETE  | `/projects/{id}/`                          |
| Ajouter un utilisateur (collaborateur) à un projet                                          | POST    | `/projects/{id}/users/`                    |
| Récupérer la liste de tous les utilisateurs (users) attachés à un projet (project)          | GET     | `/projects/{id}/users/`                    |
| Supprimer un utilisateur d'un projet                                                        | DELETE  | `/projects/{id}/users/{id}`                |
| Récupérer la liste des problèmes (issues) liés à un projet (project)                        | GET     | `/projects/{id}/issues/`                   |
| Créer un problème dans un projet                                                            | POST    | `/projects/{id}/issues/`                   |
| Mettre à jour un problème dans un projet                                                    | PUT     | `/projects/{id}/issues/{id}`               |
| Supprimer un problème d'un projet                                                           | DELETE  | `/projects/{id}/issues/{id}`               |
| Créer des commentaires sur un problème                                                      | POST    | `/projects/{id}/issues/{id}/comments/`     |
| Récupérer la liste de tous les commentaires liés à un problème (issue)                      | GET     | `/projects/{id}/issues/{id}/comments/`     |
| Modifier un commentaire                                                                     | PUT     | `/projects/{id}/issues/{id}/comments/{id}` |
| Supprimer un commentaire                                                                    | DELETE  | `/projects/{id}/issues/{id}/comments/{id}` |
| Récupérer un commentaire (comment) via son id                                               | GET     | `/projects/{id}/issues/{id}/comments/{id}` |
