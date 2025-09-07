# Simple Flask app instrumented with Prometheus client
FROM python:3.11-slim

WORKDIR /app
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py app.py

# Use a non-root user for better security
RUN useradd -ms /bin/bash appuser
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
