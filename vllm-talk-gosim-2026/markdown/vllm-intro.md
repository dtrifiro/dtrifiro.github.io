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

- Current vllm version `v0.20.0` (released April 27th)
- One release every three weeks
- 2515 (!) contributors as of today, 320 in the last release (123 new!)
- This has almost doubled in the past 6 months!
- A **lot** of code is being pushed out each release. For the last release:

  ```console
  $ git diff v0.19.1 v0.20.0 --shortstat
  1272 files changed, 88277 insertions(+), 27995 deletions(-)
  ```

  <!-- .element: style="width: 100%" -->

.

<!-- .slide: style="margin: 0 3em; width: auto; height: auto; font-size: 0.8em" -->

Lots of code:

![cloc](static/vllm-cloc.png)

 <!-- .element: style="height: 42vh" -->

⚡ That's 667k lines of python and ~66k lines of C++/CUDA!

<!-- .element: style="font-size: 0.9em"-->

.

Reflections

- 😱 python line count was ~330kloc 6 months ago.
- Net +50kloc just in the past release (3 weeks)
- We're not even taking into consideration the ecosystem (dependencies)
