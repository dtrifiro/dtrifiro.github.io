# building

.

<!-- .slide: class='noautofragment' style="display: block; overflow: auto; font-size: 0.82em" -->

Here's how easy it is to build vLLM using `uv`

```bash [|1-2|4-7|9-10|11-12]
git clone https://github.com/vllm-project/vllm
cd vllm

uv venv .venv
source .venv/bin/activate
# Install platform-specific build requirements
uv pip install -r requirements/build/cuda.txt # or cpu.txt/rocm.txt

export VLLM_TARGET_DEVICE=cuda
uv build --no-build-isolation .
# install
uv pip install dist/vllm-0.20.0-cp312-cp312-linux_x86_64.whl
```

<!-- .element: class="fragment" -->

Or is it?

<!-- .element: class="fragment" -->
<br>

.

What's not simple?

- Multiple targets: Nvidia CUDA, AMD ROCm, CPU, TPU
- Multiple architectures
- Out of tree plugins support
- Different toolchains required, depending on target
- Hardware requirements
- Build can be very hungry for memory and CPU (several GBs of memory required per process)

.

But what is vllm?

A Python module with an `Extension`

```python [|7-9]
# very simplified `setup.py`
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

setup(
    name="vllm",
    ext_modules=[
      Extension("vllm", ["vllm.cpp", "vllm.cu"])
    ],
    cmdclass={"build_ext": build_ext}
    ...
)
```

<!-- .element: class="fragment" -->

