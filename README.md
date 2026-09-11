<div align="center">

<img src="assets/logo.png" alt="RUA logo: a robotic hand gently petting a happy cat" width="160" />

# Awesome Robot Use Agent (RUA)

[![Awesome](https://img.shields.io/badge/Awesome-List-111111.svg?style=for-the-badge&labelColor=000000&logo=awesomelists&logoColor=white)](https://awesome.re) [![Resources: 39](https://img.shields.io/badge/Resources-39-111111.svg?style=for-the-badge&labelColor=000000&logo=readthedocs&logoColor=white)](#at-a-glance) [![PRs welcome](https://img.shields.io/badge/PRs-Welcome-111111.svg?style=for-the-badge&labelColor=000000&logo=git&logoColor=white)](#contributing) [![GitHub Stars](https://img.shields.io/github/stars/kairunwen/Awesome-Robot-Use-Agent?style=for-the-badge&label=Stars&labelColor=000000&color=111111&logo=github&logoColor=white)](https://github.com/kairunwen/Awesome-Robot-Use-Agent/stargazers)

[Getting started](#getting-started) · [Agents & frameworks](#agents-and-frameworks) · [Evaluation](#benchmarks-and-environments) · [Supporting components](#supporting-components) · [Blogs & demos](#blogs-and-demos)

</div>

> A **robot-use agent** is an AI system that can **reason** about tasks, **plan** sequences of actions, and **act** in the physical world through robot skills, generated code, and perception/control APIs. It combines observations with execution feedback to track progress, revise plans, and recover from failures while pursuing a user-specified goal.

A practical guide and evidence index for **agents that use robots as tools**: how they connect to a robot, call its capabilities, and respond to execution feedback. Papers, code, models, and demos are collected together for each system; supporting models and datasets remain selective.

## Contents

<details open>
<summary><strong>Browse by topic</strong></summary>

1. [Getting started](#getting-started) — scope, entry points, and evidence checklist
2. [Agents and frameworks](#agents-and-frameworks)
   - **Connect and run:** [Robot interfaces](#robot-interfaces-and-tools) · [Agent runtimes](#agent-runtimes-and-orchestration)
   - **Plan and adapt:** [Harnesses](#embodied-harnesses-and-policy-orchestration) · [Planning and code](#planning-and-code-as-policies) · [Feedback and recovery](#execution-feedback-and-recovery)
3. [Benchmarks and environments](#benchmarks-and-environments) — [Agent evaluation](#agent-benchmarks-and-evaluation-frameworks) · [Simulation tasks](#simulation-environments-and-task-suites)
4. [Supporting components](#supporting-components) — [Perception & spatial understanding](#perception-and-spatial-understanding) · [Motion planning & control](#motion-planning-and-control) · [Execution infrastructure](#execution-infrastructure) · [Multimodal models](#closed-source-multimodal-model-families) · [Policies and learning](#supporting-policies-and-learning-infrastructure)
5. [Blogs and demos](#blogs-and-demos) — [Perspectives](#blogs-and-perspectives) · [X / Twitter evidence](#social-demos-and-evaluations)

</details>

## Getting started

### What is a robot-use agent?

For this list, a **robot-use agent** is a system that turns a goal into robot actions by selecting skills, generating executable programs, or calling perception and control tools. Its interaction with the environment may include observation, execution feedback, replanning, and recovery. This is a working definition for curation, not a standardized field taxonomy.

| Layer | Main question | Typical interface |
| --- | --- | --- |
| Agent | What should happen next? | Goals, plans, tool calls, generated programs |
| Harness | How is execution organized and evaluated? | Context, memory, skill routing, outcome checks, recovery |
| Policy / controller | How is a physical action performed? | Learned policies, motion planning, control primitives |
| Environment / evaluation | What happened, and did the task succeed? | Observations, state changes, task predicates, rollout logs |

An LLM may use a robot as a tool; a robot may also use a physical tool such as a hammer. This list focuses on the former system boundary. A VLA can supply an agent's action capability, but a VLA checkpoint alone does not specify the surrounding agent workflow. Similarly, an MCP bridge exposes capabilities without necessarily providing planning or recovery.

Follow the workflow from robot interfaces and agent runtimes to planning, feedback, and evaluation. General-purpose perception, planning, execution, and model libraries are grouped separately under supporting components. A work that spans several roles receives one main entry; other sections use cross-references. Placement does not imply that every work implements the entire loop or has been independently reproduced.

### Start here

Choose an entry point by what you want to build or inspect. Links lead to official documentation and examples; they are not local reproduction records.

| Your next step | Entry points | What to inspect |
| --- | --- | --- |
| Understand robot-as-a-tool | [Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) | The boundary between an agent, its tools, and robot control |
| Connect an existing ROS robot | [ROS MCP Server](https://github.com/robotmcp/ros-mcp-server) · [ros-skill](https://github.com/lpigeon/ros-skill) · [ROSA](https://github.com/nasa-jpl/rosa) | Available commands, observations, and robot-specific setup |
| Start with a simulation workflow | [Strands Robots](https://github.com/strands-labs/robots) | Agent tool calls, policy execution, and simulator configuration |
| Inspect an embodied harness | [Show-Harness](https://github.com/showlab/Show-Harness) · [Thea](https://github.com/EIT-HAI/Thea) | Action abstractions, observation flow, execution checks, and recovery |
| Study planning and generated programs | [SayCan](https://say-can.github.io/) · [Code as Policies](https://code-as-policies.github.io/) · [CaP-X](https://github.com/capgym/cap-x) | Skill selection, generated control code, and interaction interfaces |
| Study feedback and improvement | [Inner Monologue](https://innermonologue.github.io/) · [Zetta](https://github.com/air-embodied-brain/Zetta-Embodiment) · [ENPIRE](https://github.com/NVlabs/ENPIRE) | Replanning, runtime critics, recovery, and policy refinement |
| Evaluate an agent | [EmbodiedBench](https://github.com/EmbodiedBench/EmbodiedBench) · [Inspect Robots](https://github.com/robocurve/inspect-robots) | Task protocols, rollout logs, success criteria, and intervention |

### How to compare systems

<details>
<summary><strong>Comparison checklist: observations, actions, feedback, timing, and evidence</strong></summary>

For each system or demonstration, distinguish **author-reported results**, **source inspection**, and **local execution**. A repository link alone is not a reproduction record. Missing evidence should be recorded as `Not reported`; unchecked availability as `Unverified`.

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

### At a glance

| Collection | Entries | What you will find |
| --- | --- | --- |
| [Agents and frameworks](#agents-and-frameworks) | 20 | Planning, feedback, policy orchestration, agent runtimes, and robot interfaces |
| [Agent evaluation](#agent-benchmarks-and-evaluation-frameworks) | 3 | Benchmarks and frameworks for assessing agent decisions and execution |
| [Environments and task suites](#simulation-environments-and-task-suites) | 3 | Manipulation and household tasks, with associated data |
| [Supporting components](#supporting-components) | 13 | Seven perception, planning, and execution components; three API model families; three policy/learning resources |

[X / Twitter resources](#social-demos-and-evaluations): **14 original posts** covering robot demonstrations, evaluations, and research discussions. These supplement the 39 resources counted above.

**Reading the links:** `Paper` describes a method; `Project` may contain only descriptions and demos; `Code` points to implementation resources; `Docs` describes a platform interface. Code, weights, data, and full reproduction are separate release claims. “Unverified release” means this list has not confirmed the relevant artifact, not that it does not exist.

## Agents and frameworks

<a id="research-papers"></a>

Each work has one main entry, grouped by its role in a robot-use system. Paper, Code, Project, Model, and Demo are links to artifacts of that work, not separate categories. Dated research entries are ordered by first arXiv release within each group. Star badges show repository totals, including the full monorepo for Code as Policies and SayCan. `Unverified` means implementation availability has not been confirmed. Method summaries reflect the authors' descriptions; this list does not claim independent reproduction.

### Robot interfaces and tools

<a id="projects-and-tools"></a>

Agent-facing interfaces to robot observations, actions, and execution feedback belong here. General-purpose models and libraries belong under [Supporting components](#supporting-components); a separate project that wraps one as a robot-use tool is classified by the interface it actually provides.

| Resource | Role | Scope / boundary | Official source |
| --- | --- | --- | --- |
| **ROSA — Robot Operating System Agent** | Natural-language agent for ROS systems | Supports inspection, diagnosis, and robot operation through tools; custom robots need appropriate tools and context. | [Code and documentation](https://github.com/nasa-jpl/rosa) · [Paper](https://arxiv.org/abs/2410.06472) |
| **ROS MCP Server** | MCP interface to ROS | Exposes robot communication and introspection through ROS/rosbridge. Planning and outcome evaluation depend on the connected agent and robot stack. | [Code and documentation](https://github.com/robotmcp/ros-mcp-server) |
| **ros-skill** | Agent Skill with a Python CLI for ROS/ROS 2 | Exposes topic, service, node, parameter, and action commands via rosbridge WebSocket, returning JSON. Planning and outcome interpretation remain with the calling agent; a configured robot and rosbridge are required. | [Code and command reference](https://github.com/lpigeon/ros-skill) <br> [![GitHub stars](https://img.shields.io/github/stars/lpigeon/ros-skill?style=flat-square&label=stars)](https://github.com/lpigeon/ros-skill) |

### Agent runtimes and orchestration

Frameworks for connecting agents, observations, skills, and execution backends. These entries were checked against their public repositories and documentation; installation and robot operation have not been independently validated here.

| Resource | Role | Scope / boundary | Official source |
| --- | --- | --- | --- |
| **AgenticROS** | ROS 2 capability and mission runtime | Exposes named skills through MCP and agent adapters; mission graphs pass outputs between steps and support failure branches. Its built-in natural-language mission compiler is rule-based, not an LLM planner. | [Code](https://github.com/agenticros/agenticros) · [Docs](https://github.com/agenticros/agenticros#architecture) <br> [![GitHub stars](https://img.shields.io/github/stars/agenticros/agenticros?style=flat-square&label=stars)](https://github.com/agenticros/agenticros) |
| **DimOS** | Python robot runtime with perception, spatial memory, navigation, and agent skills | Provides CLI and MCP interfaces plus replay, simulation, and hardware workflows. Pre-release Beta; individual hardware integrations range from stable to experimental. | [Code](https://github.com/dimensionalOS/dimos) · [Docs](https://docs.dimensionalos.com) <br> [![GitHub stars](https://img.shields.io/github/stars/dimensionalOS/dimos?style=flat-square&label=stars)](https://github.com/dimensionalOS/dimos) |
| **EmbodiedAgents** | ROS 2 intelligence and component orchestration in the EMOS ecosystem | Connects local or hosted models, memory, and event-driven component graphs. Its visual-question-answering quickstart alone does not establish a complete robot-control loop; motion requires the relevant robot components. | [Code](https://github.com/automatika-robotics/embodied-agents) · [Docs](https://automatika-robotics.github.io/embodied-agents/) <br> [![GitHub stars](https://img.shields.io/github/stars/automatika-robotics/embodied-agents?style=flat-square&label=stars)](https://github.com/automatika-robotics/embodied-agents) |
| **RAI** | ROS 2 agent framework with perception, robot descriptions, speech, and evaluation components | Includes simulation integrations and rai_bench; robot-specific tools and configuration are required. The README lists rai_finetune as unfinished. | [Code](https://github.com/RobotecAI/rai) · [Docs](https://robotecai.github.io/rai/) · [Paper](https://arxiv.org/abs/2505.07532) <br> [![GitHub stars](https://img.shields.io/github/stars/RobotecAI/rai?style=flat-square&label=stars)](https://github.com/RobotecAI/rai) |
| **Strands Robots** | Robot tools and policy execution for Strands Agents | Wraps simulation or hardware behind a robot tool, with policy, recording, and training integrations. MuJoCo is the default; real hardware is opt-in. Simulator asset coverage is not evidence of equivalent hardware support. | [Code](https://github.com/strands-labs/robots) · [Docs](https://strands-labs.github.io/robots) <br> [![GitHub stars](https://img.shields.io/github/stars/strands-labs/robots?style=flat-square&label=stars)](https://github.com/strands-labs/robots) |

### Embodied harnesses and policy orchestration

<details open>
<summary>Browse 6 papers</summary>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-09 | **Show-Harness: Just a VLM Agent Can Play Robots** <br> [Project and demos](https://showlab.github.io/Show-Harness/) · [Model adapters](https://huggingface.co/showlab/Show-Harness-VLMs) · [Data](https://huggingface.co/datasets/showlab/Show-Harness-Data) | [Paper](https://arxiv.org/abs/2609.10522) | [Code](https://github.com/showlab/Show-Harness) <br> [![GitHub stars](https://img.shields.io/github/stars/showlab/Show-Harness?style=flat-square&label=stars)](https://github.com/showlab/Show-Harness) | VLMs select discrete, incremental action units grounded by robot-specific interpreters. Includes planning, action-history and recovery plugins, GUMI demonstration collection, and fine-tuning tools. Franka/Piper and simulator adapters require their documented dependencies and site configuration; not independently deployed here. |
| 2026-08 | **Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence** <br> [Project](https://air-embodied-brain.github.io/zetta/) | [Paper](https://arxiv.org/abs/2608.16590) | [Code](https://github.com/air-embodied-brain/Zetta-Embodiment) <br> [![GitHub stars](https://img.shields.io/github/stars/air-embodied-brain/Zetta-Embodiment?style=flat-square&label=stars)](https://github.com/air-embodied-brain/Zetta-Embodiment) | Keeps the base policy frozen while developing runtime critics and recovery skills through execution, diagnosis, and gated updates. The separate `air-embodied-brain/zetta` repository hosts the project website. |
| 2026-08 | **Thea — Towards the Harness of Embodied Agents** <br> [Project](https://eit-hai.github.io/thea/) | [Paper](https://arxiv.org/abs/2608.11246) | [Code](https://github.com/EIT-HAI/Thea) <br> [![GitHub stars](https://img.shields.io/github/stars/EIT-HAI/Thea?style=flat-square&label=stars)](https://github.com/EIT-HAI/Thea) | Wraps robot capabilities as callable tools, maintains symbolic scene context, and evaluates action termination, success, and failure causes. Public runtime and interfaces; robot/simulator deployment requires concrete adapters and capabilities. |
| 2026-07 | **RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning** | [Paper](https://arxiv.org/abs/2607.18060) | Unverified | Uses execution memory to route among heterogeneous policies and a Memory Bridge to improve handoffs between policies. |
| 2026-06 | **ENPIRE: Agentic Robot Policy Self-Improvement in the Real World** <br> [Project](https://research.nvidia.com/labs/gear/enpire/) | [Paper](https://arxiv.org/abs/2606.19980) | [Code](https://github.com/NVlabs/ENPIRE) <br> [![GitHub stars](https://img.shields.io/github/stars/NVlabs/ENPIRE?style=flat-square&label=stars)](https://github.com/NVlabs/ENPIRE) | Connects scene reset, policy execution, outcome verification, and experiment refinement so coding agents can improve policies through physical trials. Deployment requires calibrated stations and task-specific reset and verification functions. |
| 2026-06 | **Guava: An Effective and Universal Harness for Embodied Manipulation** | [Paper](https://arxiv.org/abs/2606.18363) | Unverified | Studies iterative perception–reasoning–action, semantic action abstractions, and multimodal observations; also describes distillation into a smaller agent model. Checkpoint availability also unverified. |

</details>

[Back to top](#awesome-robot-use-agent-rua)

### Planning and code as policies

<details open>
<summary>Browse 4 papers</summary>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-03 | **CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation** | [Paper](https://arxiv.org/abs/2603.22435) | [Code](https://github.com/capgym/cap-x) <br> [![GitHub stars](https://img.shields.io/github/stars/capgym/cap-x?style=flat-square&label=stars)](https://github.com/capgym/cap-x) | Studies embodied coding agents through CaP-Gym, CaP-Bench, CaP-Agent0, and CaP-RL, including execution feedback and skill synthesis. |
| 2023-07 | **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models** <br> [Project and demos](https://voxposer.github.io/) | [Paper](https://arxiv.org/abs/2307.05973) | [Code](https://github.com/huangwl18/VoxPoser) <br> [![GitHub stars](https://img.shields.io/github/stars/huangwl18/VoxPoser?style=flat-square&label=stars)](https://github.com/huangwl18/VoxPoser) | Uses generated code and visual grounding to construct 3D value maps for motion planning; the generated program can be reevaluated with visual feedback. The public repository provides an RLBench demo; it excludes the full perception pipeline used in real-robot experiments. |
| 2022-09 | **Code as Policies: Language Model Programs for Embodied Control** <br> [Project and demos](https://code-as-policies.github.io/) · [Blog](https://research.google/blog/robots-that-write-their-own-code/) | [Paper](https://arxiv.org/abs/2209.07753) | [Code](https://github.com/google-research/google-research/tree/master/code_as_policies) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Generates programs that compose perception outputs, control APIs, and feedback loops. |
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


## Benchmarks and environments

### Agent benchmarks and evaluation frameworks

| Resource | What it evaluates / provides | Reading note | Official source |
| --- | --- | --- | --- |
| **Embodied Agent Interface (EAI)** | Goal interpretation, subgoal decomposition, action sequencing, and transition modeling | Useful for identifying decision-making errors; symbolic module evaluation should be distinguished from end-to-end physical execution. | [Code and documentation](https://github.com/embodied-agent-interface/embodied-agent-interface) |
| **EmbodiedBench** | Vision-driven embodied agents across high- and low-level tasks | Provides multiple environments and capability-oriented evaluation, including navigation and manipulation. | [Code and documentation](https://github.com/EmbodiedBench/EmbodiedBench) |
| **Inspect Robots** | Evaluation framework connecting policies, embodiments, benchmarks, and logs | Supports compatible LLM-agent and VLA integrations; currently described by its maintainers as alpha software. | [Code and documentation](https://github.com/robocurve/inspect-robots) |

[CaP-X](https://github.com/capgym/cap-x), listed under planning and code as policies, also provides CaP-Bench for comparing embodied coding agents at different interface abstraction and interaction levels.

### Simulation environments and task suites

These provide tasks and execution environments for agent research. An environment's inclusion does not mean its standard protocol evaluates tool use, streaming interaction, interruption, or recovery.

| Resource | Useful for | Official source |
| --- | --- | --- |
| **LIBERO** | Manipulation tasks and demonstrations for studying transfer across spatial, object, goal, and task variations | [Code and datasets](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **RoboCasa / RoboCasa365** | Kitchen manipulation, atomic and composite tasks, and demonstration data | [Project, code, and datasets](https://robocasa.ai/) |
| **BEHAVIOR-1K / OmniGibson** | Long-horizon household activities and rich object interactions | [Project and documentation](https://behavior.stanford.edu/) |

[Back to top](#awesome-robot-use-agent-rua)


## Supporting components

Selected building blocks for constructing robot-use tools and agents. These general-purpose components do not, by themselves, provide an agent-facing robot-use interface or a complete observation–action–feedback loop. Their possible roles below are integration suggestions, not claims of a validated robot-use system. We keep this selection focused rather than cataloguing all robotics and vision libraries.

### Perception and spatial understanding

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **Grounded SAM 2** | Text-guided object detection, segmentation, and video tracking | A perception pipeline, not a robot-use interface. Converting masks into robot-frame targets requires depth, calibration, and a control adapter; local-model and cloud-API paths have different dependencies. | [Code and documentation](https://github.com/IDEA-Research/Grounded-SAM-2) |
| **FoundationPose** | 6D object pose estimation and tracking from CAD models or reference images | Requires the corresponding object inputs and inference setup. Its source license limits use to non-commercial research or evaluation. | [Code](https://github.com/NVlabs/FoundationPose) · [License](https://github.com/NVlabs/FoundationPose/blob/main/LICENSE) |
| **ConceptGraphs** | Open-vocabulary 3D scene graphs from posed RGB-D observations | Can support object and spatial-relation queries; requires upstream perception and camera poses. Inclusion does not establish dynamic-world consistency or a complete agent memory system. | [Code and documentation](https://github.com/concept-graphs/concept-graphs) |

### Motion planning and control

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **cuRobo** | GPU-accelerated kinematics, collision checking, and motion generation | Requires CUDA, robot and collision-world configuration, and an execution adapter. Planning a trajectory does not verify task success. | [Code and documentation](https://github.com/NVlabs/curobo) |
| **MPlib** | Lightweight Python motion planning decoupled from ROS | A planning backend for a custom tool; robot models, collision geometry, and execution must be supplied by the application. | [Code and documentation](https://github.com/haosulab/MPlib) |
| **Mink** | MuJoCo-based differential inverse kinematics with joint limits and collision avoidance | A local kinematic solver, not a global task planner or a locomotion policy. The application supplies targets and the control loop. | [Code and documentation](https://github.com/kevinzakka/mink) |

### Execution infrastructure

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **BehaviorTree.CPP** | Behavior-tree execution and composition in C++ | An execution backend for application-defined actions and conditions; robot bindings, agent integration, and outcome checks must be supplied separately. | [Code and documentation](https://github.com/BehaviorTree/BehaviorTree.CPP) |

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

## Blogs and demos

### Blogs and perspectives

- **[Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html)** — Phillip Isola · 2026-09-07 · **Perspective**. General-purpose AI agents using robots through sensor and actuator APIs, with discussion of deployment, latency, and reliability. [Author post](https://x.com/phillip_isola/status/2097045136051933566); discusses agents including Claude, rather than a GPT-6-only evaluation.
- **[Planning versus high-frequency robot control](https://x.com/JitendraMalikCV/status/2097173961264284039)** — Jitendra Malik · 2026-09-08 · **Discussion**. Challenges extrapolation from planning demonstrations to dexterity, force/torque control, and locomotion on varying terrain. A research question, not an experimental result.

Official project videos and introductory articles are linked from their [main agent entries](#agents-and-frameworks). The posts below are additional reports and discussions, not additional implementations of those systems.

### Social demos and evaluations

Selected X / Twitter posts about GPT-6 Astra, with dates in UTC+8. The 12 demo/evaluation posts are grouped into 11 entries; Wenli Xiao and Tonghe Zhang describe the same group's work. The two accompanying research discussions appear under [Blogs and perspectives](#blogs-and-perspectives).

[Real robots](#real-robot-demonstrations) · [Simulation](#simulation-demonstrations) · [Perception and reconstruction](#perception-and-reconstruction) · [Research discussions](#blogs-and-perspectives)

These summaries reflect author reports and public post-text snapshots collected on 2026-09-10. They are not independent reproductions or a model ranking; videos have not been reviewed frame by frame. Follow the original posts and linked artifacts for context.

#### Real-robot demonstrations

| Date | Author / task | What is shown or reported | Sources / reading notes |
| --- | --- | --- | --- |
| 2026-09-10 | **Wenli Xiao / Tonghe Zhang — video-conditioned robot imitation** | A human demonstration video is supplied to a coding agent to guide a robot arm; authors report first-attempt success on the shown task. | [Xiao post](https://x.com/_wenlixiao/status/2097801944119349455) · [Zhang post](https://x.com/TongheZhang01/status/2097801107602911243) · [ENPIRE](https://github.com/NVlabs/ENPIRE). Related posts, not independent replications; no aggregate task success rate supplied. |
| 2026-09-08 | **Thijs — SO-101 brush painting** | Camera-guided painting of the Golden Gate Bridge, with improvement over attempts. | [Post](https://x.com/cdngdev/status/2097339677128982873) · [Control details](https://x.com/cdngdev/status/2097339677745516710). Author supplied calibration anchors and feedback; roughly one-minute action segments with background monitoring. |
| 2026-09-06 | **ARX — washing-machine knob operation** | Natural-language instruction to turn a knob in a new room; author says GPT plus a custom control layer, without a VLA. | [Post](https://x.com/ARXrobotics/status/2096328304794210604) · [Author clarification](https://x.com/ARXrobotics/status/2096449872782348475). Case demonstration; repeated success rate and control-layer capabilities remain unverified. |
| 2026-09-05 | **Jay Chooi / Robocurve — pick-and-place and insertion** | Under Inspect Robots, Astra completed block-into-bowl in **19/20** trials and puzzle insertion in **2/20**. | [Post](https://x.com/chooi_jeq/status/2096064315115839904) · [Report and trial records](https://openai.robocurve.org/gpt-6-astra/). Human, non-blind grading; bowl comparisons used different rigs. The 95% figure applies only to the bowl task. |

#### Simulation demonstrations

| Date | Author / task | What is shown or reported | Sources / reading notes |
| --- | --- | --- | --- |
| 2026-09-09 | **H / thermalpastor — two-robot juggling** | Two robots exchange balls in MuJoCo, keeping at least one airborne. | [Post](https://x.com/thermalpastor/status/2097496200631210136). Author labels the playback 1× simulation speed; this does not establish real-time model inference or hardware control. |
| 2026-09-08 | **Dmytro Hrybov — dexterous-hand drawing** | A generated MuJoCo setup and controller use a Kinova Gen3 arm and Shadow Hand to draw a dove through pen–paper contact. | [Post](https://x.com/dimentary/status/2097141042214797801) · [Contact and timing details](https://x.com/dimentary/status/2097141323883327933). Two-finger grip despite a five-finger hand; video sped up 4×. |
| 2026-09-07 | **Dmytro Hrybov — six-legged, dual-arm transport** | Building a MuJoCo embodiment and controller that move objects between tables. | [Post](https://x.com/dimentary/status/2096785235795181900). Simulation demonstration; an unusual morphology alone does not establish out-of-distribution generalization. |
| 2026-09-06 | **Hakim Phun — RoboDojo tasks** | Selected robot-simulation task demonstrations. | [Post](https://x.com/Hakim_Fang/status/2096565038744252613). The collection records the author's caveat that inference pauses were removed and a full quantitative evaluation was not yet available. |

#### Perception and reconstruction

These are supporting capabilities for robot-use workflows, rather than direct evidence of a complete robot-control agent.

| Date | Author / task | What is shown or reported | Sources / reading notes |
| --- | --- | --- | --- |
| 2026-09-10 | **Lingxiao Guo — video-to-Wuji-hand retargeting** | Real2Sim and motion retargeting from two videos, without supplied states or actions. | [Post](https://x.com/Lingxiao234/status/2097717020540481630). Execution environment, hardware deployment, repeatability, and this demo's code release remain unverified; the separate Real2Sim repository is not assumed to reproduce this result. |
| 2026-09-08 | **Lingxiao Guo — robot-demonstration Real2Sim** | Multi-view RGB and robot actions used for calibration, asset reconstruction, physical-parameter fitting, MuJoCo simulation, and Blender rendering. | [Post](https://x.com/Lingxiao234/status/2096992059731443923) · [Code and limitations](https://github.com/lingxiao-guo/GPT6-real2sim). Released examples include placement errors, approximate alignment, and failed contact-only microphone attachment; visual agreement is not validated dynamics recovery. |
| 2026-09-08 | **Kingston Kuan — egocentric 3D hand pose** | Comparison against MediaPipe using the same output schema, including gloved hands. | [Post](https://x.com/kstonekuan/status/2097119396032569555). Author reports about **3 min/frame** for Astra at high reasoning effort versus **20 ms/frame** for MediaPipe; no aggregate ground-truth accuracy metric supplied. |

[Back to top](#awesome-robot-use-agent-rua)

## Contributing

Suggestions and corrections are welcome! Please read the [contribution guidelines](CONTRIBUTING.md) before opening an issue or pull request.

[Back to top](#awesome-robot-use-agent-rua)

## Citation

If you find this collection helpful for your research, you can cite it with the following BibTeX entry:

```bibtex
@misc{awesome-robot-use-agent,
  title   = {Awesome Robot Use Agent},
  author  = {Kairun Wen and {Awesome Robot Use Agent Contributors}},
  journal = {GitHub repository},
  url     = {https://github.com/kairunwen/Awesome-Robot-Use-Agent},
  year    = {2026},
  note    = {A curated collection of resources for robot-use agents.}
}
```
