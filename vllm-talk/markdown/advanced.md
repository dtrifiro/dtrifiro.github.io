## Advanced stuff

.


**Profiling**

```bash
export VLLM_TORCH_PROFILER_DIR=/path/to/profiling/output

# start the server
vllm serve meta-llama/Llama-3.1-8B-Instruct
```

.


```bash [|1-3|4-5|6-14|15-18]
host="localhost:8000"
max_tokens=150
model=meta-llama/Llama-3.1-8B-Instruct
# enable profiling
curl -X POST "$host/start_profile" -d ""
# Do a request
curl "$host/v1/chat/completions" \
    -H "Content-Type: application/json" -d '{
    "model": "'$model'",
    "messages": [
        {"role": "user", "content": "Write a 5000 word story"}
    ],
    "max_tokens": '$max_tokens',
    "temperature": 0}'
# stop profiling
curl -X POST "$host/stop_profile" -d ""
# wait for profile dump to have been written
# result is saved to `$VLLM_TORCH_PROFILER_DIR`
```

<!-- .element: style="height: 120%; display: block; font-size: .4em"-->

This generates `.json.gz` traces, one for each process. Traces are large! stop profiling immediately

<!-- .element: style="font-size: .4em"-->

.

Traces can be visualized using [ui.perfetto.dev](https://ui.perfetto.dev) or `viztracer`:

```bash
uv pip install viztracer
vizviewer /path/to/trace.json.gz
```

A VS Code extension is also available.

.

![profiling-perfetto](static/profiling-perfetto.png)

<br>

For more information: [docs.vllm.ai/en/stable/contributing/profiling.html](https://docs.vllm.ai/en/stable/contributing/profiling.html)

.

Customizing vllm behaviour

![envs.py](static/vllm-envs.png)

<!-- .element: style="height: 12em" -->

`vllm/envs.py`

<!-- .element: style="font-size: 0.5em" -->

.

<!-- .slide: style="font-size: 0.75em" -->
- Any model supported by huggingface's `transformers`<br> is supported:

  ```bash
  vllm serve llava-hf/llava-oneviision-qwen2-0.5b-ov-hf \
      --model_impl transformers
  ```

  [blog.vllm.ai/2025/04/11/transformers-backend.html](https://blog.vllm.ai/2025/04/11/transformers-backend.html)

- `torch` cpp extensions [docs.pytorch.org/tutorials/advanced/cpp_extension.html](https://docs.pytorch.org/tutorials/advanced/cpp_extension.html)
- `torch` custom ops [docs.pytorch.org/tutorials/advanced/cpp_custom_ops.html#cpp-custom-ops-tutorial](https://docs.pytorch.org/tutorials/advanced/cpp_custom_ops.html#cpp-custom-ops-tutorial)
