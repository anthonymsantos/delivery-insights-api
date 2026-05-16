# Delivery Insights API

Delivery Insights API is a secure, cloud-deployed backend service for managing delivery records and operational delivery data.

This project was built as a hands-on backend and AWS cloud engineering portfolio project. It focuses on REST API design, authentication, database persistence, containerization, automated testing, CI, and AWS deployment.

## 🚀 Project Goals

- Build a clean, production-minded REST API with FastAPI
- Apply backend engineering patterns such as routing, validation, dependency injection, and repository-based data access
- Use PostgreSQL for relational persistence
- Secure write operations with JWT authentication and ownership-based authorization
- Containerize the application with Docker
- Deploy the service to AWS using EC2 and Amazon RDS
- Use IAM roles for AWS service access without hardcoded AWS credentials
- Prepare the project for future AWS integrations such as S3 and Amazon Bedrock

## 🧱 Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT bearer authentication
- **Testing:** Pytest, FastAPI TestClient
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud:** AWS EC2, Amazon RDS, IAM

## ✅ Current Features

- FastAPI REST API for managing delivery records
- PostgreSQL database integration
- SQLAlchemy ORM models and repository layer
- Alembic database migration setup
- JWT-based user registration and login
- Protected create, update, and delete routes
- Ownership-based authorization for delivery records
- Pagination, filtering, sorting, and structured list responses
- Environment-based configuration using `.env`
- Dockerized application runtime
- Docker Compose support for local development
- Deployment to AWS EC2
- Amazon RDS PostgreSQL integration
- EC2 IAM role configured for future AWS service access
- Automated test suite with isolated test database
- GitHub Actions CI workflow for running tests on push and pull request

## 🔐 Authentication & Authorization

The API supports JWT-based authentication.

Users can:

- Register an account
- Log in to receive an access token
- Authorize requests using bearer authentication
- Create delivery records as an authenticated user
- Update or delete only delivery records they own

Unauthorized requests return `401 Unauthorized`.

Authenticated users attempting to modify another user’s delivery record receive `403 Forbidden`.

## 📦 API Capabilities

Delivery records support:

- Create delivery
- List deliveries
- Get delivery by ID
- Update delivery
- Delete delivery
- Filter by status or driver name
- Sort by timestamp, driver name, or status
- Paginate results with limit and offset
- Return structured response metadata

## 🛠 Local Development Setup

Clone the repository:\
git clone git@github.com:anthonymsantos/delivery-insights-api.git cd delivery-insights-api

Create and activate a virtual environment:\
python3 -m venv venv\
source venv/bin/activate

Install dependencies:\
pip install -r requirements.txt

(Create a local .env file as needed)

Run the app locally:\
python -m uvicorn app.main:app --reload

Open:\
http://127.0.0.1:8000

http://127.0.0.1:8000/docs

## 🐳 Docker Usage

Build and run the service with Docker Compose:\
docker compose up --build

Run in detached mode:\
docker compose up -d

Stop containers:\
docker compose down

## 🧪 Testing

Run the test suite:\
pytest -v

The test suite covers:
- Delivery creation
- Delivery listing
- Sorting behavior
- User registration and login
- Authenticated delivery creation
- Owner update permissions
- Non-owner authorization failure
- Unauthenticated write protection

## ☁️ AWS Deployment

The project has been deployed to AWS using:

- EC2 for the application server
- RDS PostgreSQL for managed database persistence
- IAM role attached to EC2 for future AWS service access without long-lived access keys
- Security groups for controlled network access

#### Current deployment architecture:
Client\
  ↓\
EC2 Instance\
  ↓\
Dockerized FastAPI App\
  ↓\
Amazon RDS PostgreSQL

## 🗺 Roadmap

### Completed:

- FastAPI CRUD API
- SQLite persistence during early development
- PostgreSQL integration
- Docker and Docker Compose
- JWT authentication
- Ownership-based authorization
- Automated tests with pytest
- GitHub Actions CI
- AWS EC2 deployment
- Amazon RDS integration
- EC2 IAM role setup

### Planned:

- S3 integration for delivery report exports or file storage
- Amazon Bedrock integration for delivery note analysis and summarization
- CloudWatch logging and monitoring improvements
- Load balancer and HTTPS support
- ECS deployment path
- More advanced IAM least-privilege policies
- Production-ready secrets management

## 📚 Learning Focus

This repo is part of a structured backend and cloud engineering learning sprint focused on:

- Backend engineering fundamentals
- REST API design
- Secure authentication and authorization
- Relational database modeling
- Cloud-native system design on AWS
- Containerized deployment workflows
- Practical AI service integration

## 🤝 Development Acknowledgement

This project is being developed with the assistance of AI tools, primarily ChatGPT, to support learning, debugging, architecture planning, and implementation guidance.

All implementation decisions, debugging steps, and architectural tradeoffs are actively reviewed and understood as part of the development process.