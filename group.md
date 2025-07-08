# 📅 group.md - Message Service (Groupe 2)

## Membres

**Membres :** LEDUC Léo, BALMES Bastien, PEDRERO Axel, LOURS Simon

| Nom     | Rôle                             |
| ------- | -------------------------------- |
| LEO     | Documentation / Rédacteur de log |
| Bastien | Développeur principal            |
| Axel    | Tests unitaires / soutien dev    |
| Simon   | Absent les deux jours            |

---

## ✏️ LOG DE L'ÉQUIPE

### 🌟 Lundi (13h30 - 17h00)

| Heure | Événement                                                              |
| ----- | ---------------------------------------------------------------------- |
| 13h30 | Ouverture du dépôt Git et initialisation du projet                     |
| 13h35 | Mise en place de la structure de dossiers (app/, routes.py, etc.)      |
| 13h50 | Ajout du `Dockerfile` et `docker-compose.yml`                          |
| 14h05 | Configuration de `Pipfile` et `requirements.txt` avec pipenv           |
| 14h30 | Début de l’implémentation du modèle SQLAlchemy `Message` et `Reaction` |
| 15h00 | Création du décorateur `@require_jwt` dans `auth.py`                   |
| 15h15 | Premiers endpoints Flask : `POST /msg` et `GET /msg?channel=...`       |
| 15h45 | Configuration base SQLite pour démarrer plus vite                      |
| 16h15 | Ajout des routes de réactions : `POST` / `DELETE /msg/reaction`        |
| 16h45 | Tests CURL sur les routes principales                                  |
| 17h00 | Fin de journée                                                         |

---

### 🌟 Mardi (8h30 - 12h05)

| Heure | Événement                                                          |
| ----- | ------------------------------------------------------------------ |
| 08h30 | Reprise du projet, lecture des logs de la veille                   |
| 08h40 | Ajout du endpoint `PUT /msg/<id>` (modification de message)        |
| 09h00 | Ajout de `DELETE /msg/<id>`                                        |
| 09h20 | Implémentation du endpoint `/msg/thread/<id>`                      |
| 09h45 | Ajout de `GET /msg/pinned?channel=...`                             |
| 10h15 | Implémentation de la recherche plein texte `GET /msg/search?q=...` |
| 10h40 | Tests unitaires simples avec `unittest` dans `test_basic.py`       |
| 11h00 | Finalisation de la sécurisation JWT sur toutes les routes          |
| 11h20 | Relecture et correction des routes à la volée                      |
| 11h40 | Rédaction du README.md et du fichier `routes.md`                   |
| 12h00 | Finalisation et nettoyage du dépôt Git, vérification Docker        |
| 12h05 | Fin de session - projet livré                                      |
