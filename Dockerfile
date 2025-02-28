FROM python:3.12-slim

RUN apt-get update -y && apt-get install curl -y

WORKDIR /app

COPY bambu /app/bambu

# Install the dependencies
RUN pip install --no-cache-dir -r /app/bambu/requirements.txt

EXPOSE 8080

# HEALTHCHECK --interval=10s --timeout=5s --start-period=3s --retries=3 \
#     CMD curl --fail http://localhost:8080/healthz || exit 1

CMD ["uvicorn", "bambu.main:app", "--host", "0.0.0.0", "--port", "8080"]
