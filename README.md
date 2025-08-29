# Project3_-Kafka-Hello
Kafka Hello (Docker + Kafka CLI)
# Kafka Hello (Docker + Kafka CLI)

A tiny, Windows-friendly project that runs **Apache Kafka** in Docker and shows messages flowing from a **producer** to a **consumer** using Kafka’s built‑in CLI.

> **ELI5:** Kafka is a **post office**. A **topic** is a **mailbox**. A **producer** drops letters into the mailbox. A **consumer** waits and reads them.

---

## ✅ What you’ll get

* One‑file Kafka stack via **Docker Compose** (KRaft mode; no ZooKeeper).
* Scripts to **start/stop**, **create topics**, **produce**, and **consume**.
* Works great on **Windows 10/11 + PowerShell**.

---

## 📦 Prerequisites

* **Docker Desktop** installed and running
* **PowerShell** (the default terminal on Windows)

> If your path has spaces (e.g., `D:\one drive\...`), always **quote** it in commands.

---

## 🚀 Quick Start

From the project folder (where `docker-compose.yml` lives):

```powershell
# 1) Start Kafka
./scripts/start.ps1

# 2) Create a topic (mailbox)
./scripts/topic-create.ps1 hello-topic

# 3) Open a consumer (waits for messages)
./scripts/consume.ps1 hello-topic
```

Open **another** PowerShell window:

```powershell
# 4) Open a producer and type lines; press Enter to send
./scripts/produce.ps1 hello-topic
# e.g.
hello
kafka
works!
```

You’ll see those lines appear in the consumer window.

To stop everything:

```powershell
./scripts/stop.ps1
```

---

## 🧠 How it’s wired (one paragraph)

* The container listens on `9092` (for in‑Docker clients) and `29092` (for your Windows host). Inside Docker we use `kafka:9092`. On your host we use `localhost:29092`. Our scripts run CLI **inside** the container, so you don’t need Java or Kafka installed locally.

---

## 🗂️ Project Structure

```
kafka-hello/
├─ docker-compose.yml
├─ README.md
├─ .gitignore
└─ scripts/
   ├─ start.ps1
   ├─ stop.ps1
   ├─ topic-create.ps1
   ├─ consume.ps1
   └─ produce.ps1
```

---

## 🧾 File: `docker-compose.yml`

```yaml
# No "version:" key needed
services:
  kafka:
    image: apache/kafka:3.7.1
    container_name: kafka
    ports:
      - "9092:9092"     # for containers on the same Docker network
      - "29092:29092"   # for clients on your Windows host (localhost:29092)
    environment:
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_NODE_ID: 1
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093,PLAINTEXT_HOST://:29092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      # Single-broker safe defaults for internal topics
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
    restart: unless-stopped
```

---

## 🧾 File: `scripts/start.ps1`

```powershell
# Start Kafka and show status
docker compose up -d
docker compose ps
```

## 🧾 File: `scripts/stop.ps1`

```powershell
# Stop and remove the stack
docker compose down
```

## 🧾 File: `scripts/topic-create.ps1`

```powershell
param(
  [Parameter(Mandatory=$true)][string]$Topic
)

docker exec kafka bash -lc \
  "/opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic $Topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1"
```

## 🧾 File: `scripts/consume.ps1`

```powershell
param(
  [Parameter(Mandatory=$true)][string]$Topic
)

docker exec -it kafka bash -lc \
  "/opt/kafka/bin/kafka-console-consumer.sh --topic $Topic --bootstrap-server localhost:9092 --from-beginning"
```

## 🧾 File: `scripts/produce.ps1`

```powershell
param(
  [Parameter(Mandatory=$true)][string]$Topic
)

docker exec -it kafka bash -lc \
  "/opt/kafka/bin/kafka-console-producer.sh --topic $Topic --bootstrap-server localhost:9092"
```

## 🧾 File: `.gitignore`

```gitignore
.DS_Store
*.pyc
__pycache__/
.venv/
```

---

## 🔍 Troubleshooting

* **Consumer shows nothing / seems stuck** → It’s waiting. Open the producer and type messages.
* **PowerShell vs. CMD** → Use **PowerShell**. If you see errors with `type nul >`, that’s a CMD trick; in PowerShell use our scripts or `New-Item`.
* **Spaces in path** → Always quote: `cd "D:\one drive\..."`.
* **Cannot bind port 29092** → Another program is using it; change the mapping in `docker-compose.yml` to e.g. `39092:29092` and reconnect with `localhost:39092` from host clients.
* **Logs** → `docker compose logs -f kafka`

---

## 🧭 What’s next (ideas)

* Add a tiny **Python** producer/consumer (v2) using `kafka-python`.
* Add **Kafka UI** service (Provectus) to browse topics in the browser.
* Add **Kafka Connect + Postgres** (v3) to stream messages into a table.

---

---

## 📜 License (MIT)
MIT License

Copyright (c) 2025 PAVAN TEJA SRIPATI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### 🙌 Credits

Built with ❤️ for fast local Kafka demos on Windows.
