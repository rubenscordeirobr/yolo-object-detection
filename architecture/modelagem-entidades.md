# Modelo de Dados

## Visão Geral

```text
Tenant
    │
    ├──────────────┐
    │              │
    ▼              ▼
Camera         ApplicationUser
    │
    │
    ▼
DetectionEvent
    │
    ├──────────────┐
    │              │
    ▼              ▼
Plate        Snapshot

Tenant
    │
    ▼
GateController (ESP32)
    │
    ▼
GateAccessLog
```

---

# Tenant

Representa um cliente do sistema.

Exemplo:

* Condomínio A
* Empresa XYZ
* Shopping Center
* Estacionamento Central

```text
Tenant
--------
Id
Name
Document
CreatedAt
IsActive
```

---

# Camera

Cada Tenant pode possuir diversas câmeras.

```text
Camera
--------
Id
TenantId
Name
Description
RtspPath
MediaMtxPath
IpAddress
Location
Model
IsActive
CreatedAt
```

Relacionamento:

```text
Tenant
    │
    └──────< Camera
```

---

# ApplicationUser

Usuários pertencentes ao Tenant.

```text
ApplicationUser
----------------
Id
TenantId
Name
Email
PasswordHash
Role
IsActive
```

Relacionamento:

```text
Tenant
    │
    └──────< User
```

---

# DetectionEvent

Evento gerado pela IA.

```text
DetectionEvent
--------------------
Id
CameraId
Plate
Confidence
VehicleType
OccurredAt
SnapshotId
Status
```

Relacionamento:

```text
Camera
    │
    └──────< DetectionEvent
```

---

# Snapshot

Imagem capturada durante a detecção.

```text
Snapshot
----------------
Id
DetectionEventId
FileName
StoragePath
Width
Height
CreatedAt
```

Relacionamento:

```text
DetectionEvent
      │
      └────── Snapshot
```

---

# AuthorizedVehicle

Lista de veículos autorizados.

```text
AuthorizedVehicle
-------------------------
Id
TenantId
Plate
Owner
Description
ValidUntil
IsActive
```

Relacionamento:

```text
Tenant
    │
    └──────< AuthorizedVehicle
```

---

# GateController

Controlador físico baseado em ESP32.

```text
GateController
--------------------
Id
TenantId
Name
IpAddress
MacAddress
Location
ApiKey
IsOnline
LastHeartbeat
```

Relacionamento:

```text
Tenant
    │
    └──────< GateController
```

---

# GateAccessLog

Registro das aberturas de cancela.

```text
GateAccessLog
-----------------------
Id
DetectionEventId
GateControllerId
Plate
AccessGranted
Reason
CreatedAt
```

Relacionamento:

```text
DetectionEvent
        │
        └──────< GateAccessLog >────── GateController
```

---

# CameraStream

Configuração dos streams publicados pelo MediaMTX.

```text
CameraStream
-----------------------
Id
CameraId
OriginalPath
ProcessedPath
Protocol
Enabled
```

Exemplo:

Original:

cam01

Processado:

cam01-ai

---

# Relacionamento Geral

```text
Tenant
│
├───────────────< Camera
│                     │
│                     ├──────────────< CameraStream
│                     │
│                     └──────────────< DetectionEvent
│                                         │
│                                         ├────────── Snapshot
│                                         │
│                                         └────────── GateAccessLog
│
├───────────────< ApplicationUser
│
├───────────────< AuthorizedVehicle
│
└───────────────< GateController
                              │
                              └────────── GateAccessLog
```

---

# Benefícios

* Arquitetura **multi-tenant** preparada para SaaS.
* Suporte a múltiplas câmeras por cliente.
* Suporte a múltiplos ESP32 por cliente.
* Histórico completo de detecções e acessos.
* Separação lógica dos dados por Tenant.
* Fácil expansão para adicionar módulos como visitantes, moradores, OCR facial, reconhecimento de veículos e integração com sistemas externos.
