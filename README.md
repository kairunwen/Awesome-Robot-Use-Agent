<div align="center">

<img src="assets/logo.png" alt="RUA logo: a robotic hand gently petting a happy cat" width="160" />

# Awesome Robot Use Agent (RUA)

[![Awesome](https://img.shields.io/badge/Awesome-List-111111.svg?style=for-the-badge&labelColor=000000&logo=awesomelists&logoColor=white)](https://awesome.re) [![Resources: 24](https://img.shields.io/badge/Resources-24-111111.svg?style=for-the-badge&labelColor=000000&logo=readthedocs&logoColor=white)](#at-a-glance) [![PRs welcome](https://img.shields.io/badge/PRs-Welcome-111111.svg?style=for-the-badge&labelColor=000000&logo=git&logoColor=white)](#contributing) [![GitHub Stars](https://img.shields.io/github/stars/kairunwen/Awesome-Robot-Use-Agent?style=for-the-badge&label=Stars&labelColor=000000&color=111111&logo=github&logoColor=white)](https://github.com/kairunwen/Awesome-Robot-Use-Agent/stargazers)

[Start here](#start-here) · [Blogs](#blogs-and-perspectives) · [Demos](#videos-and-demonstrations) · [Papers](#research-papers) · [Projects](#robot-interfaces-and-tool-frameworks) · [Evaluation](#agent-benchmarks-and-evaluation-frameworks) · [Models](#supporting-models-and-learning-infrastructure)

</div>

> A **robot-use agent** is an AI system that can **reason** about tasks, **plan** sequences of actions, and **act** in the physical world through robot skills, generated code, and perception/control APIs. It combines observations with execution feedback to track progress, revise plans, and recover from failures while pursuing a user-specified goal.

A curated collection of research papers, blogs, demos, projects, frameworks, and tools for **robot-use agents**, with selected models and datasets as supporting foundations.

## Contents

<details open>
<summary><strong>Browse by topic</strong></summary>

- [At a glance](#at-a-glance)
- [What is a robot-use agent?](#what-is-a-robot-use-agent)
- [Start here](#start-here)
- [Blogs and perspectives](#blogs-and-perspectives)
- [Videos and demonstrations](#videos-and-demonstrations)
- [Research papers](#research-papers)
  - [Planning and code as policies](#planning-and-code-as-policies)
  - [Execution feedback and recovery](#execution-feedback-and-recovery)
  - [Embodied harnesses and policy orchestration](#embodied-harnesses-and-policy-orchestration)
- [Robot interfaces and tool frameworks](#robot-interfaces-and-tool-frameworks)
- [Agent benchmarks and evaluation frameworks](#agent-benchmarks-and-evaluation-frameworks)
- [Simulation environments and task suites](#simulation-environments-and-task-suites)
- [Supporting models and learning infrastructure](#supporting-models-and-learning-infrastructure)
  - [Closed-source multimodal model families](#closed-source-multimodal-model-families)
  - [Supporting policies and learning infrastructure](#supporting-policies-and-learning-infrastructure)
- [How to compare systems](#how-to-compare-systems)
- [Contributing](#contributing)
- [License](#license)

</details>

## At a glance

| Collection | Entries | What you will find |
| --- | --- | --- |
| [Research papers](#research-papers) | 10 | Skill selection, embodied code, feedback, recovery, and policy orchestration |
| [Robot interfaces](#robot-interfaces-and-tool-frameworks) | 2 | Agent-facing ROS tools and MCP connectivity |
| [Agent evaluation](#agent-benchmarks-and-evaluation-frameworks) | 3 | Benchmarks and frameworks for assessing agent decisions and execution |
| [Environments and task suites](#simulation-environments-and-task-suites) | 3 | Manipulation and household tasks, with associated data |
| [Supporting models and infrastructure](#supporting-models-and-learning-infrastructure) | 6 | Three API model families plus three policy/learning resources |

**Reading the links:** `Paper` describes a method; `Project` may contain only descriptions and demos; `Code` points to implementation resources; `Docs` describes a platform interface. Code, weights, data, and full reproduction are separate release claims. “Unverified release” means this list has not confirmed the relevant artifact, not that it does not exist.

## What is a robot-use agent?

For this list, a **robot-use agent** is a system that turns a goal into robot actions by selecting skills, generating executable programs, or calling perception and control tools. Its interaction with the environment may include observation, execution feedback, replanning, and recovery. This is a working definition for curation, not a standardized field taxonomy.

| Layer | Main question | Typical interface |
| --- | --- | --- |
| Agent | What should happen next? | Goals, plans, tool calls, generated programs |
| Harness | How is execution organized and evaluated? | Context, memory, skill routing, outcome checks, recovery |
| Policy / controller | How is a physical action performed? | Learned policies, motion planning, control primitives |
| Environment / evaluation | What happened, and did the task succeed? | Observations, state changes, task predicates, rollout logs |

An LLM may use a robot as a tool; a robot may also use a physical tool such as a hammer. This list focuses on the former system boundary. A VLA can supply an agent's action capability, but a VLA checkpoint alone does not specify the surrounding agent workflow. Similarly, an MCP bridge exposes capabilities without necessarily providing planning or recovery.

The categories below are editorial groupings. Placement does not imply that every work implements the entire loop or has been independently reproduced.

## Start here

| If you want to understand… | Read / inspect |
| --- | --- |
| The robot-as-a-tool perspective | [Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) |
| Language grounded in available robot skills | [SayCan](https://say-can.github.io/) |
| Robot behavior expressed as generated code | [Code as Policies](https://code-as-policies.github.io/) |
| Replanning from execution feedback | [Inner Monologue](https://innermonologue.github.io/) |
| Coding agents evaluated on manipulation | [CaP-X](https://github.com/capgym/cap-x) |
| A tool-based embodied harness | [Thea](https://github.com/EIT-HAI/Thea) |
| Runtime critics and recovery around a frozen policy | [Zetta](https://github.com/air-embodied-brain/Zetta-Embodiment) |
| Connecting an agent to ROS | [ROSA](https://github.com/nasa-jpl/rosa) / [ROS MCP Server](https://github.com/robotmcp/ros-mcp-server) |

## Blogs and perspectives

- **[Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html)** — Phillip Isola · 2026-09-07 · **Perspective**. General-purpose AI agents using robots through sensor and actuator APIs, with discussion of deployment, latency, and reliability.
- **[Robots That Write Their Own Code](https://research.google/blog/robots-that-write-their-own-code/)** — Jacky Liang and Andy Zeng, Google Research · 2022-11-02 · **Technical blog**. An introduction to Code as Policies: composing robot APIs, generating functions, and expressing feedback loops, with examples and limitations.

## Videos and demonstrations

- **[Code as Policies — experiment videos and generated code](https://code-as-policies.github.io/)** — Compare natural-language commands, generated programs, and robot behavior across tabletop manipulation, drawing, and mobile-robot tasks.
- **[Inner Monologue — video walkthrough and failure-recovery demos](https://innermonologue.github.io/)** — See how scene descriptions, success feedback, and human interventions affect replanning.
- **[VoxPoser — video and interactive value maps](https://voxposer.github.io/)** — Explore how language instructions become spatial constraints and robot trajectories, including execution under disturbances.

These are author-provided demonstrations; consult the linked papers for evaluation protocols and aggregate results. Blog and demo links supplement the research entries and are not counted again in the overview.

## Research papers

Grouped by agent mechanism, with the newest first arXiv release in each group listed first. Paper and code links are separated for quick access; project pages sit below the full titles. Star badges show repository totals, including the full monorepo for Code as Policies and SayCan. `Unverified` means implementation availability has not been confirmed. Method summaries reflect the authors' descriptions; this list does not claim independent reproduction.

### Planning and code as policies

<details open>
<summary>Browse 4 papers</summary>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-03 | **CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation** | [Paper](https://arxiv.org/abs/2603.22435) | [Code](https://github.com/capgym/cap-x) <br> [![GitHub stars](https://img.shields.io/github/stars/capgym/cap-x?style=flat-square&label=stars)](https://github.com/capgym/cap-x) | Studies embodied coding agents through CaP-Gym, CaP-Bench, CaP-Agent0, and CaP-RL, including execution feedback and skill synthesis. |
| 2023-07 | **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models** <br> [Project](https://voxposer.github.io/) | [Paper](https://arxiv.org/abs/2307.05973) | [Code](https://github.com/huangwl18/VoxPoser) <br> [![GitHub stars](https://img.shields.io/github/stars/huangwl18/VoxPoser?style=flat-square&label=stars)](https://github.com/huangwl18/VoxPoser) | Uses generated code and visual grounding to construct 3D value maps for motion planning; the generated program can be reevaluated with visual feedback. |
| 2022-09 | **Code as Policies: Language Model Programs for Embodied Control** <br> [Project](https://code-as-policies.github.io/) | [Paper](https://arxiv.org/abs/2209.07753) | [Code](https://github.com/google-research/google-research/tree/master/code_as_policies) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Generates programs that compose perception outputs, control APIs, and feedback loops. |
| 2022-04 | **SayCan — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances** <br> [Project](https://say-can.github.io/) | [Paper](https://arxiv.org/abs/2204.01691) | [Code: tabletop simulation](https://github.com/google-research/google-research/tree/master/saycan) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Combines language-model skill scoring with affordance/value estimates to select feasible robot behaviors. |

</details>

### Execution feedback and recovery

<details open>
<summary>Browse 2 papers</summary>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2023-06 | **REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction** <br> [Project](https://robot-reflect.github.io/) | [Paper](https://arxiv.org/abs/2306.15724) | [Code](https://github.com/real-stanford/reflect) <br> [![GitHub stars](https://img.shields.io/github/stars/real-stanford/reflect?style=flat-square&label=stars)](https://github.com/real-stanford/reflect) | Summarizes multisensory execution history, explains failures, and conditions a planner on those explanations to produce corrective actions. |
| 2022-07 | **Inner Monologue: Embodied Reasoning through Planning with Language Models** <br> [Project and demos](https://innermonologue.github.io/) | [Paper](https://arxiv.org/abs/2207.05608) | Unverified | Feeds success detection, scene descriptions, and human feedback into language-based planning; demonstrates replanning and responses to changed goals. |

</details>

### Embodied harnesses and policy orchestration

<details open>
<summary>Browse 4 papers</summary>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-08 | **Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence** <br> [Project](https://air-embodied-brain.github.io/zetta/) | [Paper](https://arxiv.org/abs/2608.16590) | [Code](https://github.com/air-embodied-brain/Zetta-Embodiment) <br> [![GitHub stars](https://img.shields.io/github/stars/air-embodied-brain/Zetta-Embodiment?style=flat-square&label=stars)](https://github.com/air-embodied-brain/Zetta-Embodiment) | Keeps the base policy frozen while developing runtime critics and recovery skills through execution, diagnosis, and gated updates. The separate `air-embodied-brain/zetta` repository hosts the project website. |
| 2026-08 | **Thea — Towards the Harness of Embodied Agents** <br> [Project](https://eit-hai.github.io/thea/) | [Paper](https://arxiv.org/abs/2608.11246) | [Code](https://github.com/EIT-HAI/Thea) <br> [![GitHub stars](https://img.shields.io/github/stars/EIT-HAI/Thea?style=flat-square&label=stars)](https://github.com/EIT-HAI/Thea) | Wraps robot capabilities as callable tools, maintains symbolic scene context, and evaluates action termination, success, and failure causes. Public runtime and interfaces; robot/simulator deployment requires concrete adapters and capabilities. |
| 2026-07 | **RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning** | [Paper](https://arxiv.org/abs/2607.18060) | Unverified | Uses execution memory to route among heterogeneous policies and a Memory Bridge to improve handoffs between policies. |
| 2026-06 | **Guava: An Effective and Universal Harness for Embodied Manipulation** | [Paper](https://arxiv.org/abs/2606.18363) | Unverified | Studies iterative perception–reasoning–action, semantic action abstractions, and multimodal observations; also describes distillation into a smaller agent model. Checkpoint availability also unverified. |

</details>

[Back to top](#awesome-robot-use-agent-rua)

## Robot interfaces and tool frameworks

| Resource | Role | Scope / boundary | Official source |
| --- | --- | --- | --- |
| **ROSA — Robot Operating System Agent** | Natural-language agent for ROS systems | Supports inspection, diagnosis, and robot operation through tools; custom robots need appropriate tools and context. | [Code and documentation](https://github.com/nasa-jpl/rosa) · [Paper](https://arxiv.org/abs/2410.06472) |
| **ROS MCP Server** | MCP interface to ROS | Exposes robot communication and introspection through ROS/rosbridge. Planning and outcome evaluation depend on the connected agent and robot stack. | [Code and documentation](https://github.com/robotmcp/ros-mcp-server) |

## Agent benchmarks and evaluation frameworks

| Resource | What it evaluates / provides | Reading note | Official source |
| --- | --- | --- | --- |
| **Embodied Agent Interface (EAI)** | Goal interpretation, subgoal decomposition, action sequencing, and transition modeling | Useful for identifying decision-making errors; symbolic module evaluation should be distinguished from end-to-end physical execution. | [Code and documentation](https://github.com/embodied-agent-interface/embodied-agent-interface) |
| **EmbodiedBench** | Vision-driven embodied agents across high- and low-level tasks | Provides multiple environments and capability-oriented evaluation, including navigation and manipulation. | [Code and documentation](https://github.com/EmbodiedBench/EmbodiedBench) |
| **Inspect Robots** | Evaluation framework connecting policies, embodiments, benchmarks, and logs | Supports compatible LLM-agent and VLA integrations; currently described by its maintainers as alpha software. | [Code and documentation](https://github.com/robocurve/inspect-robots) |

[CaP-X](https://github.com/capgym/cap-x), listed under planning and code as policies, also provides CaP-Bench for comparing embodied coding agents at different interface abstraction and interaction levels.

## Simulation environments and task suites

These provide tasks and execution environments for agent research. An environment's inclusion does not mean its standard protocol evaluates tool use, streaming interaction, interruption, or recovery.

| Resource | Useful for | Official source |
| --- | --- | --- |
| **LIBERO** | Manipulation tasks and demonstrations for studying transfer across spatial, object, goal, and task variations | [Code and datasets](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **RoboCasa / RoboCasa365** | Kitchen manipulation, atomic and composite tasks, and demonstration data | [Project, code, and datasets](https://robocasa.ai/) |
| **BEHAVIOR-1K / OmniGibson** | Long-horizon household activities and rich object interactions | [Project and documentation](https://behavior.stanford.edu/) |

[Back to top](#awesome-robot-use-agent-rua)

## Supporting models and learning infrastructure

These are building blocks for an agent: perception/reasoning models, robot policies, and learning tools. Their inclusion does not establish an end-to-end robot-use capability.

### Closed-source multimodal model families

Selected API model families with documented visual input and tool-calling interfaces. The suggested roles below are integration possibilities, not a robot-performance ranking. Capabilities vary by model version; record the exact model ID and access date in experiments.

| Family / provider | Documented interfaces | Possible role in a robot-use agent | Official sources |
| --- | --- | --- | --- |
| **GPT / OpenAI** | Image input and function calling on supported models | Interpret camera observations and propose calls to explicitly exposed robot skills | [Vision](https://developers.openai.com/api/docs/guides/images-vision) · [Tool calling](https://developers.openai.com/api/docs/guides/function-calling) |
| **Claude / Anthropic** | Image input and tool use | Reason over visual observations and execution reports; request perception or action tools | [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) · [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) |
| **Gemini / Google** | Image understanding and function calling | Interpret scene observations and select structured calls through a robot adapter | [Vision](https://ai.google.dev/gemini-api/docs/image-understanding) · [Tool calling](https://ai.google.dev/gemini-api/docs/function-calling) |

The application implements the tools, executes actions, and returns observations. A model-generated tool call is a request, not confirmation that the physical task succeeded.

### Supporting policies and learning infrastructure

These resources can supply action models, data workflows, or deployment components. They are listed as foundations rather than complete robot-use agents.

| Resource | Role | Official source |
| --- | --- | --- |
| **OpenVLA** | Vision-language-action model and tools for adaptation to robot manipulation | [Code and model links](https://github.com/openvla/openvla) |
| **openpi** | Physical Intelligence's robot-policy implementations, training utilities, and inference interfaces | [Code and model links](https://github.com/Physical-Intelligence/openpi) |
| **LeRobot** | Robot learning library with policies, datasets, hardware integrations, and training workflows | [Code and documentation](https://github.com/huggingface/lerobot) |

## How to compare systems

<details>
<summary><strong>Comparison checklist: observations, actions, feedback, timing, and evidence</strong></summary>

Use the following questions when reading a paper or adding a resource. These are curation dimensions, not claims that every listed system supports them.

| Dimension | Record |
| --- | --- |
| Observation | RGB, depth, proprioception, symbolic state, history; whether privileged simulator state is exposed |
| Action interface | Skill names, generated code, poses, policy calls, or joint-level commands |
| Feedback | Whether completion and success are measured, inferred, or manually supplied |
| Recovery | Retry, replan, ask for help, switch policies, or execute a learned/generated correction |
| Memory and adaptation | What persists between steps or episodes; whether prompts, skills, or model weights change |
| Timing | Whether the world advances during inference; how new instructions, cancellation, and stale actions are handled |
| Evidence | Simulation vs. hardware; number of trials, success criteria, human intervention, latency, and compute budget |
| Release | Paper, project page, implementation, weights, data, and reproduction instructions, checked separately |

Closed-loop feedback alone does not establish continuous streaming interaction. A simulator alone does not establish that world time advances during model inference. Compare systems under matched observation access, action interfaces, task conditions, and budgets before comparing success rates.

</details>


## Contributing

Suggestions and corrections are welcome through an issue or pull request.

- Add a primary source: the authors' paper, project page, repository, or official documentation.
- Explain the resource's connection to robot-use agents in one sentence and place it in the closest existing category.
- For papers, include the full title, first-release month (`YYYY-MM`), and verified official links. Describe the mechanism rather than repeating promotional claims.
- Check what is actually released. Label website-only repositories, partial releases, and unverified code availability explicitly.
- Cite the original work separately from third-party implementations. Social posts and demonstrations need an original source and clearly stated evidence scope.
- Keep general VLA, world-model, and dataset additions selective: explain their direct role as an agent component or evaluation resource.
- Preserve the distinction between a proposed method, an author-reported result, and an independently reproduced result.

Suggested paper row:

```markdown
| YYYY-MM | **Full paper title** <br> [Project](URL) | [Paper](URL) | [Code](URL) or Unverified | One-sentence mechanism; state release limits |
```

For a project or model family, include its interface, intended role, official repository/docs, and current availability. Count each resource once in the overview; cross-links do not add to the total.

Keep paper rows newest-first within a category. Use a focused commit message such as `docs: add <work>` or `docs: update <section>`, following `type: description`.

## License

This collection is distributed under the [MIT License](LICENSE). Linked papers, code, models, and datasets retain their respective licenses.

[Back to top](#awesome-robot-use-agent-rua)
