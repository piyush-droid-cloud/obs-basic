# Observability Starter: Monitor a Web App with Prometheus + Grafana (Docker Desktop)

This project demonstrates how to **monitor a simple web application** using **Prometheus** and **Grafana**, containerized with **Docker Desktop**.  
It collects metrics like **CPU, Memory, and Request Count**, and visualizes them in Grafana dashboards.  

## 📌 Features
- ✅ Web app containerized with Docker  
- ✅ Metrics collection using **Prometheus**  
- ✅ Beautiful visualizations in **Grafana**  
- ✅ Easy setup with `docker-compose`  
- ✅ Beginner-friendly observability project  

## 🛠️ Tech Stack
- **Prometheus** → Metrics collection  
- **Grafana** → Dashboards & visualization  
- **Docker + Docker Compose** → Container orchestration  
- **Web App** → (Flask / Node.js / Nginx – whichever you used)  

## Quickstart
```bash
# 1) From this folder:
docker compose up -d --build

# 2) Open UIs
# App:
http://localhost:8000/
# Prometheus:
http://localhost:9090/targets
# Grafana (admin/admin the first time):
http://localhost:3000/
```

A background `loadgen` container sends traffic to the app so you can see metrics moving.

## Create a basic Grafana dashboard (manually)
1. Login to Grafana → **New dashboard** → **Add visualization** → **Prometheus** datasource.
   (Remember if using both Grafana and prometheus with docker desktop then put URL connection this http://prometheus:9090/)
3. Use these example queries:

- **Requests per second (by endpoint)**  
  ```promql
  sum(rate(http_requests_total[1m])) by (endpoint)
  ```

- **Error rate (5xx)**  
  ```promql
  sum(rate(http_requests_total{http_status=~"5.."}[5m]))
  ```

- **p95 latency (seconds)**  
  ```promql
  histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le))
  ```

- **App memory (RSS bytes)**  
  ```promql
  process_resident_memory_bytes{job="app"}
  ```

- **App CPU (approx % on 1 core)**  
  ```promql
  rate(process_cpu_seconds_total{job="app"}[1m]) * 100
  ```

3. Save the dashboard inside the default folder *Starter* (already provisioned).

## Stop & clean
```bash
docker compose down
# or to also clear volumes:
docker compose down -v
```
**##Future Improvements**

Add Alertmanager for alerts (CPU, Memory thresholds)
Add Loki for log monitoring
Deploy on Kubernetes for scaling
Export Grafana dashboards as JSON
