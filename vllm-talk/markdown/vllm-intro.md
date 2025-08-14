<!-- .slide: style="font-size: 0.8em" -->

So how does I get started with vLLM?

- [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) <br> ![vllm-project/vllm](static/qr-vllm-project.png) <!-- .element: style="display: block; height: 5em; margin: 0 auto;" -->
  ```bash
  git clone https://github.com/vllm-project/vllm
  cd vllm
  # let's get to work
  ```
- [docs.vllm.ai/en/latest](https://docs.vllm.ai/en/latest/) Yes! Docs are useful!
- Issue tracker is a good source of information [vllm-project/vllm/issues](https://github.com/vllm-project/vllm/issues)
- Having access to an accelerator does help 🙂

.

<!-- .slide: style="display: block; overflow: auto" -->

Some vLLM facts

- Current vllm version `v0.10.0` (released Jul 25th)
- One release every three weeks
- 1410 (!) contributors as of today, 168 in the last release (62 new!)
- A **lot** of code is being pushed out each release. For the last release:

  ```console
  $ git diff v0.10.0 v0.9.2 --shortstat
  888 files changed, 40965 insertions(+), 54955 deletions(-)
  ```

  <!-- .element: style="width: 100%" -->

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto;" -->

Lots of code:

![cloc](static/vllm-cloc.png)

⚡ That's 334k lines of python and almost 60k lines of C++/CUDA!
