# Fluxo de Funcionamento

## Visão Geral

```text
Hikvision Camera
        │
        │ RTSP
        ▼
    MediaMTX
        │
        │ RTSP
        ▼
Serviço IA (.NET)
(YOLO + OCR + ANPR)
        │
        ├──────────────► ASP.NET Core Web API
        │                        │
        │                        ▼
        │                Entity Framework Core
        │                        │
        │                        ▼
        │                  Banco de Dados
        │
        └──────────────► MediaMTX (cam01-ai)
                                 │
                                 ▼
                          Dashboard WebRTC

ASP.NET Core Web API
        │
        ▼
      SignalR
        │
        ▼
Dashboard Web

ASP.NET Core Web API
        │
        ▼
 ESP32 / Arduino
        │
        ▼
 Acionamento da Cancela
```

---

## Fluxo de Funcionamento

### 1. Captura do vídeo

A câmera Hikvision envia continuamente o stream de vídeo através do protocolo **RTSP** para o **MediaMTX**, que centraliza e redistribui o fluxo para os consumidores do sistema.

---

### 2. Processamento por Inteligência Artificial

O serviço de IA desenvolvido em **.NET** consome o stream RTSP do MediaMTX e executa o pipeline de processamento:

* Detecção de veículos utilizando YOLO
* Localização da placa
* OCR (Reconhecimento Óptico de Caracteres)
* Reconhecimento automático de placas (ANPR)
* Desenho das anotações sobre o vídeo
* Captura de snapshots dos eventos

---

### 3. Publicação do stream processado

Após o processamento, o serviço publica um novo stream no MediaMTX contendo as anotações.

Exemplo:

* `cam01` → Stream original
* `cam01-ai` → Stream anotado pela IA

---

### 4. Registro dos eventos

Sempre que uma placa é identificada, o serviço envia um evento para a **ASP.NET Core Web API** contendo informações como:

* Placa reconhecida
* Nível de confiança
* Data e hora
* Identificação da câmera
* Snapshot do veículo

---

### 5. Persistência dos dados

A Web API utiliza **Entity Framework Core** para armazenar todas as informações no banco de dados, permitindo auditoria, pesquisas e geração de relatórios.

---

### 6. Atualização do Dashboard

A Web API envia os eventos em tempo real utilizando **SignalR**.

O Dashboard apresenta:

* Vídeo ao vivo
* Placa detectada
* Confiança do OCR
* Snapshot do veículo
* Histórico de detecções
* Status da câmera

---

### 7. Controle de acesso

Após validar a placa no banco de dados, a Web API pode enviar um comando para um dispositivo **ESP32/Arduino**.

O dispositivo recebe a solicitação e aciona um relé responsável pela abertura da cancela ou portão.

---

## Benefícios da arquitetura

* Apenas uma conexão RTSP por câmera.
* Escalável para dezenas ou centenas de câmeras.
* Separação entre vídeo original e vídeo processado.
* Dashboard em tempo real via WebRTC.
* Comunicação desacoplada entre IA, API e dispositivos físicos.
* Fácil manutenção e expansão futura.
