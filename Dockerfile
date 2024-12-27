FROM --platform=$BUILDPLATFORM node:22-slim AS node-builder
WORKDIR /code
COPY package.json package-lock.json ./
RUN npm install

COPY index.html svelte.config.js tsconfig.app.json tsconfig.json tsconfig.node.json vite.config.ts postcss.config.js tailwind.config.ts components.json ./
COPY public/ public/ 
COPY frontend/ frontend/

RUN npm run build



FROM python:3.12-slim AS python-builder

RUN pip install poetry

WORKDIR /code
COPY poetry.toml pyproject.toml poetry.lock /code/

RUN poetry install --no-root


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY --from=node-builder /code/dist/ /code/dist/
COPY --from=python-builder /code/.venv /code/.venv

COPY backend /code/backend

ENV VIRTUAL_ENV=/code/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
