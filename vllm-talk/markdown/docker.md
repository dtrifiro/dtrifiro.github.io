## Docker

.

Builds are run as docker images:

```console
$ ls docker
Dockerfile
Dockerfile.cpu
Dockerfile.neuron
Dockerfile.nightly_torch
Dockerfile.ppc64le
Dockerfile.rocm
Dockerfile.rocm_base
Dockerfile.s390x
Dockerfile.tpu
Dockerfile.xpu
```

.

CI builds these images and runs tests:

![buildkite CI](static/buildkite-ci-example.png)

<!-- .element: style="display: block; height: 75vh; width: 100%"-->

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
