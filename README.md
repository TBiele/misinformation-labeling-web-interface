# Setup
`python -m venv venv`
`. venv/bin/activate`
`pip install -r requirements.txt`
`python manage.py migrate` (you might need to comment out forms)
`Create .env in project directory and add SECRET_KEY=<secret key>`

Test webserver:
`python manage.py runserver PORT`

# Administration
`python manage.py createsuperuser`

# Deploy
`Set DEBUG=False` in .env
`Set suitable value for ALLOWED_HOSTS`