# GekayRealEstate dependencies

## Runtime

- Python 3.14.6
- Django 5.2
- SQLite through Python's built-in `sqlite3` module

SQLite is the local development database configured in
`djangofirst/settings.py`. It does not need a separate pip package.

## Python packages

The installable package manifest is
[`requirements.txt`](./requirements.txt). It contains:

- Django and `python-dotenv` for the web application and environment loading.
- Pillow for image handling.
- WhiteNoise for static-file serving.
- Gunicorn for non-Windows deployment.
- `astroid`, `autopep8`, `isort`, and `pylint` for code quality and formatting.

Install or restore the packages with:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

On Windows, you can double-click
[`install_dependencies.bat`](./install_dependencies.bat). It creates the
`venv\` environment when needed, installs missing packages, checks package
consistency, validates Django, and applies SQLite migrations.

Verify package consistency with:

```powershell
.\venv\Scripts\python.exe -m pip check
```

## Project files

- `.env` - local environment configuration. Keep secrets and passwords out of
  source control.
- `db.sqlite3` - local SQLite database created and migrated by Django.
- `requirements.txt` - pip dependency manifest.
- `venv\` - local Python virtual environment; recreate it rather than
  committing it.

The current `.env` keys used by the project are:

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEMO_USERNAME`
- `DEMO_PASSWORD`
- `DEMO_EMAIL`

## Project validation

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py migrate
```

On Windows, run [`seed_demo_data.bat`](./seed_demo_data.bat) to create the
default 100 demo listings and demo realtors. To choose another listing count,
pass it as the first argument:

```powershell
.\seed_demo_data.bat 25
```
