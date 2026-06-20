# payment-service

A Flask REST API used as the application target for a GitOps CI/CD pipeline project. The focus of this repo is the pipeline and DevOps tooling, not the application itself.

## What this repo contains

- Flask REST API with health, readiness, and payments endpoints
- pytest test suite (4 tests)
- Multi-stage Dockerfile using Gunicorn (135MB image, non-root user)
- Jenkinsfile implementing a 4-stage CI pipeline

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Liveness probe |
| GET | /ready | Readiness probe |
| GET | /metrics | Prometheus metrics |
| POST | /api/v1/payments | Create a payment |
| GET | /api/v1/payments/:id | Get payment by ID |

## CI pipeline (Jenkins)

Every push to main triggers:

1. **Run tests** — pytest, fails fast if tests break
2. **Build image** — multi-stage Docker build tagged with build number
3. **Push to ECR** — authenticates with short-lived ECR token
4. **Update GitOps repo** — bumps image tag in values.yaml

Jenkins never runs kubectl. Deployment is handled by ArgoCD watching the GitOps repo.

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run tests
pytest tests/ -v

# run app
python run.py
```

## Related repos

- [payment-service-gitops](https://github.com/vinayak432/payment-service-gitops) — Helm chart and deployment config
- [terraform-eks-setup](https://github.com/vinayak432/terraform-eks-setup-) — EKS cluster infrastructurei
