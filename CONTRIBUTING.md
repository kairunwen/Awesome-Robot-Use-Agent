# Contributing to Awesome Robot Use Agent

Help make robot-use agents easier to discover, understand, and build. New resources, corrections, broken-link reports, and clearer descriptions are welcome.

## Suggest a resource

Open an [issue](https://github.com/kairunwen/Awesome-Robot-Use-Agent/issues) with the resource name, a primary-source link, and one sentence explaining its relevance. A suggested category is helpful but optional. You do not need to edit the README or run code to make a suggestion.

For a pull request, edit [README.md](README.md), follow the nearest entry's format, and keep the change focused. Check for an existing entry before adding a new one; update or cross-link it when appropriate.

## What belongs here

The collection focuses on agents that turn goals into robot actions through skills, generated code, or perception and control APIs, then use observations and execution feedback to track progress and recover from failures.

We welcome:

- Research, implementations, and demonstrations of robot-use agents, including planning, tool use, execution, verification, and recovery.
- Environments and benchmarks that let agents interact with robots or evaluate their behavior.
- Tools that directly provide robot capabilities or make agent integration, execution, and feedback easier.
- Selected policies, datasets, and surveys with a clear role in building or evaluating these systems.

A resource does not need a paper or a minimum number of GitHub stars. Explain what it contributes and support the description with evidence.

Keep supporting resources selective. Robot-specific tools such as cuRobo and Pink fit; general dependencies such as PyTorch, Open3D, and Trimesh are not standalone entries. A package appearing in an agent's requirements file is not sufficient evidence of relevance. Likewise, include a VLA, world model, or dataset only when its connection to robot use is explicit.

## Choose a category

| Section | What to add |
| --- | --- |
| **Articles** | Introductions, technical blogs, and perspectives on robot-use agents. |
| **Papers** | Research references under Surveys, Methods & Frameworks, Datasets, Benchmarks, or Related Agent Self-Improvement. Clearly label non-robot methodological references in the latter. Keep a paper and its code links together. |
| **Projects → Systems & Frameworks** | Agent runtimes and systems that connect reasoning to robot execution and feedback. |
| **Projects → Environment & Sandbox** | Simulators, task environments, and scene-reconstruction workflows that supply a setting for robot interaction. |
| **Projects → Tool Box** | Reusable perception, grasping, planning, control, execution, and learning tools. Use **Other Tools** for interfaces, evaluation utilities, and data workflows that do not fit the more specific subsections. |
| **Projects → Social Demos** | Original demonstrations, grouped as Real-robot, Simulation, or Perception and reconstruction. |
| **Benchmarks** | Evaluation protocols, task suites, and benchmark implementations, with their environment and scoring scope. |

Classify a resource by its main function, not every capability it exposes. Do not add a second implementation-only row merely because a paper releases code. A separate benchmark or demo entry should add useful information; cross-link related entries. Multiple views of one work are not independent works.

## Write an informative entry

Use English, the official resource name, and a concise description of what it does. Prefer concrete capabilities over promotional claims.

- **Sources:** Link to the authors' paper, repository, project page, documentation, or original post. Label third-party implementations separately.
- **Availability:** Distinguish released code, model weights, datasets, and a project website. State when an implementation is partial or its availability is unverified.
- **Integration:** For tools and systems, identify the interface and material setup requirements, such as robot adapters, calibration, model access, or hardware. Claim an integration only when documentation or a code path supports it.
- **Evidence:** Distinguish real robots, simulation, perception-only demonstrations, and mock environments. Attribute results to their authors unless independently reproduced. Keep success rate, task progress, retries, and selected demo clips distinct.
- **Dates:** Use `YYYY-MM` for papers, based on the first arXiv release unless another basis is stated. Keep papers newest-first within each subsection. Use `YYYY-MM-DD` for demos, following the README's UTC+8 convention.

Copy a row from the target subsection so its columns remain compatible with the website. Keep the main description short; use the existing `<details class="entry-notes">` pattern for setup, release status, and limitations. Systems & Frameworks and Other Tools use **Feedback / workflow**, **Setup**, and **Limits** inside these notes.

The Getting started comparison summarizes existing entries and is not counted as additional resources; update its claims when the linked evidence changes.

For Social Demos, merge posts about the same demonstration unless they add distinct evidence. Link the underlying project where available. Use an original or official HTTPS preview with meaningful alt text and a source link; keep a text link if no suitable preview exists. Do not substitute an unrelated image.

Label direct implementation links `Code` or `Project / code`. The website's **Code linked** filter recognizes GitHub links containing `code` in the label; do not apply that label to a website-only repository or an unrelated framework.

## Check a pull request

The website is generated from README.md. Edit the source rather than `website/dist/`, and preserve existing anchors and collapsible groups.

For resource additions, removals, or moves:

- Update the relevant badges: **Resources** counts catalogue entries, **Demo** counts Social Demos, and **Tools** counts all Tool Box entries, including Other Tools.
- Update category counts or structure expectations in `website/test_build.py` when the intended catalogue changes. Investigate unexpected failures rather than weakening checks.
- Inspect the rendered README and website for table layout, working anchors, and readable notes. See [website preview instructions](website/README.md).

From the repository root, using the virtual environment described in those instructions:

```sh
website/.venv/bin/python -m unittest discover -s website -p 'test_*.py'
git diff --check
```

The test command also rebuilds the website. Check changed external destinations with:

```sh
website/.venv/bin/python website/check_links.py --url 'https://github.com/OWNER/REPO'
```

Repeat `--url` for additional links. Review failures: login requirements, rate limits, and bot protection do not necessarily mean a source is dead. Small wording-only changes need a rendered read-back and whitespace check; they do not require a full external-link scan.

In the PR description, explain what changed, why it belongs, and what you checked. Use commit messages in `type: description` form without a scope, for example `docs: add Pink to tool box` or `docs: clarify benchmark scoring`.

Thank you for helping keep the collection useful and accurate.
