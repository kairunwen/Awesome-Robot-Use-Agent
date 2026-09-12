<div align="center">

<img src="assets/logo.png" alt="RUA logo: a robotic hand gently petting a happy cat" width="160" />

# Awesome Robot Use Agent (RUA)

[![Awesome](https://img.shields.io/badge/Awesome-List-111111.svg?style=for-the-badge&labelColor=000000&logo=awesomelists&logoColor=white)](https://awesome.re) [![Website](https://img.shields.io/badge/Website-Visit-111111.svg?style=for-the-badge&labelColor=000000&logo=githubpages&logoColor=white)](https://kairunwen.github.io/Awesome-Robot-Use-Agent/) [![Resources: 39](https://img.shields.io/badge/Resources-39-111111.svg?style=for-the-badge&labelColor=000000&logo=readthedocs&logoColor=white)](#contents) [![Demo](https://img.shields.io/badge/Demo-Watch-111111.svg?style=for-the-badge&labelColor=000000&logo=x&logoColor=white)](#social-demos)
<br>
[![Tools](https://img.shields.io/badge/Tools-Explore-111111.svg?style=for-the-badge&labelColor=000000&logo=ros&logoColor=white)](#robot-interfaces-and-tools) [![PRs welcome](https://img.shields.io/badge/PRs-Welcome-111111.svg?style=for-the-badge&labelColor=000000&logo=git&logoColor=white)](#contributing) [![GitHub Stars](https://img.shields.io/github/stars/kairunwen/Awesome-Robot-Use-Agent?style=for-the-badge&label=Stars&labelColor=000000&color=111111&logo=github&logoColor=white)](https://github.com/kairunwen/Awesome-Robot-Use-Agent/stargazers) [![License: MIT](https://img.shields.io/badge/License-MIT-111111.svg?style=for-the-badge&labelColor=000000)](LICENSE)

[Articles](#articles) · [Papers](#papers) · [Projects](#projects) · [Benchmarks](#benchmarks-1)

</div>

> A **robot-use agent** is an AI system that can **reason** about tasks, **plan** sequences of actions, and **act** in the physical world through robot skills, generated code, and perception/control APIs. It combines observations with execution feedback to track progress, revise plans, and recover from failures while pursuing a user-specified goal.

A curated collection of articles, papers, open-source projects, community demos, and benchmarks for **robot-use agents**. Explore how AI agents connect to robots, use perception and control tools, generate executable code, and learn from execution feedback to carry out tasks in simulation and the **physical world.**

## Contents

- [Getting started](#getting-started)
- [Articles](#articles)
- [Papers](#papers)
  - [Surveys](#surveys)
  - [Models & Frameworks](#models--frameworks)
  - [Datasets](#datasets)
  - [Benchmarks](#benchmark-papers)
- [Projects](#projects)
  - [Open Source](#open-source)
    - [Systems & Frameworks](#systems--frameworks)
    - [Environment & Sandbox](#environment--sandbox)
    - [Other Tools](#other-tools)
    - [Components](#components)
  - [Social Demos](#social-demos)
- [Benchmarks](#benchmarks-1)

[Contributing](#contributing) · [Citation](#citation)

## Getting started

Robot-use agents turn goals into robot actions through skills, generated code, and perception/control APIs.

- **Read:** [Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) — an introduction to the idea.
- **Build:** [ROS MCP Server](https://github.com/robotmcp/ros-mcp-server) for ROS integration; [Strands Robots](https://github.com/strands-labs/robots) for a simulation workflow.
- **Watch:** [Social Demos](#social-demos) — community demonstrations.
- **Evaluate:** [CaP-X / CaP-Bench](https://github.com/capgym/cap-x) · [Inspect Robots](https://github.com/robocurve/inspect-robots).

## Articles

<a id="blogs-and-demos"></a>
<a id="blogs-and-perspectives"></a>

- **[Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html)** — Phillip Isola · 2026-09-07 · **Perspective**. General-purpose AI agents using robots through sensor and actuator APIs, with discussion of deployment, latency, and reliability. [Author post](https://x.com/phillip_isola/status/2097045136051933566); discusses agents including Claude, rather than a GPT-6-only evaluation.
- **[Planning versus high-frequency robot control](https://x.com/JitendraMalikCV/status/2097173961264284039)** — Jitendra Malik · 2026-09-08 · **Discussion**. Challenges extrapolation from planning demonstrations to dexterity, force/torque control, and locomotion on varying terrain. A research question, not an experimental result.

## Papers

Paper references are grouped by contribution. Dates refer to first arXiv release. Method summaries reflect author reports; code, weights, and complete reproduction are separate release claims. Implementation entries and benchmark descriptions are cross-linked rather than counted as additional distinct works.

<a id="research-papers"></a>

### Surveys

| Date | Work | Focus | Sources |
| --- | --- | --- | --- |
| 2024-04 | **A Survey on Integration of Large Language Models with Intelligent Robots** | LLM integration across communication, perception, planning, and control. | [Paper](https://arxiv.org/abs/2404.09228) |

### Models & Frameworks

<a id="embodied-harnesses-and-policy-orchestration"></a>
<a id="planning-and-code-as-policies"></a>
<a id="execution-feedback-and-recovery"></a>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-09 | **Show-Harness: Just a VLM Agent Can Play Robots** <br> [Project and demos](https://showlab.github.io/Show-Harness/) · [Model adapters](https://huggingface.co/showlab/Show-Harness-VLMs) · [Data](https://huggingface.co/datasets/showlab/Show-Harness-Data) | [Paper](https://arxiv.org/abs/2609.10522) | [Code](https://github.com/showlab/Show-Harness) <br> [![GitHub stars](https://img.shields.io/github/stars/showlab/Show-Harness?style=flat-square&label=stars)](https://github.com/showlab/Show-Harness) | VLMs select discrete, incremental action units grounded by robot-specific interpreters. Includes planning, action-history and recovery plugins, GUMI demonstration collection, and fine-tuning tools. Franka/Piper and simulator adapters require their documented dependencies and site configuration; not independently deployed here. |
| 2026-08 | **Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence** <br> [Project](https://air-embodied-brain.github.io/zetta/) | [Paper](https://arxiv.org/abs/2608.16590) | [Code](https://github.com/air-embodied-brain/Zetta-Embodiment) <br> [![GitHub stars](https://img.shields.io/github/stars/air-embodied-brain/Zetta-Embodiment?style=flat-square&label=stars)](https://github.com/air-embodied-brain/Zetta-Embodiment) | Keeps the base policy frozen while developing runtime critics and recovery skills through execution, diagnosis, and gated updates. The separate `air-embodied-brain/zetta` repository hosts the project website. |
| 2026-08 | **Thea — Towards the Harness of Embodied Agents** <br> [Project](https://eit-hai.github.io/thea/) | [Paper](https://arxiv.org/abs/2608.11246) | [Code](https://github.com/EIT-HAI/Thea) <br> [![GitHub stars](https://img.shields.io/github/stars/EIT-HAI/Thea?style=flat-square&label=stars)](https://github.com/EIT-HAI/Thea) | Wraps robot capabilities as callable tools, maintains symbolic scene context, and evaluates action termination, success, and failure causes. Public runtime and interfaces; robot/simulator deployment requires concrete adapters and capabilities. |
| 2026-07 | **RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning** | [Paper](https://arxiv.org/abs/2607.18060) | Unverified | Uses execution memory to route among heterogeneous policies and a Memory Bridge to improve handoffs between policies. |
| 2026-06 | **Guava: An Effective and Universal Harness for Embodied Manipulation** | [Paper](https://arxiv.org/abs/2606.18363) | Unverified | Studies iterative perception–reasoning–action, semantic action abstractions, and multimodal observations; also describes distillation into a smaller agent model. Checkpoint availability also unverified. |
| 2026-06 | **ENPIRE: Agentic Robot Policy Self-Improvement in the Real World** <br> [Project](https://research.nvidia.com/labs/gear/enpire/) | [Paper](https://arxiv.org/abs/2606.19980) | [Code](https://github.com/NVlabs/ENPIRE) <br> [![GitHub stars](https://img.shields.io/github/stars/NVlabs/ENPIRE?style=flat-square&label=stars)](https://github.com/NVlabs/ENPIRE) | Connects scene reset, policy execution, outcome verification, and experiment refinement so coding agents can improve policies through physical trials. Deployment requires calibrated stations and task-specific reset and verification functions. |
| 2023-07 | **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models** <br> [Project and demos](https://voxposer.github.io/) | [Paper](https://arxiv.org/abs/2307.05973) | [Code](https://github.com/huangwl18/VoxPoser) <br> [![GitHub stars](https://img.shields.io/github/stars/huangwl18/VoxPoser?style=flat-square&label=stars)](https://github.com/huangwl18/VoxPoser) | Uses generated code and visual grounding to construct 3D value maps for motion planning; the generated program can be reevaluated with visual feedback. The public repository provides an RLBench demo; it excludes the full perception pipeline used in real-robot experiments. |
| 2023-06 | **REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction** <br> [Project](https://robot-reflect.github.io/) | [Paper](https://arxiv.org/abs/2306.15724) | [Code](https://github.com/real-stanford/reflect) <br> [![GitHub stars](https://img.shields.io/github/stars/real-stanford/reflect?style=flat-square&label=stars)](https://github.com/real-stanford/reflect) | Summarizes multisensory execution history, explains failures, and conditions a planner on those explanations to produce corrective actions. |
| 2022-09 | **Code as Policies: Language Model Programs for Embodied Control** <br> [Project and demos](https://code-as-policies.github.io/) · [Blog](https://research.google/blog/robots-that-write-their-own-code/) | [Paper](https://arxiv.org/abs/2209.07753) | [Code](https://github.com/google-research/google-research/tree/master/code_as_policies) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Generates programs that compose perception outputs, control APIs, and feedback loops. |
| 2022-07 | **Inner Monologue: Embodied Reasoning through Planning with Language Models** <br> [Project and demos](https://innermonologue.github.io/) | [Paper](https://arxiv.org/abs/2207.05608) | Unverified | Feeds success detection, scene descriptions, and human feedback into language-based planning; demonstrates replanning and responses to changed goals. |
| 2022-04 | **SayCan — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances** <br> [Project](https://say-can.github.io/) | [Paper](https://arxiv.org/abs/2204.01691) | [Code: tabletop simulation](https://github.com/google-research/google-research/tree/master/saycan) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Combines language-model skill scoring with affordance/value estimates to select feasible robot behaviors. |

### Datasets

| Date | Work | Focus | Sources |
| --- | --- | --- | --- |
| 2023-10 | **Open X-Embodiment: Robotic Learning Datasets and RT-X Models** | Robot demonstration data across embodiments, supporting policy learning. It is not a dataset of agent tool-call traces; constituent dataset terms must be checked individually. | [Paper](https://arxiv.org/abs/2310.08864) · [Project](https://robotics-transformer-x.github.io/) · [Data and documentation](https://github.com/google-deepmind/open_x_embodiment) |

<a id="benchmark-papers"></a>

### Benchmarks

Research references; see the [benchmark catalogue](#benchmarks-1) for evaluation projects and usage notes.

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-03 | **CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation** | [Paper](https://arxiv.org/abs/2603.22435) | [Code](https://github.com/capgym/cap-x) <br> [![GitHub stars](https://img.shields.io/github/stars/capgym/cap-x?style=flat-square&label=stars)](https://github.com/capgym/cap-x) | Studies embodied coding agents through CaP-Gym, CaP-Bench, CaP-Agent0, and CaP-RL, including execution feedback and skill synthesis. |
| 2025-02 | **EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents** | [Paper](https://arxiv.org/abs/2502.09560) | [Code](https://github.com/EmbodiedBench/EmbodiedBench) | Vision-driven embodied-agent evaluation; see the [benchmark catalogue](#benchmarks-1). |
| 2024-10 | **Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making** | [Paper](https://arxiv.org/abs/2410.07166) | [Code](https://github.com/embodied-agent-interface/embodied-agent-interface) | Evaluation of embodied decision-making modules; see the [benchmark catalogue](#benchmarks-1). |


## Projects

### Open Source

Code links and usage restrictions are recorded per entry. Research works with unverified code releases are retained in Papers. Check each repository, model, and dataset license before reuse.

<details class="project-group">
<summary><h4>Systems &amp; Frameworks</h4></summary>

<a id="agents-and-frameworks"></a>

<a id="agent-runtimes-and-orchestration"></a>

| Resource | Role | Scope / boundary | Official source |
| --- | --- | --- | --- |
| **AgenticROS** | ROS 2 capability and mission runtime | Exposes named skills through MCP and agent adapters; mission graphs pass outputs between steps and support failure branches. Its built-in natural-language mission compiler is rule-based, not an LLM planner. | [Code](https://github.com/agenticros/agenticros) · [Docs](https://github.com/agenticros/agenticros#architecture) <br> [![GitHub stars](https://img.shields.io/github/stars/agenticros/agenticros?style=flat-square&label=stars)](https://github.com/agenticros/agenticros) |
| **DimOS** | Python robot runtime with perception, spatial memory, navigation, and agent skills | Provides CLI and MCP interfaces plus replay, simulation, and hardware workflows. Pre-release Beta; individual hardware integrations range from stable to experimental. | [Code](https://github.com/dimensionalOS/dimos) · [Docs](https://docs.dimensionalos.com) <br> [![GitHub stars](https://img.shields.io/github/stars/dimensionalOS/dimos?style=flat-square&label=stars)](https://github.com/dimensionalOS/dimos) |
| **EmbodiedAgents** | ROS 2 intelligence and component orchestration in the EMOS ecosystem | Connects local or hosted models, memory, and event-driven component graphs. Its visual-question-answering quickstart alone does not establish a complete robot-control loop; motion requires the relevant robot components. | [Code](https://github.com/automatika-robotics/embodied-agents) · [Docs](https://automatika-robotics.github.io/embodied-agents/) <br> [![GitHub stars](https://img.shields.io/github/stars/automatika-robotics/embodied-agents?style=flat-square&label=stars)](https://github.com/automatika-robotics/embodied-agents) |
| **RAI** | ROS 2 agent framework with perception, robot descriptions, speech, and evaluation components | Includes simulation integrations and rai_bench; robot-specific tools and configuration are required. The README lists rai_finetune as unfinished. | [Code](https://github.com/RobotecAI/rai) · [Docs](https://robotecai.github.io/rai/) · [Paper](https://arxiv.org/abs/2505.07532) <br> [![GitHub stars](https://img.shields.io/github/stars/RobotecAI/rai?style=flat-square&label=stars)](https://github.com/RobotecAI/rai) |
| **Strands Robots** | Robot tools and policy execution for Strands Agents | Wraps simulation or hardware behind a robot tool, with policy, recording, and training integrations. MuJoCo is the default; real hardware is opt-in. Simulator asset coverage is not evidence of equivalent hardware support. | [Code](https://github.com/strands-labs/robots) · [Docs](https://strands-labs.github.io/robots) <br> [![GitHub stars](https://img.shields.io/github/stars/strands-labs/robots?style=flat-square&label=stars)](https://github.com/strands-labs/robots) |

| Resource | Implementation | Research reference |
| --- | --- | --- |
| **Show-Harness: Just a VLM Agent Can Play Robots** | [Code](https://github.com/showlab/Show-Harness) | [Method and release notes](#models--frameworks) |
| **Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence** | [Code](https://github.com/air-embodied-brain/Zetta-Embodiment) | [Method and release notes](#models--frameworks) |
| **Thea — Towards the Harness of Embodied Agents** | [Code](https://github.com/EIT-HAI/Thea) | [Method and release notes](#models--frameworks) |
| **ENPIRE: Agentic Robot Policy Self-Improvement in the Real World** | [Code](https://github.com/NVlabs/ENPIRE) | [Method and release notes](#models--frameworks) |
| **CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation** | [Code](https://github.com/capgym/cap-x) | [Method and release notes](#benchmark-papers) |
| **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models** | [Code](https://github.com/huangwl18/VoxPoser) | [Method and release notes](#models--frameworks) |
| **Code as Policies: Language Model Programs for Embodied Control** | [Code](https://github.com/google-research/google-research/tree/master/code_as_policies) | [Method and release notes](#models--frameworks) |
| **SayCan — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances** | [Code: tabletop simulation](https://github.com/google-research/google-research/tree/master/saycan) | [Method and release notes](#models--frameworks) |
| **REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction** | [Code](https://github.com/real-stanford/reflect) | [Method and release notes](#models--frameworks) |

</details>

<details class="project-group">
<summary><h4>Environment &amp; Sandbox</h4></summary>

<a id="simulation-environments-and-task-suites"></a>

These provide tasks and execution environments for agent research. An environment's inclusion does not mean its standard protocol evaluates tool use, streaming interaction, interruption, or recovery.

| Resource | Useful for | Official source |
| --- | --- | --- |
| **OmniSim** | Newton-based robot simulation with HTTP/JSON and first-party MCP interfaces for scene loading, physics stepping, screenshots, and controller iteration. Public Beta: Windows binaries and Linux source builds; macOS unsupported. ROS 2 integration is partial and sim-to-real transfer is unproven. | [Code](https://github.com/omnilink-tech/omnisim) · [MCP server](https://github.com/omnilink-tech/omnisim/tree/main/packages/omnisim-mcp) · [Protocol](https://github.com/omnilink-tech/omnisim/blob/main/PROTOCOL.md) · [Demos](https://github.com/omnilink-tech/omnisim/blob/main/DEMOS.md) <br> [![GitHub stars](https://img.shields.io/github/stars/omnilink-tech/omnisim?style=flat-square&label=stars)](https://github.com/omnilink-tech/omnisim) |
| **LIBERO** | Manipulation tasks and demonstrations for studying transfer across spatial, object, goal, and task variations | [Code and datasets](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **RoboCasa / RoboCasa365** | Kitchen manipulation, atomic and composite tasks, and demonstration data | [Project, code, and datasets](https://robocasa.ai/) |
| **BEHAVIOR-1K / OmniGibson** | Long-horizon household activities and rich object interactions | [Project and documentation](https://behavior.stanford.edu/) |

[Back to top](#awesome-robot-use-agent-rua)

</details>

<details class="project-group">
<summary><h4>Other Tools</h4></summary>

<a id="robot-interfaces-and-tools"></a>

<a id="projects-and-tools"></a>

Agent-facing interfaces to robot observations, actions, and execution feedback belong here. General-purpose models and libraries belong under [Components](#components); a separate project that wraps one as a robot-use tool is classified by the interface it actually provides.

| Resource | Role | Scope / boundary | Official source |
| --- | --- | --- | --- |
| **ROSA — Robot Operating System Agent** | Natural-language agent for ROS systems | Supports inspection, diagnosis, and robot operation through tools; custom robots need appropriate tools and context. | [Code and documentation](https://github.com/nasa-jpl/rosa) · [Paper](https://arxiv.org/abs/2410.06472) |
| **ROS MCP Server** | MCP interface to ROS | Exposes robot communication and introspection through ROS/rosbridge. Planning and outcome evaluation depend on the connected agent and robot stack. | [Code and documentation](https://github.com/robotmcp/ros-mcp-server) |
| **ros-skill** | Agent Skill with a Python CLI for ROS/ROS 2 | Exposes topic, service, node, parameter, and action commands via rosbridge WebSocket, returning JSON. Planning and outcome interpretation remain with the calling agent; a configured robot and rosbridge are required. | [Code and command reference](https://github.com/lpigeon/ros-skill) <br> [![GitHub stars](https://img.shields.io/github/stars/lpigeon/ros-skill?style=flat-square&label=stars)](https://github.com/lpigeon/ros-skill) |

[OmniSim](#simulation-environments-and-task-suites) also exposes HTTP/JSON and MCP tools for controlling its simulator; its main entry is under simulation environments.

</details>

<details class="project-group">
<summary><h4>Components</h4></summary>

<a id="supporting-components"></a>

Selected building blocks for constructing robot-use tools and agents. These general-purpose components do not, by themselves, provide an agent-facing robot-use interface or a complete observation–action–feedback loop. Their possible roles below are integration suggestions, not claims of a validated robot-use system. We keep this selection focused rather than cataloguing all robotics and vision libraries.

<a id="perception-and-spatial-understanding"></a>

**Perception and spatial understanding**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **Grounded SAM 2** | Text-guided object detection, segmentation, and video tracking | A perception pipeline, not a robot-use interface. Converting masks into robot-frame targets requires depth, calibration, and a control adapter; local-model and cloud-API paths have different dependencies. | [Code and documentation](https://github.com/IDEA-Research/Grounded-SAM-2) |
| **FoundationPose** | 6D object pose estimation and tracking from CAD models or reference images | Requires the corresponding object inputs and inference setup. Its source license limits use to non-commercial research or evaluation. | [Code](https://github.com/NVlabs/FoundationPose) · [License](https://github.com/NVlabs/FoundationPose/blob/main/LICENSE) |
| **ConceptGraphs** | Open-vocabulary 3D scene graphs from posed RGB-D observations | Can support object and spatial-relation queries; requires upstream perception and camera poses. Inclusion does not establish dynamic-world consistency or a complete agent memory system. | [Code and documentation](https://github.com/concept-graphs/concept-graphs) |

<a id="motion-planning-and-control"></a>

**Motion planning and control**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **cuRobo** | GPU-accelerated kinematics, collision checking, and motion generation | Requires CUDA, robot and collision-world configuration, and an execution adapter. Planning a trajectory does not verify task success. | [Code and documentation](https://github.com/NVlabs/curobo) |
| **MPlib** | Lightweight Python motion planning decoupled from ROS | A planning backend for a custom tool; robot models, collision geometry, and execution must be supplied by the application. | [Code and documentation](https://github.com/haosulab/MPlib) |
| **Mink** | MuJoCo-based differential inverse kinematics with joint limits and collision avoidance | A local kinematic solver, not a global task planner or a locomotion policy. The application supplies targets and the control loop. | [Code and documentation](https://github.com/kevinzakka/mink) |

<a id="execution-infrastructure"></a>

**Execution infrastructure**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **BehaviorTree.CPP** | Behavior-tree execution and composition in C++ | An execution backend for application-defined actions and conditions; robot bindings, agent integration, and outcome checks must be supplied separately. | [Code and documentation](https://github.com/BehaviorTree/BehaviorTree.CPP) |

<a id="supporting-policies-and-learning-infrastructure"></a>

**Supporting policies and learning infrastructure**

These resources can supply action models, data workflows, or deployment components. They are listed as foundations rather than complete robot-use agents.

| Resource | Role | Official source |
| --- | --- | --- |
| **OpenVLA** | Vision-language-action model and tools for adaptation to robot manipulation | [Code and model links](https://github.com/openvla/openvla) |
| **openpi** | Physical Intelligence's robot-policy implementations, training utilities, and inference interfaces | [Code and model links](https://github.com/Physical-Intelligence/openpi) |
| **LeRobot** | Robot learning library with policies, datasets, hardware integrations, and training workflows | [Code and documentation](https://github.com/huggingface/lerobot) |

</details>

### Social Demos

<details class="project-group" open>
<summary>Browse 11 demos</summary>

<a id="social-demos-and-evaluations"></a>

Selected X / Twitter posts about GPT-6 Astra, with dates in UTC+8. The 12 demo/evaluation posts are grouped into 11 entries.

[Real robots](#real-robot-demonstrations) · [Simulation](#simulation-demonstrations) · [Perception and reconstruction](#perception-and-reconstruction) · [Research discussions](#articles)

<a id="real-robot-demonstrations"></a>

**Real-robot demonstrations**

| Preview | Name | Date | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://x.com/_wenlixiao/status/2097801944119349455"><img src="https://pbs.twimg.com/amplify_video_thumb/2097801926503243776/img/3MeFRqvS3uGd5_tw.jpg" alt="Wenli Xiao / Tonghe Zhang — video-conditioned robot imitation — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097801926503243776/vid/avc1/1280x720/ub5N-7mSkBw9C_d-.mp4?tag=16) | **Wenli Xiao / Tonghe Zhang — video-conditioned robot imitation** | 2026-09-10 | Real · robot arm | A human demonstration video is supplied to a coding agent to guide a robot arm; authors report first-attempt success on the shown task. <details class="entry-notes"><summary>Sources & notes</summary>[Xiao post](https://x.com/_wenlixiao/status/2097801944119349455) · [Zhang post](https://x.com/TongheZhang01/status/2097801107602911243) · [ENPIRE](https://github.com/NVlabs/ENPIRE). Related posts, not independent replications; no aggregate task success rate supplied.</details> |
| <a href="https://x.com/cdngdev/status/2097339677128982873"><img src="https://pbs.twimg.com/amplify_video_thumb/2097210560727437312/img/GYHkMobXeJU1Ahb-.jpg" alt="Thijs — SO-101 brush painting — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097210560727437312/vid/avc1/1920x1080/QiY_vztFuc1VN4mF.mp4?tag=29) | **Thijs — SO-101 brush painting** | 2026-09-08 | Real · SO-101 | Camera-guided painting of the Golden Gate Bridge, with improvement over attempts. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/cdngdev/status/2097339677128982873) · [Control details](https://x.com/cdngdev/status/2097339677745516710). Author supplied calibration anchors and feedback; roughly one-minute action segments with background monitoring.</details> |
| <a href="https://x.com/ARXrobotics/status/2096328304794210604"><img src="https://pbs.twimg.com/amplify_video_thumb/2096328278588186624/img/4_NW3RqbOTj-1SDO.jpg" alt="ARX — washing-machine knob operation — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096328278588186624/vid/avc1/1022x720/HED2x80GR0g7UCQS.mp4?tag=29) | **ARX — washing-machine knob operation** | 2026-09-06 | Real · ARX | Natural-language instruction to turn a knob in a new room; author says GPT plus a custom control layer, without a VLA. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/ARXrobotics/status/2096328304794210604) · [Author clarification](https://x.com/ARXrobotics/status/2096449872782348475). Case demonstration; repeated success rate and control-layer capabilities remain unverified.</details> |
| <a href="https://x.com/chooi_jeq/status/2096064315115839904"><img src="https://pbs.twimg.com/media/HRa3vJWaEAAQSRT.jpg" alt="Jay Chooi / Robocurve — GPT-6 Astra on robotic manipulation — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096064287764885505/vid/avc1/1920x1080/DS7GMzj6bTNwOinu.mp4?tag=29) | **Jay Chooi / Robocurve — GPT-6 Astra on robotic manipulation** | 2026-09-05 | Real · YAM arms | Inspect Robots 0.58.0 on bimanual YAM arms: **19/20** block-into-bowl completions and **2/20** puzzle insertions. Each turn supplies three camera views plus proprioception; the agent requests absolute end-effector poses through `move_to`. Medium reasoning, a 20-LLM-call budget, and a 25% speed cap. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/chooi_jeq/status/2096064315115839904) · [Report (2026-09-04) and trial records](https://openai.robocurve.org/gpt-6-astra/) · [Framework](https://github.com/robocurve/inspect-robots). Human, non-blind grading and manual resets; trials were not interleaved. Bowl comparisons used different rigs; puzzle used the same rig. The 95% figure applies only to the bowl task.</details> |

<a id="simulation-demonstrations"></a>

**Simulation demonstrations**

| Preview | Name | Date | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://x.com/thermalpastor/status/2097496200631210136"><img src="https://pbs.twimg.com/amplify_video_thumb/2097495575558258688/img/glSoKNk_84aYukL_.jpg" alt="H / thermalpastor — two-robot juggling — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097495575558258688/vid/avc1/1920x1080/_GDd0jHJHResOoJ0.mp4?tag=29) | **H / thermalpastor — two-robot juggling** | 2026-09-09 | Sim · MuJoCo | Two robots exchange balls in MuJoCo, keeping at least one airborne. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/thermalpastor/status/2097496200631210136). Author labels the playback 1× simulation speed; this does not establish real-time model inference or hardware control.</details> |
| <a href="https://x.com/dimentary/status/2097141042214797801"><img src="https://pbs.twimg.com/amplify_video_thumb/2097140400058503168/img/jdcbFn7DHbVRhf7T.jpg" alt="Dmytro Hrybov — dexterous-hand drawing — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097140400058503168/vid/avc1/1600x900/KMym95lPHX-kh0oc.mp4?tag=29) | **Dmytro Hrybov — dexterous-hand drawing** | 2026-09-08 | Sim · MuJoCo | A generated MuJoCo setup and controller use a Kinova Gen3 arm and Shadow Hand to draw a dove through pen–paper contact. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dimentary/status/2097141042214797801) · [Contact and timing details](https://x.com/dimentary/status/2097141323883327933). Two-finger grip despite a five-finger hand; video sped up 4×.</details> |
| <a href="https://x.com/dimentary/status/2096785235795181900"><img src="https://pbs.twimg.com/amplify_video_thumb/2096785124478390272/img/IGBjIu069D7LvrCx.jpg" alt="Dmytro Hrybov — six-legged, dual-arm transport — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096785124478390272/vid/avc1/1280x720/igU4w02KTPNMZ6yj.mp4?tag=29) | **Dmytro Hrybov — six-legged, dual-arm transport** | 2026-09-07 | Sim · MuJoCo | Building a MuJoCo embodiment and controller that move objects between tables. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dimentary/status/2096785235795181900). Simulation demonstration; an unusual morphology alone does not establish out-of-distribution generalization.</details> |
| <a href="https://x.com/Hakim_Fang/status/2096565038744252613"><img src="https://pbs.twimg.com/amplify_video_thumb/2096564871756451840/img/cnmv55yniWL6P6ET.jpg" alt="Hakim Phun — RoboDojo tasks — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096564871756451840/vid/avc1/960x720/F4hJJa9CwgxKMbsS.mp4?tag=14) | **Hakim Phun — RoboDojo tasks** | 2026-09-06 | Sim · RoboDojo | Selected robot-simulation task demonstrations. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/Hakim_Fang/status/2096565038744252613). The collection records the author's caveat that inference pauses were removed and a full quantitative evaluation was not yet available.</details> |

<a id="perception-and-reconstruction"></a>

**Perception and reconstruction**

These are supporting capabilities for robot-use workflows, rather than direct evidence of a complete robot-control agent.

| Preview | Name | Date | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://x.com/Lingxiao234/status/2097717020540481630"><img src="https://pbs.twimg.com/amplify_video_thumb/2097716973899780096/img/IgOqn00YQoSzMzG7.jpg" alt="Lingxiao Guo — video-to-Wuji-hand retargeting — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097716973899780096/vid/avc1/1920x1080/gsFWFgb-G3egibZw.mp4?tag=16) | **Lingxiao Guo — video-to-Wuji-hand retargeting** | 2026-09-10 | Video · retargeting | Real2Sim and motion retargeting from two videos, without supplied states or actions. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/Lingxiao234/status/2097717020540481630). Execution environment, hardware deployment, repeatability, and this demo's code release remain unverified; the separate Real2Sim repository is not assumed to reproduce this result.</details> |
| <a href="https://x.com/Lingxiao234/status/2096992059731443923"><img src="https://pbs.twimg.com/amplify_video_thumb/2096992032623607809/img/nIpBp2XGYS-V7j0r.jpg" alt="Lingxiao Guo — robot-demonstration Real2Sim — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096992032623607809/vid/avc1/1080x1080/AHW_1iefmViMhqhJ.mp4?tag=16) | **Lingxiao Guo — robot-demonstration Real2Sim** | 2026-09-08 | Real2Sim · MuJoCo / Blender | Multi-view RGB and robot actions used for calibration, asset reconstruction, physical-parameter fitting, MuJoCo simulation, and Blender rendering. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/Lingxiao234/status/2096992059731443923) · [Code and limitations](https://github.com/lingxiao-guo/GPT6-real2sim). Released examples include placement errors, approximate alignment, and failed contact-only microphone attachment; visual agreement is not validated dynamics recovery.</details> |
| <a href="https://x.com/kstonekuan/status/2097119396032569555"><img src="https://pbs.twimg.com/amplify_video_thumb/2097117752603627520/img/4ir_oaxEq6wuJD0a.jpg" alt="Kingston Kuan — egocentric 3D hand pose — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097117752603627520/vid/avc1/1920x1472/RxVQsJKOJzKy5Tht.mp4?tag=29) | **Kingston Kuan — egocentric 3D hand pose** | 2026-09-08 | Video · hand pose | Comparison against MediaPipe using the same output schema, including gloved hands. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/kstonekuan/status/2097119396032569555). Author reports about **3 min/frame** for Astra at high reasoning effort versus **20 ms/frame** for MediaPipe; no aggregate ground-truth accuracy metric supplied.</details> |

[Back to top](#awesome-robot-use-agent-rua)

</details>

## Benchmarks

<a id="benchmarks-and-environments"></a>

<a id="agent-benchmarks-and-evaluation-frameworks"></a>

| Preview | Name | Year | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://embodied-agent-interface.github.io/"><img src="https://embodied-agent-interface.github.io/website/img/teaser.png" alt="EAI official overview" width="200"></a> | **Embodied Agent Interface (EAI)** | 2024 | OmniGibson / VirtualHome | Goal interpretation, subgoal decomposition, action sequencing, and transition modeling <details class="entry-notes"><summary>Sources & notes</summary>[Code and documentation](https://github.com/embodied-agent-interface/embodied-agent-interface)<br>Useful for identifying decision-making errors; symbolic module evaluation should be distinguished from end-to-end physical execution.</details> |
| <a href="https://embodiedbench.github.io/"><img src="https://arxiv.org/html/2502.09560v3/embodied_overview_new.png" alt="EmbodiedBench paper overview" width="200"></a> | **EmbodiedBench** | 2025 | AI2-THOR / Habitat / CoppeliaSim | Vision-driven embodied agents across high- and low-level tasks <details class="entry-notes"><summary>Sources & notes</summary>[Code and documentation](https://github.com/EmbodiedBench/EmbodiedBench)<br>Provides multiple environments and capability-oriented evaluation, including navigation and manipulation.</details> |
| <a href="https://openai.robocurve.org/gpt-6-astra/"><img src="https://pbs.twimg.com/media/HRa3vJWaEAAQSRT.jpg" alt="GPT-6 Astra evaluation using Inspect Robots" width="200"></a> | **Inspect Robots (Robocurve)** | 2026 (report) | Real robots · YAM in linked report | Evaluation framework connecting LLM-agent/VLA policies, embodiments, benchmarks, and auditable logs <details class="entry-notes"><summary>Sources & notes</summary>[Code](https://github.com/robocurve/inspect-robots) · [Docs](https://docs.inspectrobots.org/) · [GPT-6 Astra report](https://openai.robocurve.org/gpt-6-astra/) <br> [![GitHub stars](https://img.shields.io/github/stars/robocurve/inspect-robots?style=flat-square&label=stars)](https://github.com/robocurve/inspect-robots)<br>Alpha software. Robocurve's GPT-6 Astra report uses version 0.58.0 on YAM arms; the framework and that particular evaluation are distinct. See the [trial results and limitations](#real-robot-demonstrations).</details> |
| <a href="https://capgym.github.io/"><img src="https://arxiv.org/html/2603.22435v1/assets/figures/splash_figure_v3.png" alt="CaP-X paper overview: CaP-Bench and CaP-Gym" width="200"></a> | **CaP-X / CaP-Bench** | 2026 | Robosuite / LIBERO-PRO / BEHAVIOR | Evaluates robot-control coding agents across API abstraction levels, single-/multi-turn interaction, and visual grounding <details class="entry-notes"><summary>Sources & notes</summary>[Paper](https://arxiv.org/abs/2603.22435) · [Code](https://github.com/capgym/cap-x) · [Project](https://capgym.github.io/)<br>Preview: Figure 1 of the paper.</details> |

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

## Star History

<a href="https://www.star-history.com/?repos=kairunwen%2FAwesome-Robot-Use-Agent&amp;type=date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=kairunwen/Awesome-Robot-Use-Agent&amp;type=date&amp;theme=dark&amp;legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=kairunwen/Awesome-Robot-Use-Agent&amp;type=date&amp;legend=top-left" />
    <img alt="Awesome Robot Use Agent star history chart" src="https://api.star-history.com/chart?repos=kairunwen/Awesome-Robot-Use-Agent&amp;type=date&amp;legend=top-left" width="100%" />
  </picture>
</a>
