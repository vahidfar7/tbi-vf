# ML Model Serving with Automated Infrastructure

This project demonstrates a fully automated cloud infrastructure and serving system for deploying and interacting with machine learning models via a FastAPI-based application. It is built to meet the requirements of a technical assessment focused on DevOps and ML system deployment.

## 🚀 Features

- Model deployment via API (`/model`)
- Inference endpoint (`/completion`)
- Live deployment status (`/status`)
- Prometheus-compatible monitoring (`/metrics`)
- Automated infrastructure provisioning with Terraform
- CI/CD with GitHub Actions
- Unit test coverage with `pytest`

---

## 📦 Tech Stack

- **FastAPI** – Web framework for serving ML models  
- **Docker** – Containerisation  
- **Terraform** – Infrastructure as Code (EC2, SGs, IAM)  
- **GitHub Actions** – CI/CD pipeline  
- **AWS** – EC2, ECR, S3, DynamoDB  
- **Prometheus Client** – Monitoring metrics  
- **pytest** – Unit testing

---

## 🗂 Folder Structure

```
.
├── iac/               # Terraform infrastructure definitions
├── serving/           # FastAPI app code
├── tests/             # Unit tests for public API endpoints
├── requirements.txt   # Python dependencies
├── pytest.ini         # PYTHONPATH config for tests
├── .github/workflows/ # GitHub Actions pipeline
└── README.md          # This file
```

---

## 🔧 Pre-requisites

Before deploying this system, ensure you have the following set up in your AWS account:

- ✅ An **empty ECR repository** for storing the Docker image  
- ✅ An **IAM user** with access to:  
  - EC2  
  - ECR  
  - S3  
  - DynamoDB  
- ✅ An **S3 bucket** for storing `terraform.tfstate`  
- ✅ A **DynamoDB table** for Terraform state locking  

You must also add the following secrets to your GitHub repository:

| Secret Key               | Description                             |
|--------------------------|-----------------------------------------|
| `AWS_ACCESS_KEY_ID`      | IAM user's access key                   |
| `AWS_SECRET_ACCESS_KEY`  | IAM user's secret key                   |
| `ECR_REPO`               | Your AWS ECR URI (e.g., `1234.dkr.ecr...`) |

---

## 🛠 Deployment Instructions

### 1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo>
```

### 2. Push to `main` branch:

This triggers GitHub Actions to:
- ✅ Install dependencies  
- ✅ Run unit tests  
- ✅ Build and push Docker image to ECR  
- ✅ Provision infrastructure with Terraform  
- ✅ Deploy and run the FastAPI container on EC2

---

## 🔍 API Endpoints

| Endpoint       | Method | Description                              |
|----------------|--------|------------------------------------------|
| `/model`       | POST   | Deploy a Hugging Face model              |
| `/model`       | GET    | Return currently deployed model ID       |
| `/status`      | GET    | Return deployment status                 |
| `/completion`  | POST   | Perform inference on message input       |
| `/metrics`     | GET    | Expose Prometheus-style request metrics  |

---

## 🧪 Running Tests Locally

Install dependencies and run:

```bash
pip install -r requirements.txt
pytest tests/
```

Test coverage includes:
- Status reporting
- Model deployment
- Completion inference
- Error states when model isn't deployed

---

## 📊 Monitoring

### `/metrics` Endpoint  
Returns Prometheus-formatted counter:

```
ml_requests_total{...} 5
```

Tracks how many times `/completion` has been hit.

---

## 🔐 SSH & Security Notes

- The EC2 instance is reachable via SSH if the security group is manually updated to allow port 22 from your IP.
- In a production environment, **AWS SSM** should be used instead of SSH to manage access without exposing the instance.
- For simplicity and time constraints, SSH was used for this assessment.

---

## ⚠️ Known Limitations / Not Production Ready

- No HTTPS / TLS (no ALB or certificate)  
- EC2 is publicly exposed  
- No auto-scaling or health checks  
- No persistent model state (in-memory only)  
- SSH used instead of SSM  
- No secrets manager integration  

These were deliberately scoped out due to time and complexity constraints, but noted as important next steps for real-world deployments.