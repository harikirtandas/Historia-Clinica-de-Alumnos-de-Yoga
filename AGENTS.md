# Repository Guidelines

## Project Structure & Module Organization
- `app/` is the Flask application package.
- `app/models/` contains SQLAlchemy models (e.g., `app/models/alumno.py`).
- `app/controllers/` is reserved for route/controller logic.
- `app/templates/` holds Jinja templates.
- `app/static/` stores CSS, JS, and images.
- `run.py` is the entry point for local development.
- `config.py` loads environment config and database settings.
- `instance/` may contain local state like the SQLite database.

## Build, Test, and Development Commands
- `python3 -m venv venv` creates a virtual environment.
- `source venv/bin/activate` activates it (macOS/Linux).
- `pip install -r requirements.txt` installs dependencies.
- `python run.py` starts the dev server (debug mode enabled in `run.py`).
- `pip freeze > requirements.txt` updates dependency pins when new packages are added.

## Coding Style & Naming Conventions
- Use 4-space indentation and standard PEP 8 formatting.
- Python modules and functions use `snake_case`.
- Classes use `CamelCase` (e.g., `Alumno`).
- Constants should be `UPPER_SNAKE_CASE`.
- Keep imports grouped: standard library, third-party, local.

## Testing Guidelines
- No test suite is currently configured.
- If adding tests, prefer `pytest` with files named `test_*.py` under a `tests/` directory.
- Example run command (once added): `pytest`.

## Commit & Pull Request Guidelines
- No Git history is present in this repository, so commit conventions are unknown.
- Use clear, imperative commit messages (e.g., "Add alumno model validation").
- PRs should include a summary, testing notes, and screenshots for UI changes.

## Security & Configuration Tips
- Create a `.env` file for `SECRET_KEY` and local configuration.
- Do not commit credentials or the SQLite database file.
- The app is intended for local use; handle student medical data carefully.
