Ce repository contient le Back
end de l'application web de la
 plateforme de veille Juridique
 (EasyLaw), développée par
 l'équipe ITouch  en Flask  python
 dans le cadre du projet de
 spécialité (2CS-SIL) à l'ESI.
 Ce repository contient
 principalement la logique
 d’authentification , users
 management,subscriptions and
 payment,create and get plans,
 seperate access for each
 search....

## Getting Started

### Pull and run docker image

1.  First authenticate with your github credentials (if you haven't already)

```bash
docker login ghcr.io -u <username>
```

Replace < username > with your GitHub username and enter your personal access token (PAT) that has the read:packages scope.

2.  Pull the image

```bash
docker pull ghcr.io/salahdevp/itouch-easylaw-backend:latest
```

3. Run the container

```bash
docker run -e ELASTIC_PASSWORD=<elastic password> -p 5000:5000 ghcr.io/salahdevp/itouch-easylaw-backend:latest
```

Replace < elastic password > with your elastic search password.
