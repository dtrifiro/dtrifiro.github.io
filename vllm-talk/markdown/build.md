# building

.

Here's how easy it is to build vLLM using `uv`<sup>1</sup>

```bash [|1-2|4-7|9-10]
git clone https://github.com/vllm-project/vllm
cd vllm

uv venv .venv
source .venv/bin/activate
# let's pretend PEP517 doesn't exist
uv pip install -r requirements/build.txt

export VLLM_TARGET_DEVICE=cuda
python setup.py bdist_wheel
```

Or is it?

<!-- .element: class="fragment" -->
<br>

1. [github.com/astral-sh/uv](https://github.com/astral-sh/uv)

.

What's not simple?

- There are several available targets: Nvidia CUDA, AMD ROCm, Google TPU, Intel HPU, CPU, ...
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

Find a working example of a C extension here: [github.com/dtrifiro/python-c-extension-example](https://github.com/dtrifiro/python-c-extension-example)

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
  # or tpu, cpu, xpu, ...
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
2. Same thing from `torch`: [github.com/pytorch/pytorch/blob/v2.7.1/torch/utils/
   cpp_extension.py#L2326-L2341](https://github.com/pytorch/pytorch/blob/v2.7.1/torch/utils/cpp_extension.py#L2326-L2341)
3. ROCm arches [rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html](https://rocm.docs.amd.com/en/latest/reference/gpu-arch-specs.html)

<!-- .element: style="width: 80%; display: block;"-->

.

## Configuring the build, pt. 2

- Many targets have their own `torch` flavour: ROCm, CPU, Google TPU (XLA), Intel XPU, Amazon Neuron, ...
- Install the correct version **before** building: set the index to point to the appropriate torch version

  ```bash
  export \
    PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

  # or with uv
  export \
    UV_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu \
    UV_INDEX_STRATEGY="unsafe-best-match" # 😅
  ```

  <!-- .element: style="width: 100%; display: block;"-->

.

## Local development

```bash [7,14-15|7-10,14-15|7-12,14-15|1-8,14-15]
# Sometimes you can get by building the CPU target
export \
    VLLM_TARGET_DEVICE=cpu \
    UV_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu \
    UV_INDEX_STRATEGY=unsafe-best-match

uv pip install -r requirements/build.txt # has to match VLLM_TARGET_DEVICE

# only editing python?
export VLLM_USE_PRECOMPILED=1
# use latest nightly binaries
export VLLM_TEST_USE_PRECOMPILED_NIGHTLY_WHEEL=1

# build and install in editable mode
uv pip install --no-build-isolation -e .
```

<!-- .element: style="width: 100%; height: 100%; display: block; font-size: .40em"-->

.

## Speeding up builds

Use a compiler cache!

- `ccache` ([ccache/ccache](https://github.com/ccache/ccache))
- `sccache` ([mozilla/ccache](https://github.com/mozilla/sccache)) can use remote storage, S3, GCP Buckets, Alibaba OSS and more
- `vllm`'s build system will use them by default if they are installed!

.

More suggestions:

- Build for the targets you need:

  ```bash
  # only build for Nvidia A100
  export TORCH_CUDA_ARCH_LIST="8.0"
  # OR only build for AMD MI300X
  export PYTORCH_ROCM_ARCH="gfx942"
  ```
- Sometimes building the CPU version might be enough for simple local testing
  ```bash
  export VLLM_TARGET_DEVICE='cpu'
  ```

.

## Hardware accelerator plugins

[blog.vllm.ai/2025/05/12/hardware-plugin.html](https://blog.vllm.ai/2025/05/12/hardware-plugin.html)

- [RFC] vLLM Plugin System <!--: This RFC introduces a plugin-based approach to support various customization requirements, allowing users to define custom models, executors, schedulers, etc.-->
- [RFC] Make vLLM Device-Agnostic for Diverse Hardware Support ([vllm-project/vllm#6080](https://github.com/vllm-project/vllm/pull/6080)) <!-- This RFC introduces the platform submodule, which centralizes hardware-related implementations to reduce conditional logic in the main codebase and lays the foundation for modularization.-->
- TLDR: New hardware support can be implemented via an out-of-tree plugin that registers with `vllm`

<!-- .element: class="noautofragment" -->


.

### Examples

<!-- .slide: style="font-size: 0.8em" -->

How these are actually implemented varies, some are extensions, some rely on custom torch flavours.

1. IBM: [github.com/vllm-project/vllm-spyre](https://github.com/vllm-project/vllm-spyre)
2. Intel: [github.com/vllm-project/vllm-gaudi](https://github.com/vllm-project/vllm-gaudi)
3. Huawei: [github.com/vllm-project/vllm-ascend](https://github.com/vllm-project/vllm-ascend)
4. Rebellions (KR): [github.com/rebellions-sw/vllm-rbln](https://github.com/rebellions-sw/vllm-rbln)
5. MetaX (CN): [github.com/MetaX-MACA/vLLM-metax](https://github.com/MetaX-MACA/vLLM-metax)


.

```python
from vllm.platform import Platform, PlaftormEnum


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



## What I did not cover

vllm has dependencies which are built in a similar way, and need to be built similarly

1. [github.com/dao-AILab/flash-attention/](https://github.com/dao-AILab/flash-attention/)
2. [github.com/flashinfer-ai/flashinfer](https://github.com/flashinfer-ai/flashinfer)
3. [github.com/deepseek-ai/FlashMLA](https://github.com/deepseek-ai/FlashMLA)
4. [github.com/facebookresearch/xformers](https://github.com/facebookresearch/xformers)

.

A few tips

- `torch` version has to match
- `CUDA` version has to match
- Not all architectures/devices support all features
