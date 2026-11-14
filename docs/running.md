# Running it in containers, and the settings

## Run it in containers

With Docker, and without installing anything else:

```bash
cp .env.example .env     # then fill in the two values; the file says how
mise run docker:up       # or: docker compose up --build --detach --wait
```

Open http://localhost:8080. This runs the `production` settings with PostgreSQL and gunicorn,
as a user without root rights, with the migrations applied before the application starts.
The demo users do not exist here, because debug is off. Make a user of your own:

```bash
docker compose exec web python manage.py createsuperuser
```

`docker compose down` stops it and keeps the data. Add `--volumes` to throw the data away.

## Settings

| File | For | Debug | Database |
|---|---|---|---|
| `local` | Your machine | On, unless `DJANGO_DEBUG=false` | SQLite |
| `test` | The test run | Off | SQLite, in memory |
| `staging` | A rehearsal server | Off | PostgreSQL |
| `production` | A server | Off | PostgreSQL |

`staging` is `production` with a shorter HTTPS promise: browsers are told to insist on HTTPS for
an hour instead of a year, without subdomains and without the preload list. Preload is off in
`production` too unless you set `DJANGO_HSTS_PRELOAD=true`: leaving the browsers' list takes months. Both stop with the name of the variable when a value is missing, and both
refuse the key that ships with the code. Everything that can be set is listed in
[`project/settings/env.py`](../project/settings/env.py). `mise run check:deploy` runs the
deployment check of the framework on both.
