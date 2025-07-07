# Message Service (Groupe 2)

Membres : 
Leduc Léo - Balmes Bastien - Lours Simon - Pedrero Axel

Ce micro-service fait partie de l’architecture IRC distribuée de CanaDuck. Il gère
les messages publics et privés, les réactions, la modification, la suppression,
les fils de discussion, les épinglés et la recherche.

---

## 🎯 Objectif du service

* Recevoir et stocker les messages (canaux publics et messages privés).
* Gérer les réactions emoji sur chaque message.
* Permettre l’édition et la suppression des messages (seulement par l’auteur).
* Offrir des endpoints pour récupérer :

  * Tous les messages d’un canal (`GET /msg?channel=...`).
  * Les messages privés entre deux utilisateurs (`GET /msg/private?from=...&to=...`).
  * Les réactions (`POST`/`DELETE /msg/reaction`).
  * Les fils de discussion (`GET /msg/thread/<id>`).
  * Les messages épinglés (`GET /msg/pinned?channel=...`).
  * La recherche plein texte (`GET /msg/search?q=...`).

---

## 🔗 Dépendances inter-groupes

| Service cible       | Groupe | Rôle                      | Interaction technique                         |
| ------------------- | ------ | ------------------------- | --------------------------------------------- |
| **user-service**    | 1      | Authentification & JWT    | Décorateur `@require_jwt` ; extraire `pseudo` |
| **channel-service** | 3      | Gestion des canaux & ACLs | (Optionnel) Vérifier existence et droits      |
| **gateway-service** | 4      | Proxy public / agrégateur | Toutes les requêtes `/msg*` passent par lui   |

* **user-service** :

  * Envoie un JWT signé contenant `{ pseudo, roles, exp }`.
  * Notre décorateur lit le header `Authorization: Bearer <token>` et injecte
    `request.user['pseudo']` pour authentifier les actions.

* **channel-service** :

  * (Optionnel) Appel interne pour vérifier qu’un canal existe et que l’utilisateur
    a le droit d’y écrire. Pour commencer, on utilise un mock en mémoire.

* **gateway-service** :

  * Point d’entrée unique. Il route `/msg`, `/msg/private`, `/msg/reaction`,
    etc. vers ce service sur le port interne `5002`.

---

## 🏗️ Architecture du projet

```text
message-service/
├── app.py          # Entrée Flask avec toutes les routes
├── config.py       # (Optionnel) Configuration et variables d’environnement
├── utils.py        # (Optionnel) Fonctions utilitaires et validateurs
├── models.py       # (Optionnel) Modèles SQLAlchemy si on passe à MySQL
├── requirements.txt# flask, pyjwt, etc.
├── Dockerfile      # Conteneurisation
└── README.md       # Documentation du service (ce fichier)
```

* **app.py** :

  * Initialise l’app Flask.
  * Définit le décorateur `require_jwt` pour sécuriser les routes d’écriture.
  * Implémente les endpoints :

    * `POST /msg`, `GET /msg`, `POST`/`DELETE /msg/reaction`,
    * `PUT`/`DELETE /msg/<id>`, `GET /msg/thread/<id>`,
    * `GET /msg/pinned`, `GET /msg/private`, `GET /msg/search`.
  * Stocke temporairement les messages dans une liste Python `MESSAGES`.

* **requirements.txt** :

  ```text
  flask
  pyjwt
  ```

* **Dockerfile** :

  ```dockerfile
  FROM python:3.9-slim
  WORKDIR /app
  COPY requirements.txt ./
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . ./
  EXPOSE 5002
  CMD ["python", "app.py"]
  ```

---

## 🚀 Installation et lancement

1. **En local** (sans Docker) :

   ```bash
   git clone <url-de-votre-dépôt>
   cd message-service
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   export SECRET_KEY="ce-projet-est-horrible"
   python app.py
   ```

   Le service écoute sur `http://localhost:5002`.

2. **Avec Docker** :

   ```bash
   docker build -t message-service .
   docker run -d -p 5002:5002 \
     -e SECRET_KEY="ce-projet-est-horrible" \
     --name msgsvc message-service
   ```

---

## 📋 Exemples d’appels

1. **Envoi de message** :

   ```bash
   curl -X POST http://localhost:5002/msg \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{ "channel": "tech", "text": "Salut tout le monde" }'
   ```

2. **Récupérer les messages d’un canal** :

   ```bash
   curl http://localhost:5002/msg?channel=tech
   ```

3. **Ajouter une réaction** :

   ```bash
   curl -X POST http://localhost:5002/msg/reaction \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{ "message_id": "<id>", "emoji": "😀" }'
   ```

4. **Modifier un message** :

   ```bash
   curl -X PUT http://localhost:5002/msg/<id> \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{ "text": "Nouveau texte" }'
   ```

5. **Recherche plein texte** :

   ```bash
   curl http://localhost:5002/msg/search?q=erreur
   ```
