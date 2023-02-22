# Git Check Alive

Educational project to gather data about GitHub projects.

## Components

1. API tries to get data from Cache, then falls back to publishing refresh task via Bus
1. Worker listens for Bus and gather data from GitHub API upon receiving appropriate task

```mermaid
graph LR
  actor((actor))
  github((github))

  subgraph project
    api
    worker
    bus
    cache[(cache)]
  end

  actor --> api
  api --> bus --> worker
  worker --> github
  api & worker -.-> cache
```

## Sample scenarios

### Background refresh

```mermaid
sequenceDiagram
  User->>Api: GET /repo/OWNER/NAME
  Api-->>User: Could not find repository data, please return in a moment

  User->>Api: GET /repo/OWNER/NAME
  Api-->>User: {...}
```

### Force refresh

```mermaid
sequenceDiagram
  User->>Api: GET /repo/OWNER/NAME
  Api-->>User: Could not find repository data, please return in a moment

  User->>Api: POST /repo/OWNER/NAME/refresh {"token": ...}
  Api-->>User: {"task": TASK_ID, ...}

  User->>Api: GET /task/TASK_ID
  Api-->>User: {"finished": true, ...}

  User->>Api: GET /repo/OWNER/NAME
  Api-->>User: {...}
```

## Local usage

```
$ docker-compose up --build
$ http 127.0.0.1:8081/repo/nodejs/node/refresh token=YOUR_GITHUB_TOKEN
$ http 127.0.0.1:8081/repo/nodejs/node
```
