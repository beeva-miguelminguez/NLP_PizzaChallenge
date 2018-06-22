# NLP Pizza&Challenge Multi Cloud API Servives
Docker service that includes the following NLP Cloud services:
- [Google Cloud Natural Language](https://cloud.google.com/natural-language/)
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

### 1.1 Twitter
We have the following endpoints available: 
- `/twitter/tweets`: Retrives te latest user tweets, limited to 300 items. Making a `POST` request with `username` field via `multipart/form-data`.
- `/twitter/hashtag`: Retrives te latest tweets about hashtag provided, limited to 300 items. Making a `POST` request with `hashtag` field via `multipart/form-data`.
- `/twitter/threads`: Retrives te latest user threads. Making a `POST` request with `username` field via `multipart/form-data`.

### 1.2 Rosette Text Analytics (Only English)
All request must be via `POST` method, and text must be into `content` field via `multipart/form-data`. We have the following endpoints available:
- `/rosette/tokenize`: Retrives content provided splitted into single tokens.
- `/rosette/part-of-speech`: Tags whole words with its morphologic category.
- `/rosette/language`: Detects content language.
- `/rosette/entities`: Extract entities from the content and retrives contextual information if exists.
- `/rosette/topics`: Returns content topics.
- `/rosette/sentiment`: Analyses text sentiment.
- `/rosette/categories`: Categorizes the text into a common category.

### 1.3 Google Cloud Natural Language
All request must be via `POST` method, and text must be into `content` field via `multipart/form-data`. We have the following endpoints available:
- `/google/sentiment`: Analyses text sentiment.
- `/google/entities`: Extract entities from the content and retrives contextual information if exists.
- `/google/part-of-speech`: Tags whole words with its morphologic category.
- `/google/categories`: Categorizes the text into a common category.

### 1.4 Azure Text Analytics
All request must be via `POST` method, and text must be into `content` field via `multipart/form-data`. We have the following endpoints available:
- `/azure/language`: Detects content language.
- `/azure/entities`: Extract entities from the content and retrives contextual information if exists.
- `/azure/sentiment`: Analyses text sentiment.
- `/azure/topics`: Returns content topics.

### 1.5 Interpretext API (Only Spanish and English)
All request must be via `POST` method, and text must be into `content` field via `multipart/form-data`. We have the following endpoints available:
- `/interpretext/language`: Detects content language.
- `/interpretext/tokenize`: Retrives content provided splitted into single tokens.
- `/interpretext/part-of-speech`: Tags whole words with its morphologic category.
- `/interpretext/summary`: Returns summary by gathering relevant phrases extracted from content.

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
