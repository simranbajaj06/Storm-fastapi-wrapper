# STORM FastAPI Wrapper

This project wraps the Stanford STORM framework in a modular, production-ready FastAPI application. It exposes a clean API for querying STORM without writing output files to disk, and supports both normal and streamed responses.

---

## Setup Instructions 

### 1. Clone the Repository
git clone https://github.com/simranbajaj06/Storm-api.git
cd wrapstorm

### 2. Create .env file
Create a `.env` file in the root directory to store any secrets (e.g., API keys).

### 3. Install Dependencies with Poetry
Ensure Poetry is installed: https://python-poetry.org/docs/#installation

poetry install

### 4. Run Locally (Without Docker)
poetry run uvicorn app.main:app --host 0.0.0.1 --port 8000 --reload

---

## Docker Usage

### 1. Build the Docker Image
docker build -t storm-api .

### 2. Run the Container
docker run -p 8000:8000 storm-api

---

## API Usage

### POST /storm/query

Send a POST request with relevant parameters to query STORM.

#### Example cURL Command

curl -X POST http://0.0.0.1:8000/storm/query \
  -H "Content-Type: application/json" \
  -N \
  -d '{
        "topic": "Artificial Intelligence",
        "do_research": true,
        "do_generate_outline": true,
        "do_generate_article": true,
        "do_polish_article": true,
        "stream": true
      }'

#### Request Body Parameters

- topic (string): The topic to research and generate content about.
- do_research (boolean): Whether to run the research stage.
- do_generate_outline (boolean): Whether to generate an outline.
- do_generate_article (boolean): Whether to generate a full article.
- do_polish_article (boolean): Whether to polish the article.
- stream (boolean): Set to true to receive a streamed response.

#### Response
- If `stream` is false: standard JSON response.
- If `stream` is true: streamed newline-delimited text.

---

## Project Structure

wrapstorm/
├── src/
│   └── wrapstorm/
│       ├── api/             # FastAPI routes and request models
│       ├── core/            # STORM integration logic
│       ├── utils/           # Helper functions
│       ├── main.py          # Entry point for FastAPI app
│       └── storm/           # Cloned STORM repository
├── Dockerfile
├── pyproject.toml           # Poetry dependency file
├── poetry.lock
└── README.md

---

