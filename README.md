# Message-Service (Groupe 2)

## Installation et Lancement

### 1. En local
```bash
pipenv --python 3.10.12
pipenv install
pipenv lock --requirements > requirements.txt
cp .env.sample .env
pipenv run python -m app.main
```

### 2. Docker
```bash
docker-compose up --build
```

## Routes
- POST   /msg
- GET    /msg
- POST   /msg/reaction
- DELETE /msg/reaction
- PUT    /msg/:id
- DELETE /msg/:id
- GET    /msg/thread/:id
- GET    /msg/pinned?channel=
- GET    /msg/private?from=&to=
- GET    /msg/search?q=
