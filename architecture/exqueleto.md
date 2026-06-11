# Estrutura da Solução

```text
AnprPlatform.sln
│
├── docker-compose.yml
├── docker-compose.override.yml
├── .env
├── README.md
│
├── src
│
│   ├── BuildingBlocks
│   │
│   │   ├── Anpr.SharedKernel
│   │   ├── Anpr.Contracts
│   │   ├── Anpr.EventBus
│   │   ├── Anpr.Storage
│   │   ├── Anpr.Common
│   │   └── Anpr.Infrastructure
│   │
│   ├── Services
│   │
│   │   ├── Anpr.Api
│   │   │
│   │   ├── Controllers
│   │   ├── SignalR
│   │   ├── Authentication
│   │   ├── Authorization
│   │   ├── Swagger
│   │   └── Program.cs
│   │
│   │
│   │   ├── Anpr.AI.Worker
│   │   │
│   │   ├── CameraConsumers
│   │   ├── Yolo
│   │   ├── OCR
│   │   ├── ANPR
│   │   ├── VideoAnnotation
│   │   ├── Snapshot
│   │   ├── RtspPublisher
│   │   └── BackgroundServices
│   │
│   │
│   │   ├── Anpr.DeviceGateway
│   │   │
│   │   ├── Esp32
│   │   ├── Arduino
│   │   ├── MQTT
│   │   ├── Http
│   │   └── WebSocket
│   │
│   │
│   │   └── Anpr.MediaGateway
│   │
│   │       ├── MediaMTX
│   │       ├── Rtsp
│   │       ├── WebRTC
│   │       └── FFmpeg
│   │
│   │
│   ├── Modules
│   │
│   │   ├── Tenants
│   │   ├── Cameras
│   │   ├── Users
│   │   ├── Vehicles
│   │   ├── Detections
│   │   ├── AccessControl
│   │   ├── GateControllers
│   │   ├── Dashboard
│   │   └── Notifications
│   │
│   │
│   ├── Infrastructure
│   │
│   │   ├── Persistence
│   │   ├── EntityFramework
│   │   ├── SqlServer
│   │   ├── PostgreSql
│   │   ├── Redis
│   │   ├── BlobStorage
│   │   └── Migrations
│   │
│   │
│   └── Frontend
│
│       ├── dashboard-react
│       └── admin-react
│
│
├── docker
│
│   ├── mediamtx
│   │     └── mediamtx.yml
│   │
│   ├── sqlserver
│   │
│   ├── postgres
│   │
│   ├── redis
│   │
│   └── nginx
│
│
├── docs
│
│   ├── Architecture.md
│   ├── DataModel.md
│   ├── Flow.md
│   ├── Deployment.md
│   ├── Docker.md
│   ├── Api.md
│   └── Roadmap.md
│
│
└── tests

    ├── UnitTests
    ├── IntegrationTests
    └── PerformanceTests
```

---

# Docker Compose

```yaml
services:

  mediamtx:

    image: bluenviron/mediamtx:latest

    ports:
      - "8554:8554"
      - "8889:8889"

    volumes:
      - ./docker/mediamtx/mediamtx.yml:/mediamtx.yml

  sqlserver:

    image: mcr.microsoft.com/mssql/server:2022-latest

    environment:

      ACCEPT_EULA: Y

      SA_PASSWORD: YourStrongPassword123!

    ports:

      - "1433:1433"

  redis:

    image: redis:latest

    ports:

      - "6379:6379"

  api:

    build:

      context: .

      dockerfile: src/Services/Anpr.Api/Dockerfile

    depends_on:

      - sqlserver
      - redis
      - mediamtx

  ai-worker:

    build:

      context: .

      dockerfile: src/Services/Anpr.AI.Worker/Dockerfile

    depends_on:

      - mediamtx
      - api

  device-gateway:

    build:

      context: .

      dockerfile: src/Services/Anpr.DeviceGateway/Dockerfile

  dashboard:

    build:

      context: ./src/Frontend/dashboard-react

    ports:

      - "3000:80"
```

---

# Streams do MediaMTX

Cada câmera possui dois streams.

```text
cam01
```

Vídeo original.

```text
cam01-ai
```

Vídeo anotado pelo YOLO.

---

# Fluxo Geral

```text
Camera

      │

      ▼

MediaMTX

      │

      ▼

AI Worker

(YOLO + OCR)

      │

      ├────────► MediaMTX (cam-ai)

      │

      └────────► ASP.NET Core API

                          │

                          ▼

                   SQL Server

                          │

          ┌───────────────┴───────────────┐

          ▼                               ▼

      Dashboard                      ESP32 Gateway

          │                               │

          ▼                               ▼

      SignalR                       Abrir Cancela
```

---

# Serviços

## Anpr.Api

* REST API
* SignalR
* JWT
* Autenticação
* Controle de acesso
* Multi Tenant

---

## Anpr.AI.Worker

* Consome RTSP
* YOLO
* OCR
* ANPR
* Snapshot
* Publica stream anotado
* Envia eventos

---

## DeviceGateway

* HTTP

* MQTT

* WebSocket

* ESP32

* Arduino

* Relés

---

## Dashboard

* React

* WebRTC

* SignalR

* Histórico

* Pesquisa de placas

* Mapa das câmeras

---

# Banco de Dados

```text
Tenant

    ├────────────< Camera

    │

    ├────────────< User

    │

    ├────────────< AuthorizedVehicle

    │

    └────────────< GateController

                        │

Camera                  │

    │                   │

    └────────< DetectionEvent

                    │

                    ├──────── Snapshot

                    │

                    └──────── GateAccessLog
```

---

# Roadmap Futuro

* Reconhecimento facial

* Classificação de veículos

* Cor do veículo

* Marca/modelo

* Rastreamento entre câmeras

* Dashboard GIS

* Cluster MediaMTX

* Kubernetes

* RabbitMQ

* Elasticsearch

* Prometheus

* Grafana

* OpenTelemetry

* API pública

* Aplicativo móvel

* SaaS Multi-Tenant
