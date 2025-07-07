# Projet-MicroService

Groupe 2 - message-service - gestion des messages publics, privés et réactions


Interaction a anticiper avec les autres groupes :

| Interaction             | Avec qui ?      | Ce qu'on dois faire                                     |
| ----------------------- | --------------- | ------------------------------------------------------- |
| Authentification        | user-service    | Lire le JWT, extraire le pseudo                         |
| Validation d’émetteur   | user-service    | Ne pas faire confiance à un champ `"from"` dans un POST |
| Droits d’écriture canal | channel-service | Vérifier l’existence du canal, et droits (si possible)  |
| Format des canaux       | channel-service | Connaitre le format des canaux pour valider les posts   |
| Proxy des requêtes      | gateway-service | Tu exposes `/msg`, etc. – eux relaient                  |
| Sécurité et cohérence   | tous            | Toujours vérifier l’utilisateur via le JWT              |
