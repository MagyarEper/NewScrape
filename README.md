# Newscrapeer

Simple Hungarian news scraper + web viewer.

## Features

- Scrapes RSS feeds from major Hungarian news portals:
  - Telex
  - 24.hu
  - HVG
  - Index
  - 444.hu
  - Portfolio
- Stores articles in PostgreSQL with SQLAlchemy
- Displays latest articles in a Flask web app
- Supports search, source filtering, and pagination (100 per page)

## Requirements

- Python 3.10+
- PostgreSQL

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create environment file:

```bash
cp .env.example .env
```

4. Edit `.env` and set your PostgreSQL password.

## Run scraper

```bash
python main.py
```

## Run web app

```bash
python web/app.py
```

Open in browser: http://127.0.0.1:5000

## Deploy (Render + Neon)

This app is dynamic (Flask + PostgreSQL), so GitHub Pages is not suitable.

1. Create a free PostgreSQL database on Neon and copy its connection string.
2. In Render, create a new Web Service from this repository.
3. Render will detect `render.yaml` automatically.
4. In Render environment variables, set:

  - `DATABASE_URL` = your Neon PostgreSQL URL

5. Deploy the service.

### Manual Render settings (if you do not use render.yaml)

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn web.app:app`

## Project layout

- `main.py`: scraper entrypoint
- `fetchers/`: RSS source fetchers
- `models/`: database and SQLAlchemy models
- `web/`: Flask app, templates, styles
