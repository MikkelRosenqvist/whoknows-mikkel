# whoknows-mikkel

DevOps course — WhoKnows search engine

## About

A search engine application rewritten from a legacy Python 2 / Flask 0.5 codebase to modern Python 3 / Flask 3.x.

## Changes from legacy version

- Upgraded from Python 2 to Python 3
- Upgraded Flask from 0.5 to 3.1.0
- Fixed SQL injection vulnerabilities (parameterized queries)
- Replaced MD5 password hashing with Werkzeug's `generate_password_hash` (pbkdf2)
- Moved secrets to `.env` file (no more hardcoded secret key)
- Removed hardcoded admin user with known password from schema
- Fixed template bug (`description` → `content`)
- Added proper HTML structure to layout template
- Updated tests for Python 3

## Getting started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
cd src/backend
pip install -r requirements.txt
cp .env.example .env
```

### Initialize the database

```bash
cd src
make init
```

### Run the application

```bash
cd src
make run
```

The app runs at http://localhost:8080

### Run tests

```bash
cd src
make test
```

## Tech stack

- Python 3
- Flask 3.1.0
- SQLite
- Jinja2 templates
