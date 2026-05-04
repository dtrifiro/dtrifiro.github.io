<!-- .slide: style="font-size: 0.8em" -->

<img src="static/vllm-logo-text-dark.png" style="height: 2em; display: inline-icon; margin-bottom: 0" alt="vLLM"></img>

- vLLM is a fast library for LLM inference and serving.
- Latest features and optimizations
- Supports a Wide range models
- Supports a wide Wide range of hardware configurations

.

![de facto inference platform](static/vllm_defacto_open_genai_inference_platform.jpg) <!-- .element: style="display: block" -->

.

## Base Idea: Paged Attention

Efficient Memory Management for Large Language Model Serving with PagedAttention (2023) [arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180) <!-- .element: style="font-size: .8em" -->

![PagedAttention paper](static/arxiv-pagedattention.png)

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->
<aside class="notes"> problem: KV cache is large and dynamic: varies on context length </aside?>
.

Partition KV Cache into blocks

![paged attention animation](https://vllm.ai/blog-assets/figures/annimation0.gif) <!-- .element: width="70%" -->

https://vllm.ai/blog/vllm

.

**Improved memory management:** <br>Better throughput, longer sequences, larger batches

![paged attention request flow](https://vllm.ai/blog-assets/figures/annimation1.gif) <!-- .element: width="70%" -->

https://vllm.ai/blog/vllm

.

<!-- .slide: style="display: block; overflow: auto; font-size: 0.5em" -->

## Optimizations

- Continuous batching of incoming requests, chunked prefill
- Prefix caching
- Speculative decoding (2x to 5x decoding throughput)
- Fast and flexible model execution with piecewise and full CUDA/HIP graphs
- Quantization: `FP8`, `MXFP8`/`MXFP4`, `NVFP4`, `INT8`, `INT4`, `GPTQ`/`AWQ`, `GGUF`, compressed-tensors, ModelOpt, TorchAO, and more
- Optimized attention kernels including FlashAttention, FlashInfer, TRTLLM-GEN, FlashMLA, and Triton
- Optimized GEMM/MoE kernels for various precisions using CUTLASS, TRTLLM-GEN, CuTeDSL
- Speculative decoding including n-gram, suffix, EAGLE, ...
- Automatic kernel generation and graph-level transformations using torch.compile
- Disaggregated prefill, decode, and encode

<!-- .element: class="noautofragment" -->

😵‍💫 <!--.element: class="fragment" style="font-size: 2.5em"-->

**Most optimizations are enabled by default** <!--.element: class="fragment" style="font-size=1em"-->

.

**Quick Start**

- Install it, just run:

  ```bash
   uv pip install --torch-backend=auto vllm
  ```

- Only if you're using CUDA (?)
- Only if you're not building a container image
- Relies on `uv`'s automatic backend selection [docs.astral.sh/uv/guides/integration/pytorch/#automatic-backend-selection](https://docs.astral.sh/uv/guides/integration/pytorch/#automatic-backend-selection)
- CUDA, some ROCm versions, Intel GPUs

<!--.element: class="nofragment" style="font-size=.2em"-->

.

**Quick Start**

```bash
# it's easy
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

.

<!-- .slide: class='noautofragment' style="display: block; overflow: auto; font-size: 0.65em" -->

**Quick Start, pt. 2**

```bash
# It also can look like this
docker run --gpus all \
    --ipc=host -p 8000:8000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    vllm/vllm-openai:deepseekv4-cu130 deepseek-ai/DeepSeek-V4-Pro \
    --trust-remote-code \
    --kv-cache-dtype fp8 \
    --block-size 256 \
    --enable-expert-parallel \
    --data-parallel-size 8 \
    --compilation-config '{"cudagraph_mode":"FULL_AND_PIECEWISE", "custom_ops":["all"]}' \
    --attention_config.use_fp4_indexer_cache=True \
    --tokenizer-mode deepseek_v4 \
    --tool-call-parser deepseek_v4 \
    --enable-auto-tool-choice \
    --reasoning-parser deepseek_v4
```

- Just 1.6T parameters
- 8xB200 or 8xB300

.

800GBs (weights-only)

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->

![old man yells at ram](static/old-man-yells-at-ram.png)

.

- Having access to an accelerator(s) does help 🙂 <!-- .element: class="noautofragment" -->
- Also works on CPU, recent optimizations [<i class="fa-brands fa-github"></i> #35446](https://github.com/vllm-project/vllm/pull/35466) improved performance/build process for AVX512
- Basic Metal (M-series Macs) support recently added [github.com/vllm-project/vllm-metal](https://github.com/vllm-project/vllm-metal)

.

**Some vLLM facts**

- Current vLLM version <s>`v0.20.0`</s> `v0.20.1`
- Released <s>April 27th</s> yesterday
- One release every roughly three weeks
- 2515 (!) contributors as of today, 320 in the last release (123 new!)
- This has almost doubled in the past 6 months!
- A **lot** of code is being pushed out each release.

  ```console
  $ git diff v0.19.1 v0.20.0 --shortstat
  1272 files changed, 88277 insertions(+), 27995 deletions(-)
  ```

  <!-- .element: style="width: 100%" -->

<!-- .element: style="font-size: 0.7em" -->

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->

**Lots** of code:

![cloc](static/vllm-cloc.png)

 <!-- .element: style="height: 70vh" -->

⚡ That's 677k lines of python and ~66k lines of C++/CUDA!

<!-- .element: style="font-size: 0.9em"-->

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->

Considerations

- 😱 line count was ~300k 1 year ago.

  ![kloc over time](static/cloc_lines_of_code_historical.png) <!-- .element: style="display: block; font-size: 0.5em" -->

.

Considerations

- Net +50kloc just in the past release (3 weeks)
- We're not even taking into consideration the ecosystem (dependencies) <!-- .element: class="fragment" -->

<!-- .element: class="noautofragment" -->

.

So how do I get started with vLLM?

- Source: [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) <br>

  ```bash
  git clone https://github.com/vllm-project/vllm
  cd vllm
  # let's get to work
  ```

- Docs: [docs.vllm.ai/en/latest](https://docs.vllm.ai/en/latest/) Yes! Docs are useful!
- Issue tracker is a good source of information [vllm-project/vllm/issues](https://github.com/vllm-project/vllm/issues)
