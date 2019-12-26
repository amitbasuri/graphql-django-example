## Sample User Onboarding GraphQL Django Python server

#### Setup Virtual env
```bash 
python3.6 -m venv venv
source venv/bin/activate
```

#### Run migrations and seed database
```bash
make migrate
make seed
```

#### Run server
```bash
python manage.py runserver
```

##### Navigate to http://127.0.0.1:8000/graphql/ for graphiQL UI