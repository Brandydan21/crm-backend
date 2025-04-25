test db
```
podman run -d \
  --name crm-db \
  -e POSTGRES_DB=crm_db \
  -e POSTGRES_USER=crm_user \
  -e POSTGRES_PASSWORD=supersecret \
  -v $(pwd)/pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  docker.io/postgres:16

```

run to create groups 
```
python manage.py shell
>>> from apps.accounts.setup.group_setup import create_groups
>>> create_groups()
```

create test company and user
```
from apps.accounts.setup.set_up_company_owner import create_owner
create_owner()
```
create a superuser (admin)
```
from apps.accounts.setup.superuser_setup import superuser_setup
create_super_admin()
```