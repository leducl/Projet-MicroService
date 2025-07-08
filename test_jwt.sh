#!/usr/bin/env bash
# tests/test_endpoints.sh
# Script d'intégration utilisant curl pour tester les endpoints du message-service
# Prérequis : le service doit être accessible sur l'adresse interne Docker (172.18.0.3:5002)

# Jeton JWT pré-généré
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNzUxOTcyNDIzfQ.j6LFbmKB0Y1n6mmZ0mzgtfWY65Cn9KZ2zSsqf2FtqAk"

# Fonction utilitaire pour afficher titre de test
title() {
  echo -e "\n=== $1 ==="
}

# Base URL utilisée
BASE_URL="http://172.18.0.3:5002"

# Success scenarios
# 1. GET /msg (sans JWT)
title "1. GET /msg sans JWT"
curl -i "$BASE_URL/msg"

# 2. GET /msg (avec JWT)
title "2. GET /msg avec JWT"
curl -i -H "Authorization: Bearer $TOKEN" "$BASE_URL/msg"

# 3. POST /msg : création de message
title "3. POST /msg : création de message"
curl -i -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from curl","channel":"test"}' \
  "$BASE_URL/msg"

# 4. GET /msg?channel=test
title "4. GET /msg?channel=test"
curl -i -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/msg?channel=test"

# 5. POST /msg/reaction : ajout réaction
title "5. POST /msg/reaction : ajout réaction"
curl -i -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message_id":1,"emoji":"👍"}' \
  "$BASE_URL/msg/reaction"

# 6. DELETE /msg/reaction : suppression réaction
title "6. DELETE /msg/reaction : suppression réaction"
curl -i -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message_id":1,"emoji":"👍"}' \
  "$BASE_URL/msg/reaction"

# 7. PUT /msg/1 : modification message
title "7. PUT /msg/1 : modification message"
curl -i -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Updated via curl"}' \
  "$BASE_URL/msg/1"

# 8. DELETE /msg/1 : suppression message
title "8. DELETE /msg/1 : suppression message"
curl -i -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/msg/1"

# 9. GET /msg/thread/1 : fil de discussion
title "9. GET /msg/thread/1 : fil de discussion"
curl -i -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/msg/thread/1"

# 10. GET /msg/pinned?channel=test : épinglés
title "10. GET /msg/pinned?channel=test : épinglés"
curl -i -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/msg/pinned?channel=test"

# 11. GET /msg/private?from=testuser&to=testuser : privés
title "11. GET /msg/private?from=testuser&to=testuser : privés"
curl -i -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/msg/private?from=testuser&to=testuser"

# 12. GET /msg/search?q=Hello : recherche full-text
title "12. GET /msg/search?q=Hello : recherche full-text"
curl -i -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/msg/search?q=Hello"

# Error scenarios (KO)
# 13. GET /msg with invalid JWT
title "13. GET /msg avec JWT invalide"
curl -i -H "Authorization: Bearer INVALID_TOKEN" "$BASE_URL/msg"

# 14. POST /msg without text field
title "14. POST /msg sans 'text' (400)"
curl -i -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"test"}' \
  "$BASE_URL/msg"

# 15. POST /msg/reaction missing fields
title "15. POST /msg/reaction sans champs (400)"
curl -i -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "$BASE_URL/msg/reaction"

# 16. PUT /msg/9999 non-existent (404)
title "16. PUT /msg/9999 inexistant (404)"
curl -i -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Does not matter"}' \
  "$BASE_URL/msg/9999"

