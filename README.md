# 📨 Message Service (Groupe 2)

**Membres** : LEDUC Léo, BALMES Bastien, PEDRERO Axel, LOURS Simon (ABSENT), ChatGPT (voir `group.md` pour plus de détails)

Ce micro-service gère :

* Les messages publics (canaux) et privés (entre deux utilisateurs)
* Les réactions emoji (ajout / suppression)
* La modification et la suppression de messages par leur auteur
* Les fils de discussion (réponses)
* Les messages épinglés
* La recherche plein-texte

Il s’intègre à l’architecture IRC de CanaDuck et s’appuie sur un JWT fourni par le **user-service**.

---

## 🎯 Objectif du service

1. Recevoir, stocker et retourner des messages via une API REST JSON
2. Contrôler les accès via JWT
3. Offrir une API simple pour :

   * Envoyer un message (public ou privé)
   * Lister / filtrer / paginer les messages
   * Réagir à un message
   * Éditer / supprimer un message
   * Gérer les threads, les messages épinglés et la recherche

---

## 🧱 Structure du projet

```
.
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── .env
├── requirements.txt
├── test.sh
├── instance/
│   └── messages.db
└── app/
    ├── __init__.py
    ├── config.py
    ├── auth.py
    ├── main.py
    ├── models.py
    └── routes.py
```

* **Dockerfile** : construction de l’image Docker
* **docker-compose.yml** : stack Docker (BDD MySQL)
* **entrypoint.sh** : script d’attente du service de BDD et lancement des migrations
* **.env** : variables d’environnement (SECRET\_KEY, DB\_URL)
* **requirements.txt** : dépendances Python
* **test.sh** : script d’intégration (bash + curl)
* **instance/messages.db** : base MySQL (volume local)
* **app/** : code de l’application Flask

  * `__init__.py` : création de l’app, configuration SQLAlchemy, migrations
  * `config.py` : classe de configuration (SECRET\_KEY, DB\_URL…)
  * `auth.py` : décorateur `@require_jwt` (vérification et décodage JWT)
  * `main.py` : point d’entrée (`python -m app.main`)
  * `models.py` : définition des modèles SQLAlchemy (Message, Reaction…)
  * `routes.py` : endpoints REST (`/msg`, `/msg/search`, etc.)

---

## ⚙️ Installation & Lancement

### 1. En local (pip)

```bash
git clone <votre-repo>
cd message-service
pip install -r requirements.txt
python -m app.main
```

L’application écoute sur : `http://localhost:5002`

### 2. En local (Docker)

```bash
docker-compose up --build
```

* Le conteneur MySQL est initialisé via `entrypoint.sh`.
* L’app se lance automatiquement sur le port 5002.

---

## 🔐 Authentification JWT

Toutes les routes exigent un **JWT** valide :

```
Authorization: Bearer <token>
```

Le décorateur `@require_jwt` injecte `request.user` (user\_id, username).

---

## 📚 Routes REST

| Méthode | Route                    | Description                                  |
| ------- | ------------------------ | -------------------------------------------- |
| POST    | `/msg`                   | Envoyer un message (public ou privé)         |
| GET     | `/msg`                   | Lister messages (`?channel=&offset=&limit=`) |
| GET     | `/msg/private?from=&to=` | Messages privés entre deux utilisateurs      |
| POST    | `/msg/reaction`          | Ajouter une réaction emoji                   |
| DELETE  | `/msg/reaction`          | Supprimer une réaction                       |
| PUT     | `/msg/{id}`              | Modifier son message                         |
| DELETE  | `/msg/{id}`              | Supprimer son message                        |
| GET     | `/msg/thread/{id}`       | Récupérer les réponses à un message          |
| GET     | `/msg/pinned?channel=`   | Récupérer les messages épinglés              |
| GET     | `/msg/search?q=`         | Recherche plein-texte                        |

> ⚠️ Routes protégées : `401 Unauthorized` si JWT absent ou invalide.

---

## 📊 Exemples `curl`

**Envoyer un message :**

```bash
curl -X POST http://localhost:5002/msg \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "channel": "dev", "text": "Hello world!" }'
```

**Ajouter une réaction :**

```bash
curl -X POST http://localhost:5002/msg/reaction \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "message_id": 1, "emoji": "🔥" }'
```

**Modifier un message :**

```bash
curl -X PUT http://localhost:5002/msg/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "text": "Message modifié" }'
```

**Rechercher un mot-clé :**

```bash
curl http://localhost:5002/msg/search?q=erreur \
  -H "Authorization: Bearer <token>"
```

---

## ✅ Tests d’intégration

Un script `test.sh` couvre les scénarios basiques et d’erreur.
Après avoir démarré le service :

```bash
bash test.sh
```

---

## 🔗 Dépendances inter-services

| Service         | Groupe | Usage principal                      |
| --------------- | ------ | ------------------------------------ |
| user-service    | 1      | Authentification JWT                 |
| channel-service | 3      | Validation de l’existence des canaux |
| gateway-service | 4      | Point d’entrée / reverse-proxy       |

---

> **Migrations (MySQL)**
> Avec Flask-Migrate :
>
> ```bash
> flask db init       # une seule fois
> flask db migrate -m "Initial"
> flask db upgrade
> ```
>
> Les migrations sont aussi lancées automatiquement par `entrypoint.sh`.
