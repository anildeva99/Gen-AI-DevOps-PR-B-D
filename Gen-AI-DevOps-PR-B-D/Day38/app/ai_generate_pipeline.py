import os

# Create project directories
os.makedirs("app", exist_ok=True)
os.makedirs("k8s", exist_ok=True)

# -----------------------------
# Jenkinsfile
# -----------------------------
jenkinsfile_content = """pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "genai-devops-app:latest"
        DOCKER_REGISTRY = "docker.io/your_dockerhub_username"
        K8S_DEPLOYMENT = "app-deployment"
        K8S_SERVICE = "app-service"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'git@github.com:adinarayanap/Gen-AI-DevOps.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE, './app')
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                            docker.image(DOCKER_IMAGE).push()
                        }
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/service.yaml'
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }
    }
}
"""

with open("Jenkinsfile", "w") as f:
    f.write(jenkinsfile_content)

# -----------------------------
# app/app.py
# -----------------------------
app_py_content = """from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from AI-powered DevOps CI/CD!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""

with open("app/app.py", "w") as f:
    f.write(app_py_content)

# -----------------------------
# app/requirements.txt
# -----------------------------
requirements_content = """flask==2.3.3
"""

with open("app/requirements.txt", "w") as f:
    f.write(requirements_content)

# -----------------------------
# app/Dockerfile
# -----------------------------
dockerfile_content = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
"""

with open("app/Dockerfile", "w") as f:
    f.write(dockerfile_content)

# -----------------------------
# k8s/deployment.yaml
# -----------------------------
deployment_yaml_content = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: devops-ai
  template:
    metadata:
      labels:
        app: devops-ai
    spec:
      containers:
      - name: devops-ai
        image: genai-devops-app:latest
        ports:
        - containerPort: 5000
"""

with open("k8s/deployment.yaml", "w") as f:
    f.write(deployment_yaml_content)

# -----------------------------
# k8s/service.yaml
# -----------------------------
service_yaml_content = """apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: devops-ai
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: NodePort
"""

with open("k8s/service.yaml", "w") as f:
    f.write(service_yaml_content)

print("✅ All files generated successfully! Ready for CI/CD demo.")

