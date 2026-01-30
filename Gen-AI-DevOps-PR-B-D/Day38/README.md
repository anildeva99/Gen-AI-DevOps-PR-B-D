<<<<<<< HEAD
# AI-Powered DevOps CI/CD Demo

## Overview
This project demonstrates end-to-end AI-powered DevOps CI/CD:
- **GitHub** → Source Code
- **Jenkins** → CI/CD Automation
- **Docker** → Containerization
- **Minikube / Kubernetes** → Deployment

## Folder Structure
app/          # Flask app + Dockerfile
k8s/          # Kubernetes manifests
Jenkinsfile   # Jenkins pipeline
ai_generate_pipeline.py # AI script to auto-generate files

## Steps
1. Run `python3 ai_generate_pipeline.py` to generate all files
2. Start Minikube on your EC2
3. Run Jenkins and configure pipeline pointing to this repo
4. Build & deploy using Jenkins
5. Access app: http://<EC2-Public-IP>:30080
=======
# PRReview
>>>>>>> f089c29 (Initial commit)
Day38 pipeline setup - updated
Update: Wed Nov 19 07:43:21 AM UTC 2025
# Test update to trigger pipeline
trigger build Wed Nov 19 07:55:38 AM UTC 2025
Pipeline test run Wed Nov 19 08:13:04 AM UTC 2025
PR Trigger Test - Wed Nov 19 09:47:40 AM UTC 2025
