# Tecnologias Utilizadas

## Arquitetura

O projeto utiliza uma arquitetura modular baseada em microsserviços e processamento de vídeo em tempo real.

---

## Câmeras

* Hikvision IP Camera
* RTSP
* ONVIF
* H.264 / H.265

---

## Streaming

### MediaMTX

Responsável por centralizar e redistribuir os streams de vídeo.

Protocolos suportados:

* RTSP
* WebRTC
* HLS
* LL-HLS
* SRT

---

## Inteligência Artificial

Serviço desenvolvido em **C#/.NET** responsável pelo processamento dos vídeos.

### Componentes

* YOLO
* OCR
* ANPR
* OpenCV
* ONNX Runtime

### Funcionalidades

* Detecção de veículos
* Localização de placas
* Reconhecimento de caracteres
* Geração de vídeo anotado
* Captura de snapshots

---

## Backend

### ASP.NET Core Web API

Responsável por:

* Receber eventos da IA
* Regras de negócio
* Autenticação
* Controle de acesso
* Integração com dispositivos
* APIs REST

---

## Persistência

### Entity Framework Core

ORM utilizado para acesso ao banco de dados.

Compatível com:

* SQL Server
* PostgreSQL

---

## Comunicação em Tempo Real

### SignalR

Permite atualizar o dashboard instantaneamente sempre que uma nova placa for detectada.

---

## Dashboard

Pode ser desenvolvido utilizando:

* Blazor
* React
* Angular

Consome:

* WebRTC para vídeo ao vivo
* SignalR para eventos em tempo real
* REST API para consultas

---

## Dispositivos IoT

### ESP32 / Arduino

Responsável pelo acionamento de dispositivos físicos.

Exemplos:

* Relé de cancela
* Portão eletrônico
* LEDs indicadores
* Sirenes
* Sensores

---

## Protocolos

| Protocolo         | Finalidade                        |
| ----------------- | --------------------------------- |
| RTSP              | Streaming entre câmera e servidor |
| WebRTC            | Visualização no navegador         |
| HTTP REST         | Comunicação entre serviços        |
| SignalR           | Eventos em tempo real             |
| MQTT *(opcional)* | Comunicação IoT escalável         |

---

## Estrutura Geral

```text
Camera
    │
    ▼
MediaMTX
    │
    ▼
Serviço IA (.NET)
    ├──► MediaMTX (Stream Anotado)
    └──► ASP.NET Core API
                │
                ▼
        Entity Framework Core
                │
                ▼
         Banco de Dados
                │
        ┌───────┴────────┐
        ▼                ▼
   Dashboard        ESP32/Arduino
```
