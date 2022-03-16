# Setup
- `python -m venv venv`
- `. venv/bin/activate`
- `pip install -r requirements.txt`
- `Create .env in project directory (see .env.example) and change the SECRET_KEY`
- `python manage.py migrate` (you might need to temporarily comment out the Misconceptions model from forms.py)

Test webserver:
- `python manage.py runserver PORT`

# Administration
- `python manage.py createsuperuser`

# Deploy
- Set `DEBUG=False` in .env
- Set suitable value for `ALLOWED_HOSTS`