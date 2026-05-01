## Container images

.

The vLLM wheel is built in a `Dockerfile` step.

<div class='fragment'>
There are different dockerfiles for each target:

```console
$ ls docker
Dockerfile
Dockerfile.cpu
Dockerfile.ppc64le
Dockerfile.rocm
Dockerfile.rocm_base
Dockerfile.s390x
Dockerfile.xpu
```

</div>

.

### CUDA Image build

Should be simple enough, right?

```bash
$ wc -l docker/Dockerfile
827 docker/Dockerfile
```

<!-- .element: class="fragment" -->

<img src="static/blob-sweat.png" class="fragment inline-icon" alt=":blob-sweat:">

<div class='fragment'>
We have a guide on how to generate a graph from the dockerfile!
<a href='https://github.com/vllm-project/vllm/blob/main/docs/contributing/dockerfile/dockerfile.md'><pre>docs/contributing/dockerfile/dockerfile.md</pre></a>
</div>

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.7em" -->

**Dependency graph**

![dockerfile-stage-dependency](https://raw.githubusercontent.com/vllm-project/vllm/refs/heads/main/docs/assets/contributing/dockerfile-stages-dependency.png?raw=true)

<!-- .element: style="font-size: .15em" -->

<img src="static/conspiracy-map-guy-meme.jpg" alt="conspiracy-map-guy-meme" class="fragment fade-in-then-out" style="height: 20vh; horizontal-align: center; transform: translateY(-60%);">

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.6em" -->

**Docker stages**

- `base`: toolchain setup (CUDA, nvcc, ...), python build/runtime deps
- `csrc-build`: Builds C++ extensions independently (better caching)
- `extensions-build`: Parallel build of DeepEP kernels
- `build`: Final wheel assembly
- `vllm-base`: installs vLLM wheel
- `vllm-openai*`: final stage for REST API (extra deps)
- `test`: stage used by CI

<!-- .slide: style="font-size: .85em" -->

.

### Build with docker-bake

```bash
cd docker
# Build default target (openai)
docker bake

# Build test target
docker bake test

# Show resolved config
docker bake --print
```

Override build args via env vars:

- `MAX_JOBS`
- `NVCC_THREADS`
- `TORCH_CUDA_ARCH_LIST`

<!-- .element: style="font-size: 0.7em" -->

.

Images are built with [Buildkite CI](https://buildkite.com).<br>Tests are run from the `test` stage

<img src="static/buildkite-ci-example.png" alt='buildkite ci' style="display: block; height: 55vh; width: 100%; object-fit: contain; vertical-align: center">

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->

**CI failing?**

![angry](static/rage-angry.gif)

<!-- .element: style="display: block" -->

- CI can be flaky at times
- Check known failures board: [github.com/orgs/vllm-project/projects/20/views/2](https://github.com/orgs/vllm-project/projects/20/views/2)
- Check vllm CI dashboard: [vllm-ci-dashboard.vercel.app](https://vllm-ci-dashboard.vercel.app)
- Source: [github.com/vllm-project/vllm-dashboard](https://github.com/vllm-project/vllm-dashboard)
- Compare against main or other runs
- Wait for maintainers to re-trigger CI

<!-- .element: style="font-size: 0.7em" -->

.

**vLLM CI Dashboard**

![vLLM CI Dashboard](static/vllm-ci-dashboard.png)

 <!-- .element: style="height: 55vh" -->

- Filter by branch
- Filter by time range
- List known (recurring) failures

<!-- .element: class="blurred-background" style="transform: translateY(-45vh)" -->

.

Also available on buildkite website:

![buildkite CI filter](static/buildkite-ci-filter.png)

<!-- .element: style="display: block; height: 75vh; width: 100%"-->

.

Useful links

- [Known failures board](https://github.com/orgs/vllm-project/projects/20/views/2)
- [https://vllm-ci-dashboard.vercel.app](https://vllm-ci-dashboard.vercel.app)
- [buildkite.com/vllm/fastcheck](https://buildkite.com/vllm/fastcheck)
- [buildkite.com/vllm/ci](https://buildkite.com/vllm/ci)
- [github.com/vllm-project/ci-infra](https://github.com/vllm-project/ci-infra)
- [buildkite.com/docs](https://buildkite.com/docs)

<!-- .element: class="noautofragment" -->

.

Images releases

- [hub.docker.com/r/vllm/vllm-openai](https://hub.docker.com/r/vllm/vllm-openai)
- [hub.docker.com/r/vllm/vllm-openai-rocm](https://hub.docker.com/r/vllm/vllm-openai-rocm)
- [hub.docker.com/r/vllm/vllm-openai-cpu](https://hub.docker.com/r/vllm/vllm-openai-cpu)
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

<!-- .slide: style="font-size: .85em" -->

## Hardware plugins

- Each accelerator has its own docker image
- Check with the plugin's documentation
- The host needs to be configured properly
- On Kubernetes, operators take care of managing device access

.

<!-- .slide: style="font-size: .85em" -->

<i class="fa-brands fa-redhat"></i> Red Hat "midstream" builds

- Images are based on [Red Hat Universal Base Image](https://catalog.redhat.com/en/software/base-images) (UBI)
- Staging area for RHAIIS
- Available on `quay.io` registry:
  - [`quay.io/vllm/vllm-cuda`](https://quay.io/vllm/vllm-cuda)
  - [`quay.io/vllm/vllm-rocm`](https://quay.io/vllm/vllm-rocm)
  - [`quay.io/vllm/vllm-cpu`](https://quay.io/vllm/vllm-cpu)
  - [`quay.io/vllm/vllm-tpu`](https://quay.io/vllm/vllm-tpu)
  - [`quay.io/vllm/vllm-neuron`](https://quay.io/vllm/vllm-neuron)
  - [`quay.io/vllm/vllm-gaudi`](https://quay.io/vllm/vllm-gaudi)

  <!-- .element: class="noautofragment" -->
