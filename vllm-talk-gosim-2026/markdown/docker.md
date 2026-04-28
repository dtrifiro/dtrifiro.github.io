## Docker

.

The vLLM wheel is built in a `Dockerfile` step.

<div class='fragment'>
There are different dockerfiles for each target:

```console
$ ls docker
Dockerfile
Dockerfile.cpu
Dockerfile.nightly_torch
Dockerfile.ppc64le
Dockerfile.rocm
Dockerfile.rocm_base
Dockerfile.s390x
Dockerfile.tpu
Dockerfile.xpu
```

</div>

.

### CUDA Image build

Should be simple enough, right?

```bash
$ wc -l docker/Dockerfile
543 docker/Dockerfile
```

<img src="static/blob-sweat.png" class="fragment inline-icon" alt=":blob-sweat:">

<div class='fragment'>
We have a guide on how to generate a graph from the dockerfile!
<a href='https://github.com/vllm-project/vllm/blob/main/docs/contributing/dockerfile/dockerfile.md'><pre>docs/contributing/dockerfile/dockerfile.md</pre></a>
</div>

.

Dependency graph
![dockerfile-stage-dependency-v0.11.0](https://raw.githubusercontent.com/vllm-project/vllm/refs/heads/main/docs/assets/contributing/dockerfile-stages-dependency.png?raw=true)

<img src="static/conspiracy-map-guy-meme.jpg" alt="conspiracy-map-guy-meme" class="fragment fade-in-then-out" style="height: 20vh; horizontal-align: center">

.

Dependency graph
![dockerfile-stage-dependency-v0.11.0](https://raw.githubusercontent.com/vllm-project/vllm/refs/heads/main/docs/assets/contributing/dockerfile-stages-dependency.png?raw=true)

- `base`: toolchain setup (CUDA, nvcc, ...), python build/runtime deps
- `build`: vLLM wheel build
- `vllm-base`: installs vLLM wheel
- `vllm-openai*`: final stage for REST API (extra deps)
- `test`: stage used by CI
<!-- .slide: style="font-size: .85em" -->

.

Images are built with [Buildkite CI](https://buildkite.com). Tests are run from the `test` stage

<img src="static/buildkite-ci-example.png" alt='buildkite ci' style="display: block; height: 55vh; width: 100%; object-fit: contain; vertical-align: center">

.

CI failing?

![angry](static/rage-angry.gif)

<!-- .element: style="display: block"-->

- CI can be flaky at times
- Compare against main or other runs
- Wait for maintainers to re-trigger CI

.

Filter by branch

![buildkite CI filter](static/buildkite-ci-filter.png)

<!-- .element: style="display: block; height: 75vh; width: 100%"-->

.

Useful links

- [buildkite.com/vllm/fastcheck](https://buildkite.com/vllm/fastcheck)
- [buildkite.com/vllm/ci](https://buildkite.com/vllm/ci)
- [github.com/vllm-project/ci-infra](https://github.com/vllm-project/ci-infra)
- [buildkite.com/docs](https://buildkite.com/docs)

<!-- .element: class="noautofragment" -->

.

Images releases

- [hub.docker.com/r/vllm/vllm-openai](https://hub.docker.com/r/vllm/vllm-openai)
- [hub.docker.com/r/rocm/vllm](https://hub.docker.com/r/rocm/vllm)
- [hub.docker.com/r/vllm/vllm-tpu](https://hub.docker.com/r/vllm/vllm-tpu)
- some nightlies are also available on DockerHub

.

Nightlies available on the public CI ECR (`main` branch):

```bash [1-4|6-8]
git checkout main
ref=$(git rev-parse HEAD)
docker pull \
    public.ecr.aws/q9t5s3a7/vllm-ci-postmerge-repo:$ref

# list available tags
skopeo inspect \
    docker://public.ecr.aws/q9t5s3a7/vllm-ci-postmerge-repo
```

<!-- .slide: style="font-size: .85em" -->

.

<i class="fa-brands fa-redhat"></i> Red Hat "midstream" builds

- Images are based on [Red Hat Universal Base Image](https://catalog.redhat.com/en/software/base-images) (UBI)
- Staging area for RHAIIS
- Available on `quay.io` registry:
  - [`quay.io/vllm/vllm-cuda`](https://quay.io/vllm/vllm-cuda)
  - [`quay.io/vllm/vllm-rocm`](https://quay.io/vllm/vllm-rocm)
  - Coming up: `quay.io/vllm/vllm-tpu`

  <!-- .element: class="noautofragment" -->
