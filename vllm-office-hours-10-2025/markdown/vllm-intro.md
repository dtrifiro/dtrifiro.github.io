<!-- .slide: style="font-size: 0.8em" -->

So how does I get started with vLLM?

- Source: [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) <br>

  ```bash
  git clone https://github.com/vllm-project/vllm
  cd vllm
  # let's get to work
  ```

- Docs: [docs.vllm.ai/en/latest](https://docs.vllm.ai/en/latest/) Yes! Docs are useful!
- Issue tracker is a good source of information [vllm-project/vllm/issues](https://github.com/vllm-project/vllm/issues)
- Having access to an accelerator does help 🙂

.

<!-- .slide: class='noautofragment' style="display: block; overflow: auto; font-size: 0.8em" -->

Some vLLM facts

- Current vllm version `v0.11.0` (released Oct 10th), with `v0.11.1` brewing (`rc1` available) <!-- .element: class='fade-out' -->
- One release every three weeks
- 1716 (!) contributors as of today, 207 in the last release (65 new!). This is a 200+ contributor increase from just a couple months ago!
- A **lot** of code is being pushed out each release. For the last release:

  ```console
  $ git diff v0.11.0 v0.10.2 --shortstat
  1162 files changed, 74424 insertions(+), 63294 deletions(-)
  ```

  <!-- .element: style="width: 100%" -->

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->

Lots of code:

![cloc](static/vllm-cloc.png)

 <!-- .element: style="height: 42vh" -->

⚡ That's 374k lines of python and almost 60k lines of C++/CUDA!
