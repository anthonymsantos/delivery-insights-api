# Delivery Insights API

Backend service built with FastAPI for managing delivery events and notes.
This project is being developed as a foundation for a cloud-native, AI-integrated backend system on AWS.

### 🚀 Goals

- Build a clean, well-structured REST API with FastAPI

- Deploy the service to AWS (EC2 → load balancing → scaling)

- Integrate AWS AI services (e.g., Bedrock/Comprehend) for text analysis

- Practice production-ready backend patterns (auth, logging, config, testing)

### 🧱 Tech Stack

- Backend: Python 3.12, FastAPI

- Server: Uvicorn

- (Planned) Cloud: AWS (EC2, RDS, S3, IAM)

- (Planned) AI: AWS Bedrock / Comprehend

### 📦 Current Features (v1)

- Basic FastAPI app

- Health endpoint (GET /)

- Local development setup with virtual environment

- More endpoints (CRUD for deliveries), database integration, and AWS deployment are coming next.

### 🛠 Local Setup
git clone git@github.com:anthonymsantos/delivery-insights-api.git

cd delivery-insights-api

python3 -m venv venv

source venv/bin/activate

pip install fastapi uvicorn

uvicorn main:app --reload


#### Open:

- http://127.0.0.1:8000

- http://127.0.0.1:8000/docs
 (interactive API docs)
 
### 🗺 Roadmap

◼️ CRUD endpoints for deliveries

◼️ Database integration (SQLite → PostgreSQL/RDS)

◼️ Auth (JWT)

◼️ AWS deployment (EC2 + security groups)

◼️ Load balancer + auto scaling

◼️ AI integration (text summarization / analysis)

◼️ Tests + CI

## 📚 Notes

This repo is part of a structured learning sprint focused on:

- Backend engineering fundamentals

- Cloud-native system design on AWS

- Practical AI service integration
