test db
```
podman run -d \
  --name crm-db \
  -e POSTGRES_DB=crm_db \
  -e POSTGRES_USER=crm_user \
  -e POSTGRES_PASSWORD=supersecret \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  docker.io/postgres:16
```

run to create groups 
```
python manage.py shell
>>> from apps.accounts.setup.group_setup import create_groups
>>> create_groups()
```