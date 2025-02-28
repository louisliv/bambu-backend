FROM python:3.12-slim AS python-builder

RUN pip install poetry

WORKDIR /app
COPY poetry.toml pyproject.toml poetry.lock /app/

RUN poetry install --no-root


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTEapp=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && apt-get install curl -y

WORKDIR /app

COPY --from=python-builder /app/.venv /app/.venv

COPY backend /app/backend

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=3s --retries=3 \
    CMD curl --fail http://localhost:8080/healthz || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
