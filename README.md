
A Server-Sent Events (SSE) based time-series streaming application with PostgreSQL integration. This project allows for real-time event streaming, historical data retrieval, and configurable intervals for event generation, all wrapped in a Dockerized setup.

---

## Key Features

1. **Real-Time Streaming**:
   - The `/stream` endpoint streams time-series events continuously using **Server-Sent Events (SSE)**.

2. **Historical Data Retrieval**:
   - The `/history` endpoint retrieves the last N events stored in the PostgreSQL database.

3. **Customizable Event Interval**:
   - The `/set_interval` endpoint allows users to configure the interval for time-series event generation.

4. **Fully Dockerized**:
   - Both the **Flask application** and **PostgreSQL database** are containerized for easy deployment using Docker.

---

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose** must be installed on your machine.
- Python 3+ is recommended if running locally without Docker.

---

### Installation

1. Clone the repository:
```shell script
git clone https://github.com/IamMashed/timeSeriesEventEmitter.git
cd timeSeriesEventEmitter
```

---

### Usage

#### Dockerized Setup

1. Start the application:
```shell script
docker-compose up --build
```

2. Access the endpoints using the default port (e.g., http://localhost:5000). Modify the configuration in the `docker-compose.yml` file if needed.

#### Database Initialization (First-Time Setup)

1. Start an interactive shell inside the Flask application container:
```shell script
docker exec -it <container-name> flask shell
```

2. Initialize the database:
```python
from app import db
db.create_all()
```

3. Exit the shell:
```shell script
exit
```

---

### Core Endpoints

1. **`/stream`**:
   - Streams time-series events. Access it via:
```shell script
curl http://localhost:5000/stream
```

2. **`/history`**:
   - Retrieves the last N events from the database. Example usage:
```shell script
curl http://localhost:5000/history?count=10
```

3. **`/set_interval`**:
   - Changes the interval for time-series event generation. Example usage:
```shell script
curl -X POST http://localhost:5000/set_interval -d '{"interval": 5}'
```

---

### Project Structure

- **Flask app**: Manages the SSE streaming and API logic.
- **PostgreSQL database**: Stores historical events.
- **Docker Compose**: Orchestrates the Flask app and PostgreSQL as containers.

---

### Contributing
Feel free to fork the repository, report issues, or propose changes via pull requests.
