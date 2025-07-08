# 📨 Message Service (Groupe 2)

**Membres** : Leduc Léo, Balmes Bastien, Pedrero Axel, Lours Simon *(absent)*, et **ChatGPT** *(support rédaction, correction, documentation – voir `group.md` pour plus de détails)*.

Ce micro-service gère les messages publics et privés, les réactions emoji, la modification et suppression de messages, les fils de discussion, les messages épinglés, ainsi que la recherche plein texte. Il fait partie de l'architecture distribuée IRC de CanaDuck.

---

## 🎯 Objectif du service

* Recevoir, stocker et afficher les messages :

  * publics dans un canal (`channel`)
  * privés entre deux utilisateurs (`recipient`)
* Gérer les réactions emoji (ajout / suppression)
* Permettre à un utilisateur d’éditer ou supprimer ses propres messages
* Fournir les fonctionnalités suivantes via des endpoints REST :

  * Liste des messages d’un canal → `GET /msg?channel=...`
  * Messages privés entre deux pseudos → `GET /msg/private?from=...&to=...`
  * Ajout / retrait de réactions → `POST` / `DELETE /msg/reaction`
  * Fil de discussion → `GET /msg/thread/<id>`
  * Messages épinglés → `GET /msg/pinned?channel=...`
  * Recherche plein texte → `GET /msg/search?q=...`

---

## 🔐 Authentification (JWT)

Toutes les routes nécessitent un **JWT valide** généré par le `user-service`.

* Le token est lu dans le header :

  ```http
  Authorization: Bearer <token>
  ```
* Le décorateur `@require_jwt` injecte automatiquement les infos utilisateur (`user_id`, `username`) dans `request.user`.

---

## 🧱 Structure du projet

```text
.
├── Dockerfile              ← Image Docker du service
├── docker-compose.yml      ← Stack avec MySQL
├── entrypoint.sh           ← Attend le démarrage de MySQL
├── .env                    ← Configuration (clé secrète, URL BDD)
├── Pipfile / Pipfile.lock  ← Gestion des dépendances (pipenv)
├── requirements.txt        ← Généré depuis pipenv
├── test_basic.py           ← Test unitaire minimal
└── app/
    ├── __init__.py         ← Initialisation Flask, DB, routes
    ├── main.py             ← Point d’entrée (lance le serveur Flask)
    ├── config.py           ← Configuration Flask (clé, DB)
    ├── auth.py             ← Vérification JWT
    └── models.py / routes.py ← Modèles SQLAlchemy, routes REST
```

---

## ⚙️ Installation et Lancement

### ▶️ En local (via Pipenv)

```bash
git clone <votre-repo>
cd message-service
pipenv install
pipenv run python -m app.main
```

Variables dans `.env` :

```env
SECRET_KEY=informations-sur-les-utilisateurs
DB_URL=sqlite:///instance/messages.db
```

### 🐳 Avec Docker

```bash
docker-compose up --build
```

Le service écoute sur `http://localhost:5002`.

---

## 🔗 Dépendances inter-services

| Service         | Groupe | Usage principal                    |
| --------------- | ------ | ---------------------------------- |
| user-service    | 1      | Authentification via JWT           |
| channel-service | 3      | (Optionnel) Vérification de canal  |
| gateway-service | 4      | Reverse proxy de toutes les routes |

---

## 📚 Routes REST disponibles

| Méthode | Route                          | Description                             |
| ------- | ------------------------------ | --------------------------------------- |
| POST    | `/msg`                         | Envoyer un message                      |
| GET     | `/msg?channel=...`             | Liste des messages d’un canal           |
| GET     | `/msg/private?from=...&to=...` | Messages privés entre deux pseudos      |
| POST    | `/msg/reaction`                | Ajouter une réaction emoji              |
| DELETE  | `/msg/reaction`                | Supprimer une réaction emoji            |
| PUT     | `/msg/<id>`                    | Modifier un message (si auteur)         |
| DELETE  | `/msg/<id>`                    | Supprimer un message (si auteur)        |
| GET     | `/msg/thread/<id>`             | Réponses à un message                   |
| GET     | `/msg/pinned?channel=...`      | Messages épinglés d’un canal            |
| GET     | `/msg/search?q=...`            | Recherche plein texte dans les messages |

---

## 📊 Exemples d’appels `curl`

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

**Recherche plein texte :**

```bash
curl http://localhost:5002/msg/search?q=erreur \
 -H "Authorization: Bearer <token>"
```

---

## ✅ Tests

```bash
pipenv run python test_basic.py
```

Un test basique vérifie que `/msg` sans JWT retourne bien un `401 Unauthorized`.
