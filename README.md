# NLP Pizza&Challenge Multi Cloud API Servives
Docker service that includes the following NLP Cloud services:
- [Google Cloud Language](https://cloud.google.com/natural-language/)
- [Rosette Text Analytics](https://www.rosette.com/)
- [Azure Text Analytics](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/?v=18.05)
- [Interpretext API](https://beeva-labs.github.io/interpretext-api/)
- [Twitter Service]()

## 0. Index
1. [Usage](#1-usage)
2. [Deploy](#2-deploy)

## 1. Usage
All services and providers are describe on `http://<ip or localhost>/` with `GET` http call:
```json
  {
    "Rosette Text Analytics": "/rosette",
    "Google Cloud Natural Language": "/google",
    "Azure Text Analytics": "/azure",
    "Interpretext API": "/interpretext",
    "Twitter threads extraction": "/twitter"
  }
```

All services are listed on `http://<ip or localhost>/<service>/` with `GET` http call:
```sh
  {
    "language detection": "/interpretext/language",
    "tokens extraction": "/interpretext/tokenize",
    "part of speech analysis": "/interpretext/part-of-speech",
    "summary extraction": "/interpretext/summary"
  }
```

## 2. Deploy

### Install Interpretext API
```sh
  git clone https://github.com/beeva-labs/interpretext-api.git
  cd interpretext-api
  docker build -t interpretext .
```

### Install Service
```sh
  git clone https://github.com/beeva-labs/NLP_PizzaChallenge.git
  cd NLP_PizzaChallenge
  docker build -t nlpmultiservice .
```

### Run Service
Create `docker-compose.yml` with this content:
```yaml
  version: "3"

  services:
    interpretext:
      image: interpretext
      restart: always
    nlpmultiapi:
      image: nlpmultiapi
      ports:
      - "80:80"
      links:
      - interpretext:interpretext
      restart: always
```

Run services:
```sh
  docker-compose up
```
