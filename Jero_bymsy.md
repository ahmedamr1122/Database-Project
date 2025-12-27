## for database server

```
docker compose up -d
```

### for resetting database

```
docker compose down -v
docker compose up -d
```

## for running flask app

in another terminal

```
cd backend
python3 -m app
```

webpage: http://localhost:5000

kol el passwords are the same: password123

admin username: admin
ba2et el usernames mn gwa el seed file fi backend/database/seed_data.sql
