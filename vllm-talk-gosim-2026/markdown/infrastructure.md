# Infrastructure

.

- buildkite runners on AWS/GCP
- tests are read from a template file and sharded across runners
- [github.com/vllm-project/ci-infra](https://github.com/vllm-project/ci-infra )

.

## Actions Runner Controller (ARC)

[github.com/actions/actions-runner-controller](https://github.com/actions/actions-runner-controller)

1. Deploy on k8s
2. Define runner deployments
3. Run github actions workflows