Find a (basic) working example of a C extension here: [github.com/dtrifiro/python-c-extension-example](https://github.com/dtrifiro/python-c-extension-example)

<!-- .element: class="fragment" -->

.

vLLM extensions

- Built on top of `torch` [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- Custom extensions using `cmake`/`ninja`
  - CUDA: `nvcc`
  - ROCm: `hipify_torch` ([rocm/hipify_torch](https://github.com/ROCm/hipify_torch)) + `hipcc`
  - other targets: it depends

.

## Configuring the build

.

A few env vars:

- Target (accelerator) device:

  ```bash
  export VLLM_TARGET_DEVICE="cuda"
  # or
  export VLLM_TARGET_DEVICE="rocm"
  # or cpu, tpu, xpu, ...
  ```

<!-- .element: style="width: 100%; display: block;"-->

- ❗ `MAX_JOBS`: CUDA ~4GB/job, ROCm ~1GB/job
- `NVCC_THREADS=2` used when building for multiple architectures (cuda only)
- Target architectures
  ```bash
  # CUDA (device capabilities)
  export TORCH_CUDA_ARCH_LIST="7.5 8.0 ..." # T4, A100, ...
  # ROCm (arches)
  export PYTORCH_ROCM_ARCH="gfx90a;gfx942" # MI210X/MI300X
  ```
  using more architectures increases compile time.

<!-- .element: style="width: 100%; display: block; font-size: .7em"-->

.

### Useful references

1. Nvidia GPU/capability mapping: [developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus)
2. Same mapping in `torch`: [github.com/pytorch/pytorch/blob/v2.11.0/torch/utils/
   cpp_extension.py#L2552-L2579](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/utils/cpp_extension.py#L2552-L2579)
3. ROCm arches [rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html](https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html)

<!-- .element: style="width: 80%; display: block;"-->

.

<!-- .slide: style="font-size: 0.8em" -->

## Configuring the build, pt. 2

- Many targets have their own `torch` flavour: ROCm, CPU, Intel XPU, Intel Habana Gaudi, ...
- Install the correct version **before** building: set the pip index to point to the appropriate torch version

  ```bash
  # for cpu
  export \
    PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

  # or with uv
  export UV_TORCH_BACKEND=cpu # or `cu129`, `rocm7.1`, `xpu` etc
  ```

  <!-- .element: style="width: 100%; display: block;"-->

.

## Local development

```bash [6,12,13|1-4,7,12-13|6,9-13]
# Sometimes you can get by building the CPU target
export \
    VLLM_TARGET_DEVICE=cpu \
    UV_TORCH_BACKEND=cpu

uv pip install -r requirements/build/cuda.txt # ! has to match VLLM_TARGET_DEVICE
uv pip install -r requirements/build/cpu.txt # has to match VLLM_TARGET_DEVICE

# only editing python?
export VLLM_USE_PRECOMPILED=1

# build and install in editable mode
uv pip install --no-build-isolation -e .
```

<!-- .element: style="width: 100%; height: 100%; display: block; font-size: .40em"-->

`VLLM_USE_PRECOMPILED=1` downloads and installs the correct version depending on the checked out version

<!-- .element: class="fragment" style="font-size: 0.7em" -->

.

Installing nightly builds:

```bash
uv pip install --upgrade \
    --pre \
    --extra-index-url https://wheels.vllm.ai/nightly \
    --index-strategy unsafe-best-match \
    vllm
```

.

More useful information: [docs.vllm.ai/en/latest/getting_started/quickstart.html](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)

.

## Speeding up builds

Use a compiler cache!

- `ccache` ([ccache/ccache](https://github.com/ccache/ccache))
- `sccache` ([mozilla/sccache](https://github.com/mozilla/sccache)) can use remote storage, S3, GCP Buckets, Alibaba OSS and more
- `vllm`'s build system will use them by default if they are installed!

.

Caveats:

- `pip` build isolation uses temporary build dirs which might cause cache misses ([vllm-project/vllm#27345](https://github.com/vllm-project/vllm/pull/27345))

  ```bash
  python setup.py bdist_wheel
  python setup.py develop
  ```

.

More suggestions:

- Build for the targets you need:

  ```bash
  # only build for Nvidia B200
  export TORCH_CUDA_ARCH_LIST="10.0"
  # OR only build for AMD MI300X
  export PYTORCH_ROCM_ARCH="gfx942"
  ```

- Sometimes building the CPU version might be enough for simple local testing

  ```bash
  export VLLM_TARGET_DEVICE='cpu'
  ```

.

To install a specific git ref

```bash [1-5|4|5]
export VLLM_TARGET_DEVICE=cpu
uv pip install \
    --torch-backend=cpu \
    --no-binary=vllm \
    git+https://github.com/vllm-project/vllm@v0.20.0
```

This is especially useful with hardware plugins<br>(more later) <!-- .element: class="fragment" -->

.

vLLM supports multiple hardware platforms:

- **Nvidia CUDA** (from Tesla to Blackwell + DGX Spark)
- **AMD ROCm** (MI200X, MI300X, MI355X, `gfx90a`-`gfx942`-`gfx950`)
- **CPU**: x86_64, ARM64, ppc64le, s390x (IBM Z), riscv64
- **Intel Habana Gaudi 3** & **XPU** (Intel GPUs)
- **Google TPU** (via JAX)
- **AWS Neuron** (Inferentia, Trainium)
- **IBM Spyre**
- **Apple M-Series** - Metal (new)
- ... <!-- .element: class="fragment" -->

<!-- .slide: class="noautofragment" style="font-size: 0.8em" -->

.

<!-- .slide: style="font-size: .7em" -->

## Hardware accelerator plugins

[blog.vllm.ai/2025/05/12/hardware-plugin.html](https://blog.vllm.ai/2025/05/12/hardware-plugin.html)

- vLLM Plugin System enables out-of-tree hardware support
- New hardware support can be implemented via a plugin that registers with `vllm`
- Device-agnostic design through platform abstraction

<!-- .element: class="noautofragment" -->

.

### Current plugin implementations

<!-- .slide: style="font-size: 0.8em" -->

1. <i class="fa-brands fa-aws"></i> AWS Neuron [github.com/vllm-project/vllm-neuron](https://github.com/vllm-project/vllm-neuron)
1. <img src="static/ibm.ico" class="inline-icon invert-image" alt="IBM logo"> IBM Spyre: [github.com/vllm-project/vllm-spyre](https://github.com/vllm-project/vllm-spyre)
1. <i class="fa-brands fa-google"></i> Google TPU [github.com/vllm-project/tpu-inference](https://github.com/vllm-project/tpu-inference)
1. <img src="static/intel.ico" class="inline-icon" alt="Intel logo"> Intel Gaudi: [github.com/vllm-project/vllm-gaudi](https://github.com/vllm-project/vllm-gaudi)
1. <img src="static/apple.ico" class="inline-icon" alt="Apple Logo"> Apple Metal: [github.com/vllm-project/vllm-metal](https://github.com/vllm-project/vllm-metal)
1. <img src="static/rebellions.png" class="inline-icon" alt="Rebellions logo"> Rebellions: [github.com/rebellions-sw/vllm-rbln](https://github.com/rebellions-sw/vllm-rbln)
1. <img src="static/metax.ico" class="inline-icon" alt="MetaX logo"> MetaX: [github.com/MetaX-MACA/vLLM-metax](https://github.com/MetaX-MACA/vLLM-metax)
1. <img src="static/huawei.ico" class="inline-icon" alt="Huawei logo"> Huawei Ascend: [github.com/vllm-project/vllm-ascend](https://github.com/vllm-project/vllm-ascend)

.

```python
from vllm.platform import Platform, PlatformEnum


class MyPlatform(Platform):
    _enum = PlatformEnum.OOT
    device_name = "my device name"
    device_type = "cpu"

    ...
    # implement all the relevant methods
```

```python
# setup.py

setup(
    name="vllm_plugin_example",
    ...,
    entry_points={
        "vllm.platform_plugins": ["plugin_example = vllm_plugin_example:register"],
        "vllm.general_plugins": ["plugin_example = vllm_plugin:register_model"],
    },
)
```

<!-- .element: style="width: 100%; height: 100%; display: block; font-size: .40em"-->

.

More details [docs.vllm.ai/en/latest/design/plugin_system.html](https://docs.vllm.ai/en/latest/design/plugin_system.html)

.

<!-- .slide: style="font-size: 0.8em" -->

Generally, plugins require:

- `vllm`, built with `VLLM_TARGET_DEVICE=cpu` or `empty`
- `vllm-<plugin>`, often installed from GitHub
- Device SDK and custom `torch` version/dependencies
  <br>(alternate pip index)

<!-- .element: style="display: block" -->

.

Installing plugins:

```bash [1-7|4|5|6-7]
export VLLM_TARGET_DEVICE=empty
uv pip install \
   --torch-backend=cpu \
   --no-binary=vllm \
   --extra-index-url=<...> \
   vllm==<...> \
   git+https://github.com/vllm-project/vllm-<plugin>@<...>
```

<!-- .element: style="font-size: .5em" -->

Check with each plugin's documentation <!-- .element: class="fragment" -->

.

## What I did not cover

<!-- .slide: style="font-size: 0.8em" -->

vLLM has dependencies which also are python extensions linking against `torch`:

- [github.com/dao-AILab/flash-attention/](https://github.com/dao-AILab/flash-attention/)
- [github.com/flashinfer-ai/flashinfer](https://github.com/flashinfer-ai/flashinfer)
- [github.com/deepseek-ai/FlashMLA](https://github.com/deepseek-ai/FlashMLA)

<!-- .element: class="noautofragment" -->

Some dependencies heavily rely on Just-in-Time (JIT) compilation, such as [deepseek-ai/DeepGEMM](https://github.com/deepseek-ai/DeepGEMM), requiring compilers and development headers to be available

<!-- .element: class="fragment" data-fragment-index=5 -->

.

A few tips

- `torch` version has to match
- `CUDA` version has to match
- Not all architectures/devices support all models/features, check compatibility matrix
