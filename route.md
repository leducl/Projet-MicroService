## Route 

| Méthode | Route                        | Description                             |
| ------- | ---------------------------- | --------------------------------------- |
| POST    | `/msg`                       | Envoyer un message public               |
| GET     | `/msg?channel={name}`        | Récupérer les messages d’un canal       |
| POST    | `/msg/reaction`              | Ajouter une réaction (emoji)            |
| DELETE  | `/msg/reaction`              | Retirer une réaction                    |
| PUT     | `/msg/{id}`                  | Modifier un message (auteur seul)       |
| DELETE  | `/msg/{id}`                  | Supprimer un message (auteur seul)      |
| GET     | `/msg/thread/{id}`           | Récupérer les réponses à un message     |
| GET     | `/msg/pinned?channel={}`     | Messages épinglés dans un canal         |
| GET     | `/msg/private?from={}&to={}` | Messages privés entre deux utilisateurs |
| GET     | `/msg/search?q={}`           | Recherche plein texte                   |
