# 📄 Documentation des routes - Message Service

## ✅ Routes implémentées

| Méthode | Route                                      | Description                             |
| ------- | ------------------------------------------ | --------------------------------------- |
| POST    | `/msg`                                     | Envoyer un message public ou privé      |
| GET     | `/msg?channel={name}`                      | Récupérer les messages d’un canal       |
| GET     | `/msg/private?from={pseudo1}&to={pseudo2}` | Messages privés entre deux utilisateurs |
| POST    | `/msg/reaction`                            | Ajouter une réaction emoji              |
| DELETE  | `/msg/reaction`                            | Supprimer une réaction                  |
| PUT     | `/msg/{id}`                                | Modifier un message (si auteur)         |
| DELETE  | `/msg/{id}`                                | Supprimer un message (si auteur)        |
| GET     | `/msg/thread/{id}`                         | Réponses à un message donné             |
| GET     | `/msg/pinned?channel={name}`               | Messages épinglés dans un canal         |
| GET     | `/msg/search?q={mot}`                      | Recherche plein texte dans les messages |

> ⚠️ Toutes les routes sont protégées : nécessitent un JWT dans `Authorization: Bearer <token>`

---

## ❌ Routes non implémentées (idées à venir ou supprimées)

| Méthode | Route             | Statut        | Commentaire                                             |
| ------- | ----------------- | ------------- | ------------------------------------------------------- |
| GET     | `/lastmsg/{id}`   | Non existante | Route mentionnée dans l'ancien doc mais absente du code |
| POST    | `/msg/pin/{id}`   | Non existante | Ajouter l'épinglage manuel de message                   |
| DELETE  | `/msg/pin/{id}`   | Non existante | Supprimer un épinglage                                  |
| PATCH   | `/msg/{id}/reply` | Non existante | Alternative pour répondre via une route dédiée          |

---

## 🔍 Détails techniques

* Toutes les routes REST utilisent le format JSON en entrée/sortie.
* Les identifiants (`{id}`) sont des entiers uniques pour les messages.
* Les réactions sont uniques par combinaison `(user_id, message_id, emoji)`.
* Le champ `reply_to` permet d'organiser des fils de discussion.
* La pagination partielle est disponible pour `/msg` via `offset` et `limit` (valeurs par défaut 0 et 50).
