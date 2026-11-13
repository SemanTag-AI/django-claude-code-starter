# Two stages. The first has the tools and makes everything. The second only runs it.

FROM python:3.14-slim-bookworm AS build
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /usr/local/bin/uv
WORKDIR /app
# Use the Python of the image, so that the environment still works in the second stage.
ENV UV_PYTHON_DOWNLOADS=never UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1

# Dependencies first: this layer is reused until the lock file changes.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --group production

COPY manage.py ./
COPY project project
COPY apps apps
COPY assets assets
# Compile the stylesheet and collect the static files. The settings refuse to load without
# their values, so they get stand-ins for these two commands. None of them ends up in the image.
RUN DJANGO_SETTINGS_MODULE=project.settings.production \
    DJANGO_SECRET_KEY=only-for-the-build-of-the-image \
    DJANGO_ALLOWED_HOSTS=build DJANGO_DATABASE_NAME=build DJANGO_DATABASE_USER=build \
    DJANGO_DATABASE_PASSWORD=build DJANGO_DATABASE_HOST=build \
    sh -c "uv run --no-sync python manage.py tailwind build && uv run --no-sync python manage.py collectstatic --noinput"


FROM python:3.14-slim-bookworm
# Not root: a break-in through the application gets an account that owns nothing.
RUN useradd --system --uid 10001 --no-create-home register
WORKDIR /app
COPY --from=build /app/.venv .venv
COPY --from=build /app/manage.py manage.py
COPY --from=build /app/project project
COPY --from=build /app/apps apps
COPY --from=build /app/staticfiles staticfiles
ENV PATH=/app/.venv/bin:$PATH \
    DJANGO_SETTINGS_MODULE=project.settings.production \
    PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER register
EXPOSE 8000
# Asks the application whether it and its database answer, under the first host it listens to.
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=5 CMD ["python", "-c", "import os, urllib.request; host = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')[0].strip(); request = urllib.request.Request('http://127.0.0.1:8000/healthz/', headers={'Host': host}); urllib.request.urlopen(request, timeout=3)"]
CMD ["gunicorn", "project.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-"]
