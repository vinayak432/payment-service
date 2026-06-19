pipeline {
    agent any
    environment {
        AWS_REGION  = 'ap-south-1'
        ECR_REPO    = '251478238826.dkr.ecr.ap-south-1.amazonaws.com/payment-service'
        IMAGE_TAG   = "${BUILD_NUMBER}"
        GITOPS_REPO = 'github.com/vinayak432/payment-service-gitops.git'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/vinayak432/payment-service.git'
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -q -r requirements.txt
                    pytest tests/ -v --tb=short
                '''
            }
            post {
                failure {
                    echo 'Tests failed — not building the image.'
                }
            }
        }
        stage('Build Image') {
            steps {
                sh '''
                    docker build \
                        -t ${ECR_REPO}:${IMAGE_TAG} \
                        -t ${ECR_REPO}:latest \
                        .
                '''
            }
        }
        stage('Push to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} \
                        | docker login \
                            --username AWS \
                            --password-stdin \
                            ${ECR_REPO}
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                '''
            }
        }
        stage('Update GitOps Repo') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh '''
                        rm -rf /tmp/gitops
                        git clone https://${GIT_USER}:${GIT_PASS}@${GITOPS_REPO} /tmp/gitops
                        cd /tmp/gitops
                        sed -i "s|tag:.*|tag: \"${IMAGE_TAG}\"|" \
                            apps/payment-service/values.yaml
                        git config user.email "jenkins@ci"
                        git config user.name "jenkins"
                        git add apps/payment-service/values.yaml
                        git commit -m "update image tag to ${IMAGE_TAG}"
                        git push origin main
                        rm -rf /tmp/gitops
                    '''
                }
            }
        }
        stage('ArgoCD — Verify Sync') {
            steps {
                withCredentials([string(
                    credentialsId: 'argocd-token',
                    variable: 'ARGOCD_AUTH_TOKEN'
                )]) {
                    sh '''
                        sleep 15
                        argocd app wait payment-service \
                            --server ${ARGOCD_SERVER} \
                            --auth-token ${ARGOCD_AUTH_TOKEN} \
                            --grpc-web \
                            --health \
                            --timeout 120
                    '''
                }
            }
        }
    }
    post {
        success {
            echo "Done. ${ECR_REPO}:${IMAGE_TAG} is live."
        }
        failure {
            echo "Pipeline failed — check the stage logs above."
        }
        always {
            sh 'docker image prune -f || true'
            cleanWs()
        }
    }
}
