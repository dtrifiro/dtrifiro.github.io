## Contributing

.

Always:

- Signoff commits with `git commit --signoff` since Developer Certificate of Origin signoff is a required check
- Run `pre-commit`: [pre-commit/pre-commit](https://github.com/pre-commit/pre-commit) is used to enforce coding standards (formatting, linting)

.

**pre-commit**

```bash
pip install pre-commit
# enable the pre-commit hook
pre-commit install
# run pre commit checks on all files
pre-commit run --all-files
# only run on a subset of commits
pre-commit run --from-ref=HEAD~10 --to-ref=HEAD # last 10 commits
# skip pre--commit hooks
git commit --no-verify # don't do this 🙂
```

<!-- .element: style="width: 100%; display: block;"-->

❗ All checks must pass for a PR to be merged

<!-- .element: style="width: 100%; display: block;"-->

.

## Contributing, pt 2

Always:

- Write tests (unit/integration)
- Add documentation to `docs/`
- Keep changes small/incremental when possible

.

**PR Title and Classification**

```markdown
- [Bugfix] for bug fixes.
- [CI/Build] for build or continuous integration improvements.
- [Doc] for documentation fixes and improvements.
- [Model] for adding a new model or improving an existing model.
  Model name should appear in the title.
- [Frontend] For changes on the vLLM frontend.
  (e.g., OpenAI API server, LLM class, etc.)
- [Kernel] for changes affecting CUDA kernels or other compute kernels.
- [Core] for changes in the core vLLM logic
  (e.g., LLMEngine, AsyncLLMEngine, Scheduler, etc.)
- [Hardware][Vendor] for hardware-specific changes.
  Vendor name should appear in the prefix (e.g., [Hardware][AMD]).
- [Misc] for PRs that do not fit the above categories.
  Please use this sparingly.
```

<!-- .element: style="width: 100%; display: block; font-size: .4em"-->

See [docs.vllm.ai/en/latest/contributing/index.html#pull-requests-code-reviews](https://docs.vllm.ai/en/latest/contributing/index.html#pull-requests-code-reviews)

.


Search for "good first issue" labeled issues

![good first issue](static/vllm-good-first-issue.png)

<!-- .element: style="height: 65vh; width: auto" -->

.

Join slack: [slack.vllm.ai](https://slack.vllm.ai):

![img](static/vllm-slack.png)

.

Useful channels:

```markdown
- #questions
- #documentation
- #contributors
- #pr-reviews
```

Check out Special Interest Groups channels:

```markdown
- #sig-*
```
