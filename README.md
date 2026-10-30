# GekayRealEstate
GekayRealEstate is a realestate management system. The user can easily book any villa or homes that listed in the website.

## Prerequisites

* Python 3.14
* Django 5.2
* SQLite (included with Python)

![Gekay Real Estate](https://github.com/akhilgkrishnan/GekayRealEstate/assets/22231095/9f3b629b-9dff-4d00-8a7e-6ad3bec7c961)

## Local Windows setup

1. Install Python 3.14. PostgreSQL is not required for local development.
2. Create a virtual environment and install dependencies:

   ```powershell
   py -3.14 -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```powershell
   DJANGO_SECRET_KEY=replace-with-a-local-secret
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   ```

4. Apply migrations, create an administrator, and start the server:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

Open <http://127.0.0.1:8000/> after the server starts. Email is sent to the
console unless `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are configured.

To prepare, validate, migrate, test, and start the project with one command,
double-click `run.bat` or run it from PowerShell:

```powershell
.\run.bat
```

To populate the local SQLite database with 100 sample properties:

```powershell
python manage.py seed_demo_data
```
