# Infrastructure

.

- buildkite runners on AWS/GCP
- tests are read from a template file and sharded across runners
- [github.com/vllm-project/ci-infra](https://github.com/vllm-project/ci-infra )


.

## Buildkite

- [github.com/buildkite/agent-stack-k8s](https://github.com/buildkite/agent-stack-k8s)

.

**How to onboard runners onto CI cluster on Buildkite**

The machines communicate with Buildkite server via an agent being installed on the machine. There are multiple ways agents can be installed, depending on how the machines are set up:
1. [Buildkite Elastic CI stack](https://buildkite.com/docs/agent/v3/elastic-ci-aws/elastic-ci-stack-overview) if you want the compute to be autoscaling EC2 instances.
2. [Buildkite K8s agent stack](https://github.com/buildkite/agent-stack-k8s) if you want machines to be managed/orchestrated in a Kubernetes cluster.
3. [Buildkite agent](https://buildkite.com/docs/agent/v3) if you already have existing standalone machines.

.

For all of these approaches, you would need the following info to set up (please contact @khluu on #sig-ci channel - vllm-dev.slack.com to get them):
- Buildkite agent token
- Buildkite queue name
- (optional) Buildkite cluster UUID

.

## Actions Runner Controller (ARC)

[github.com/actions/actions-runner-controller](https://github.com/actions/actions-runner-controller)

1. Deploy on k8s
2. Define runner deployments
3. Run github actions workflows
