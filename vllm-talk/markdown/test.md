## Testing

- Unit tests: "just" run `pytest`
- Example:

  ```console
  $ pytest --collect-only
  ...
  === 49059 tests collected, 60 errors in 96.82s ===
  ```

  <!-- .element: style="width: 100%; display: block;"-->

  ![nani](static/nani.gif)
    <!-- .element: class='fragment' style="display: block; margin: 0 auto; text-align: center" -->

- good luck 😉

.

### Tips

- Buildkite ([buildkite.com](https://buildkite.com)) is used for CI, check the definition to see which tests are run and how:

  ```yaml
  # .buildkite/test-pipeline.yaml
  - label: Basic Models Test # 24min
    mirror_hardwares: [amdexperimental]
    torch_nightly: true
    source_file_dependencies:
      - vllm/
      - tests/models
    commands:
      - pytest -v -s models/test_transformers.py
      - pytest -v -s models/test_registry.py
      - pytest -v -s models/test_utils.py
      - pytest -v -s models/test_vision.py
      - pytest -v -s models/test_initialization.py
  ```

  <!-- .element: style="width: 100%; display: block;"-->

- Use pytest `-k` to select tests by name/pattern
  ```bash
  pytest -k <pattern> [tests/path/to/name.py]
  ```

.

#### More tips

(shameless plug)

Use [dtrifiro/pytest-fzf](https://github.com/dtrifiro/pytest-fzf)<sup>1</sup> to select tests using `fzf`<sup>2</sup>

![pytest-fzf](static/pytest-fzf.png)
<!-- .element: style="height: 7em; margin: 0 auto;" -->

1. https://github.com/dtrifiro/pytest-fzf
2. https://github.com/junegunn/fzf

.

### what else?

- Functional tests
- Benchmarks (we strive to be fast after all!)

.

#### Evaluations

How can we make sure that `vllm` behaves as expected on a given model?

- [`EleutherAI/lm-evaluation-harness`](https://github.com/EleutherAI/lm-evaluation-harness/)
- Evaluate a given model on a task (or set of tasks)
  - 568 tasks groups
  - 10k+ tasks

.

Example: the famous OpenLLM Leaderboard

```yaml
group: openllm
group_alias: Open LLM Leaderboard
task:
  - task: arc_challenge
    fewshot_split: train
    num_fewshot: 25
  - task: hellaswag
    fewshot_split: train
    num_fewshot: 10
  - task: truthfulqa
    num_fewshot: 0
  - task: mmlu
    num_fewshot: 5
  - task: winogrande
    fewshot_split: train
    num_fewshot: 5
  - task: gsm8k
    num_fewshot: 5
```

<!-- .element: style="font-size: 0.4em"-->

.

<!-- .slide: style="font-size: 0.7em"-->

**Options:**

- Use vllm backend
- Spin up vllm manually and use `local-completions`:

  ```json
  // model_args.json
  {
    "model": "RedHatAI/Llama-3.3-70B-Instruct-FP8-dynamic",
    // Assuming vllm is running locally on port 8000
    "base_url": "http://localhost:8000/v1/completions",
    "num_concurrent": 1,
    "max_retries": 3,
    "tokenized_requests": false,
    "batch_size": 16
  }
  ```

  <!-- .element: style="display: block; font-size: 0.4em"-->

  ```bash
  lm-eval \
      --model local-completions \
      --tasks mmlu \
      --model_args "$(< model_args.json )" # read model args from file
  ```

  <!-- .element: style="display: block; font-size: 0.4em"-->

- In both cases: wait (a long time)
- Compare results to the Model Card (HuggingFace, ...)

.

#### Performance

[github.com/vllm-project/guidellm](https://github.com/vllm-project/guidellm)

```text
A platform for evaluating and optimizing the deployment of large language models.
By simulating real-world inference workloads, GuideLLM enables users to assess the
performance, resource requirements, and cost implications of deploying LLMs on various
hardware configurations.
This approach ensures efficient, scalable, and cost-effective LLM inference serving while
maintaining high service quality.
```

<!-- .element: style="display: block; font-size: 0.4em; width: 100%"-->

.

**Quick Start**

```bash [|1-2|4-7|9-15|12]
# start vllm server
vllm serve meta-llama/Llama-3.1-8B-Instruct

# then, in another session
uv venv .venv
source .venv/bin/activate
uv pip install guidellm

# start the benchmark
guidellm benchmark \
  --target=http://localhost:8000 \
  --rate-type=throughput \ # customize for different benchmark types
  --max-requests=50 \
  --output-path=guidellm_results.json \
  --data='{"prompt_tokens":100, "output_tokens":500}'
```

<!-- .element: style="display: block; font-size: 0.4em; width: 100%"-->

.

Useful flags:

```markdown
- --data: Specifies the dataset to use (synthetic data can be generated)
- --max-seconds:  Sets the maximum duration (in seconds) for each benchmark run.
- --rate-type: Defines the type of benchmark to run (default sweep).
   Supported types include:
     synchronous, throughput, concurrent, constant, poisson, sweep
```

<!-- .element: style="display: block; font-size: 0.4em; width: 100%"-->

More details at <br>[vllm-project/guidellm#configurations](https://github.com/vllm-project/guidellm#configurations)

<!-- .element: class="fragment" data-fragment-index=1 -->

.

## guidellm demo

<!-- <section> --> <!-- unreliable -->
<!--   <script src="https://asciinema.org/a/X2AgmbfQtiA0LgVz7rPh89rSd.js" id="asciicast-X2AgmbfQtiA0LgVz7rPh89rSd" async="true"></script> -->
<!-- </section> -->

<!-- no asciinema.org alternative -->

<!-- ![guidellm](static/guidellm.svg) --> 
<!-- better quality, starts halfway through -->

![guidellm gif](static/guidellm.gif)
<!-- faster than svg, lower quality
<!-- <img src=static/guidellm.svg> -->
