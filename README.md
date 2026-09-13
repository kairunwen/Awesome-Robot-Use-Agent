<div align="center">

<img src="assets/logo.png" alt="RUA logo: a robotic hand gently petting a happy cat" width="160" />

# Awesome Robot Use Agent (RUA)

[![Awesome](https://img.shields.io/badge/Awesome-List-111111.svg?style=for-the-badge&labelColor=000000&logo=awesomelists&logoColor=white)](https://awesome.re) [![Website](https://img.shields.io/badge/Website-Visit-111111.svg?style=for-the-badge&labelColor=000000&logo=githubpages&logoColor=white)](https://kairunwen.github.io/Awesome-Robot-Use-Agent/) [![Resources](https://img.shields.io/badge/Resources-96-111111.svg?style=for-the-badge&labelColor=000000&logo=readthedocs&logoColor=white)](#contents) [![Demo](https://img.shields.io/badge/Demo-31-111111.svg?style=for-the-badge&labelColor=000000&logo=x&logoColor=white)](#social-demos)
<br>
[![Tools](https://img.shields.io/badge/Tools-21-111111.svg?style=for-the-badge&labelColor=000000&logo=ros&logoColor=white)](#tool-box) [![PRs welcome](https://img.shields.io/badge/PRs-Welcome-111111.svg?style=for-the-badge&labelColor=000000&logo=git&logoColor=white)](#contributing) [![GitHub Stars](https://img.shields.io/github/stars/kairunwen/Awesome-Robot-Use-Agent?style=for-the-badge&label=Stars&labelColor=000000&color=111111&logo=github&logoColor=white)](https://github.com/kairunwen/Awesome-Robot-Use-Agent) [![License: MIT](https://img.shields.io/badge/License-MIT-111111.svg?style=for-the-badge&labelColor=000000)](LICENSE)

[Articles](#articles) · [Papers](#papers) · [Projects](#projects) · [Benchmarks](#benchmarks-1) · [Social Demos](#social-demos)

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
    - [Tool Box](#tool-box)
  - [Social Demos](#social-demos)
- [Benchmarks](#benchmarks-1)

[Contributing](#contributing) · [Citation](#citation)

## Getting started

Robot-use agents turn goals into robot actions through skills, generated code, and perception/control APIs.

- **Read:** [Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) — an introduction to the idea.
- **Build:** [ROS MCP Server](https://github.com/robotmcp/ros-mcp-server) for ROS integration; [Strands Robots](https://github.com/strands-labs/robots) for a simulation workflow.
- **Watch:** [Social Demos](#social-demos) — community demonstrations.
- **Evaluate:** [CaP-X / CaP-Bench](https://github.com/capgym/cap-x) · [RoboCurve](https://robocurve.org/).

## Articles

<a id="blogs-and-demos"></a>
<a id="blogs-and-perspectives"></a>

- **[Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html)** — Phillip Isola · 2026-09-07 · **Perspective**. General-purpose AI agents using robots through sensor and actuator APIs, with discussion of deployment, latency, and reliability. [Author post](https://x.com/phillip_isola/status/2097045136051933566); discusses agents including Claude, rather than a GPT-6-only evaluation.

- **[Claude plays robotics](https://www.anthropic.com/research/claude-plays-robotics)** — Anthropic · 2026-07-09 · **Research article**. Compares direct motor commands, generated controllers, pretrained-policy supervision, and RL training across control, locomotion, and manipulation tasks. Author-reported results show that robot embodiment and control interface strongly affect performance. Direct-control simulations pause between model calls; physical Go2 explorations should be distinguished from simulated benchmark results.

- **[Gemini Robotics ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/)** — Google DeepMind · **Model overview**. Describes embodied reasoning for multi-step planning, tool use, success tracking, and multi-robot coordination. ER 2 provides high-level decisions while a connected VLA handles motor execution; the page presents developer-reported capabilities and evaluations.

- **[NVIDIA brings agents to life with DGX Spark and Reachy Mini](https://huggingface.co/blog/nvidia-reachy-mini)** — Hugging Face & NVIDIA · 2026-01-05 · **Technical tutorial**. Connects Nemotron reasoning and vision models, NeMo Agent Toolkit, and Pipecat to Reachy Mini for voice, camera input, and robot behaviors. Describes ReAct tool calling and Python interfaces for hardware or simulation; focuses on a desktop interactive robot rather than general manipulation.

## Papers

Paper references are grouped by contribution. Dates refer to first arXiv release unless noted. Method summaries reflect author reports; code, weights, and complete reproduction are separate release claims. Implementation entries and benchmark descriptions are cross-linked rather than counted as additional distinct works.

<a id="research-papers"></a>

### Surveys

| Date | Work | Focus | Sources |
| --- | --- | --- | --- |
| 2026-09 | **Survey on Multimodal Embodied Agents: A Unified Capability-centric Perspective from Computer-Use to Robot-Use** | Unifies computer-use and robot-use through PAPAV: Perceive, Anticipate, Plan, Act, and Verify; examines physical constraints and benchmark coverage. | [Paper](https://github.com/showlab/Awesome-Multimodal-Embodied-Agent/blob/main/assets/Awesome_Multimodal_Embodied_Agent.pdf) · [Repository](https://github.com/showlab/Awesome-Multimodal-Embodied-Agent) |
| 2025-10 | **A Survey on Agentic Multimodal Large Language Models** | Broader multimodal-agent survey covering reasoning, reflection, memory, tool invocation, and interaction with physical environments, including embodied AI applications. | [Paper](https://arxiv.org/abs/2510.10991) · [Repository](https://github.com/HJYao00/Awesome-Agentic-MLLMs) |
| 2025-08 | **Towards Embodied Agentic AI: Review and Classification of LLM- and VLM-Driven Robot Autonomy and Interaction** | Classifies how LLM/VLM agents integrate with robot APIs, ROS middleware, and orchestration frameworks; covers planning, tool calling, agent roles, and practical robotics toolkits. | [Paper](https://arxiv.org/abs/2508.05294) |
| 2024-04 | **A Survey on Integration of Large Language Models with Intelligent Robots** | LLM integration across communication, perception, planning, and control. | [Paper](https://arxiv.org/abs/2404.09228) |

### Models & Frameworks

<a id="embodied-harnesses-and-policy-orchestration"></a>
<a id="planning-and-code-as-policies"></a>
<a id="execution-feedback-and-recovery"></a>

| Date | Work | Paper | Code | Mechanism / release notes |
| --- | --- | --- | --- | --- |
| 2026-09 | **Show-Harness: Just a VLM Agent Can Play Robots** <br> [Project and demos](https://showlab.github.io/Show-Harness/) · [Model adapters](https://huggingface.co/showlab/Show-Harness-VLMs) · [Data](https://huggingface.co/datasets/showlab/Show-Harness-Data) | [Paper](https://arxiv.org/abs/2609.10522) | [Code](https://github.com/showlab/Show-Harness) <br> [![GitHub stars](https://img.shields.io/github/stars/showlab/Show-Harness?style=flat-square&label=stars)](https://github.com/showlab/Show-Harness) | VLMs select discrete, incremental action units grounded by robot-specific interpreters. <details class="entry-notes"><summary>Release & deployment</summary>Includes planning, action-history and recovery plugins, GUMI demonstration collection, and fine-tuning tools. Franka/Piper and simulator adapters require their documented dependencies and site configuration; not independently deployed here.</details> |
| 2026-08 | **Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence** <br> [Project](https://air-embodied-brain.github.io/zetta/) | [Paper](https://arxiv.org/abs/2608.16590) | [Code](https://github.com/air-embodied-brain/Zetta-Embodiment) <br> [![GitHub stars](https://img.shields.io/github/stars/air-embodied-brain/Zetta-Embodiment?style=flat-square&label=stars)](https://github.com/air-embodied-brain/Zetta-Embodiment) | Keeps the base policy frozen while developing runtime critics and recovery skills through execution, diagnosis, and gated updates. <details class="entry-notes"><summary>Release notes</summary>The separate `air-embodied-brain/zetta` repository hosts the project website.</details> |
| 2026-08 | **Thea — Towards the Harness of Embodied Agents** <br> [Project](https://eit-hai.github.io/thea/) | [Paper](https://arxiv.org/abs/2608.11246) | [Code](https://github.com/EIT-HAI/Thea) <br> [![GitHub stars](https://img.shields.io/github/stars/EIT-HAI/Thea?style=flat-square&label=stars)](https://github.com/EIT-HAI/Thea) | Wraps robot capabilities as callable tools, maintains symbolic scene context, and evaluates action termination, success, and failure causes. <details class="entry-notes"><summary>Release & deployment</summary>Public runtime and interfaces; robot/simulator deployment requires concrete adapters and capabilities.</details> |
| 2026-07 | **RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning** | [Paper](https://arxiv.org/abs/2607.18060) | Unverified | Uses execution memory to route among heterogeneous policies and a Memory Bridge to improve handoffs between policies. |
| 2026-06 | **ASPIRE: Agentic /Skills Discovery for Robotics** <br> [Project](https://research.nvidia.com/labs/gear/aspire/) | [Paper](https://arxiv.org/abs/2607.00272) | [Code](https://github.com/NVlabs/ASPIRE) <br> [![GitHub stars](https://img.shields.io/github/stars/NVlabs/ASPIRE?style=flat-square&label=stars)](https://github.com/NVlabs/ASPIRE) | Refines code-as-policy programs using multimodal execution traces, failure diagnosis, repair validation, a reusable skill library, and evolutionary search. <details class="entry-notes"><summary>Release & deployment</summary>Provides simulation workflows and real-robot transfer code. Behaviors remain bounded by predefined perception, planning, and control primitives; real-world deployment requires success detection, resets, safety monitoring, and calibration. First arXiv submission: 2026-06-30.</details> |
| 2026-06 | **Guava: An Effective and Universal Harness for Embodied Manipulation** | [Paper](https://arxiv.org/abs/2606.18363) | Unverified | Studies iterative perception–reasoning–action, semantic action abstractions, and multimodal observations; also describes distillation into a smaller agent model. <details class="entry-notes"><summary>Release notes</summary>Checkpoint availability also unverified.</details> |
| 2026-06 | **ENPIRE: Agentic Robot Policy Self-Improvement in the Real World** <br> [Project](https://research.nvidia.com/labs/gear/enpire/) | [Paper](https://arxiv.org/abs/2606.19980) | [Code](https://github.com/NVlabs/ENPIRE) <br> [![GitHub stars](https://img.shields.io/github/stars/NVlabs/ENPIRE?style=flat-square&label=stars)](https://github.com/NVlabs/ENPIRE) | Connects scene reset, policy execution, outcome verification, and experiment refinement so coding agents can improve policies through physical trials. <details class="entry-notes"><summary>Deployment notes</summary>Deployment requires calibrated stations and task-specific reset and verification functions.</details> |
| 2023-07 | **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models** <br> [Project and demos](https://voxposer.github.io/) | [Paper](https://arxiv.org/abs/2307.05973) | [Code](https://github.com/huangwl18/VoxPoser) <br> [![GitHub stars](https://img.shields.io/github/stars/huangwl18/VoxPoser?style=flat-square&label=stars)](https://github.com/huangwl18/VoxPoser) | Uses generated code and visual grounding to construct 3D value maps for motion planning; the generated program can be reevaluated with visual feedback. <details class="entry-notes"><summary>Release & evidence</summary>The public repository provides an RLBench demo; it excludes the full perception pipeline used in real-robot experiments.</details> |
| 2023-06 | **REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction** <br> [Project](https://robot-reflect.github.io/) | [Paper](https://arxiv.org/abs/2306.15724) | [Code](https://github.com/real-stanford/reflect) <br> [![GitHub stars](https://img.shields.io/github/stars/real-stanford/reflect?style=flat-square&label=stars)](https://github.com/real-stanford/reflect) | Summarizes multisensory execution history, explains failures, and conditions a planner on those explanations to produce corrective actions. |
| 2022-09 | **Code as Policies: Language Model Programs for Embodied Control** <br> [Project and demos](https://code-as-policies.github.io/) · [Blog](https://research.google/blog/robots-that-write-their-own-code/) | [Paper](https://arxiv.org/abs/2209.07753) | [Code](https://github.com/google-research/google-research/tree/master/code_as_policies) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Generates programs that compose perception outputs, control APIs, and feedback loops. |
| 2022-07 | **Inner Monologue: Embodied Reasoning through Planning with Language Models** <br> [Project and demos](https://innermonologue.github.io/) | [Paper](https://arxiv.org/abs/2207.05608) | Unverified | Feeds success detection, scene descriptions, and human feedback into language-based planning; demonstrates replanning and responses to changed goals. |
| 2022-04 | **SayCan — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances** <br> [Project](https://say-can.github.io/) | [Paper](https://arxiv.org/abs/2204.01691) | [Code: tabletop simulation](https://github.com/google-research/google-research/tree/master/saycan) <br> [![GitHub stars](https://img.shields.io/github/stars/google-research/google-research?style=flat-square&label=stars)](https://github.com/google-research/google-research) | Combines language-model skill scoring with affordance/value estimates to select feasible robot behaviors. |

### Datasets

Data for agent action selection, tool use, planning, and execution feedback, with broader robot demonstrations included as supporting resources. Dates follow the associated paper; public downloads, paper-described training data, and data surveys are distinguished below.

| Date | Work | Focus | Sources |
| --- | --- | --- | --- |
| 2026-09 | **Show-Harness Data** | Observation–action-unit demonstrations across Franka, AgileX, RoboLab, and ManiSkill for training visual robot agents. Primarily action-selection data, not a complete reasoning and failure-recovery log. | **Public data:** [Dataset](https://huggingface.co/datasets/showlab/Show-Harness-Data) · [Paper](https://arxiv.org/abs/2609.10522) |
| 2026-07 | **Data Pyramid for Embodied Manipulation: A Survey** | Surveys real-robot, UMI-style, egocentric/exocentric, simulation, and general vision-language data; examines data mixtures, robot alignment, and gaps in failure and recovery data. | **Data survey:** [Paper](https://arxiv.org/abs/2607.24744) · [Resource list](https://github.com/worldbench/awesome-embodied-data-pyramid) |
| 2026-06 | **Guava-Agent-4B training data** | Simulated trajectories with observations, tool calls, execution feedback, and recovery from injected errors. The paper reports 1,934 trajectories, including 743 recovery trajectories. | **Paper-described; data download unverified:** [Construction and filtering](https://arxiv.org/html/2606.18363v1#A1) |
| 2025-06 | **RoboCerebra: A Large-scale Benchmark for Long-horizon Robotic Manipulation Evaluation** | Long-horizon simulation demonstrations with subtask annotations, disturbances, and memory-dependent tasks. Supports hierarchical planning and execution evaluation; not a dedicated tool-call trace dataset. | **Public data:** [Dataset](https://huggingface.co/datasets/qiukingballball/RoboCerebra) · [Paper](https://arxiv.org/abs/2506.06677) · [Project](https://robocerebra.github.io/) |

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

Code links and usage restrictions are recorded per entry. Research papers and their code links are listed together in [Papers](#papers); this section focuses on standalone tools, frameworks, environments, and demos. Check each repository, model, and dataset license before reuse.

<details class="project-group">
<summary><h4>Systems &amp; Frameworks</h4></summary>

<a id="agents-and-frameworks"></a>

<a id="agent-runtimes-and-orchestration"></a>

| Resource | Role | Interface | Deployment & evidence | Official source |
| --- | --- | --- | --- | --- |
| **AgenticROS** | ROS 2 capability and mission runtime | Named skills via MCP and agent adapters | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Mission graphs pass step outputs and support failure branches.</p><p><strong>Setup:</strong> ROS 2 capabilities and mission definitions.</p><p><strong>Limits:</strong> The built-in natural-language mission compiler is rule-based, not an LLM planner.</p></details> | [Code](https://github.com/agenticros/agenticros) · [Docs](https://github.com/agenticros/agenticros#architecture) <br> [![GitHub stars](https://img.shields.io/github/stars/agenticros/agenticros?style=flat-square&label=stars)](https://github.com/agenticros/agenticros) |
| **DimOS** | Robot runtime for perception, spatial memory, navigation, and agent skills | Python, CLI, and MCP | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Replay, simulation, and hardware workflows.</p><p><strong>Setup:</strong> Dependencies for the selected workflow and hardware integration.</p><p><strong>Limits:</strong> Pre-release Beta; individual hardware integrations range from stable to experimental.</p></details> | [Code](https://github.com/dimensionalOS/dimos) · [Docs](https://docs.dimensionalos.com) <br> [![GitHub stars](https://img.shields.io/github/stars/dimensionalOS/dimos?style=flat-square&label=stars)](https://github.com/dimensionalOS/dimos) |
| **EmbodiedAgents** | ROS 2 intelligence and component orchestration in EMOS | Event-driven component graphs; local or hosted models | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Model, memory, and component events.</p><p><strong>Setup:</strong> Relevant robot components for motion.</p><p><strong>Limits:</strong> The visual-question-answering quickstart alone does not establish a complete robot-control loop.</p></details> | [Code](https://github.com/automatika-robotics/embodied-agents) · [Docs](https://automatika-robotics.github.io/embodied-agents/) <br> [![GitHub stars](https://img.shields.io/github/stars/automatika-robotics/embodied-agents?style=flat-square&label=stars)](https://github.com/automatika-robotics/embodied-agents) |
| **RAI** | ROS 2 agent framework for perception, speech, and evaluation | Robot-specific tools and robot descriptions | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Simulation integrations and rai_bench.</p><p><strong>Setup:</strong> Robot-specific tools and configuration.</p><p><strong>Limits:</strong> The README lists rai_finetune as unfinished.</p></details> | [Code](https://github.com/RobotecAI/rai) · [Docs](https://robotecai.github.io/rai/) · [Paper](https://arxiv.org/abs/2505.07532) <br> [![GitHub stars](https://img.shields.io/github/stars/RobotecAI/rai?style=flat-square&label=stars)](https://github.com/RobotecAI/rai) |
| **Strands Robots** | Robot tools and policy execution for Strands Agents | Robot tool wrapping simulation or hardware | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Policy execution, recording, and training integrations.</p><p><strong>Setup:</strong> MuJoCo by default; real hardware is opt-in.</p><p><strong>Limits:</strong> Simulator asset coverage does not establish equivalent hardware support.</p></details> | [Code](https://github.com/strands-labs/robots) · [Docs](https://strands-labs.github.io/robots) <br> [![GitHub stars](https://img.shields.io/github/stars/strands-labs/robots?style=flat-square&label=stars)](https://github.com/strands-labs/robots) |

</details>

<details class="project-group">
<summary><h4>Environment &amp; Sandbox</h4></summary>

<a id="simulation-environments-and-task-suites"></a>

These provide tasks, execution environments, and scene reconstruction workflows for agent research. Visual replay and contact simulation are distinguished per entry. An environment's inclusion does not mean its standard protocol evaluates tool use, streaming interaction, interruption, or recovery.

| Resource | Useful for | Official source |
| --- | --- | --- |
| **OmniSim** | Newton-based robot simulation with HTTP/JSON and first-party MCP interfaces for scene loading, physics stepping, screenshots, and controller iteration. <details class="entry-notes"><summary>Deployment & limits</summary>Public Beta: Windows binaries and Linux source builds; macOS unsupported. ROS 2 integration is partial and sim-to-real transfer is unproven.</details> | [Code](https://github.com/omnilink-tech/omnisim) · [MCP server](https://github.com/omnilink-tech/omnisim/tree/main/packages/omnisim-mcp) · [Protocol](https://github.com/omnilink-tech/omnisim/blob/main/PROTOCOL.md) · [Demos](https://github.com/omnilink-tech/omnisim/blob/main/DEMOS.md) <br> [![GitHub stars](https://img.shields.io/github/stars/omnilink-tech/omnisim?style=flat-square&label=stars)](https://github.com/omnilink-tech/omnisim) |
| **SimFoundry** | **Simulation scene generation.** Modular video-to-simulation pipeline for object reconstruction, physical scene compilation, digital cousin variations, and task proposals in OmniGibson. <details class="entry-notes"><summary>Deployment & limits</summary>Requires Linux, an NVIDIA GPU, model access, and Gemini service access. The release includes rigid-body and articulation generation; automated background generation and robotics data generation, training, and evaluation are listed as coming soon.</details> | [Code and documentation](https://github.com/NVlabs/SimFoundry) <br> [![GitHub stars](https://img.shields.io/github/stars/NVlabs/SimFoundry?style=flat-square&label=stars)](https://github.com/NVlabs/SimFoundry) |
| **DexGPT** | **Contact simulation.** Reconstructs manipulation from a monocular GIF, retargets motion to two Sharpa Wave hands, and provides MuJoCo contact rollouts, recorded states, and audit reports. <details class="entry-notes"><summary>Deployment & limits</summary>Task-specific experimental reconstruction with assumed scale and depth. The repository reports unmet physical validation criteria; exact replay uses a bundled fitted grasp seed.</details> | [Code and documentation](https://github.com/Hu-xiao-max/dexgpt) <br> [![GitHub stars](https://img.shields.io/github/stars/Hu-xiao-max/dexgpt?style=flat-square&label=stars)](https://github.com/Hu-xiao-max/dexgpt) |
| **Real2Sim_GPT6_ASTRA** | **Visual reconstruction / replay.** Reconstructs a robot workspace from three RGB views and provides editable Blender scenes, motion replay, rendering, and geometric validation scripts. <details class="entry-notes"><summary>Deployment & limits</summary>Visual approximation without measured calibration, depth, joint states, or dynamics. Input RGB frames are not bundled; reproduction requires those inputs, Blender, and FFmpeg.</details> | [Code and documentation](https://github.com/hku-sail/Real2Sim_GPT6_ASTRA) <br> [![GitHub stars](https://img.shields.io/github/stars/hku-sail/Real2Sim_GPT6_ASTRA?style=flat-square&label=stars)](https://github.com/hku-sail/Real2Sim_GPT6_ASTRA) |
| **SIMPLE** | Humanoid locomotion-and-manipulation simulation with AMO/SONIC whole-body controllers, teleoperation and motion-planning data collection, and client–server policy evaluation. <details class="entry-notes"><summary>Deployment & limits</summary>Built on Isaac Sim 4.5 and MuJoCo 3.3; requires Ubuntu 22.04, an RTX-class NVIDIA GPU, task assets, and matching policy checkpoints. Its documented evaluations focus on learned policies; an LLM tool-use agent requires a separate integration.</details> | [Code](https://github.com/physical-superintelligence-lab/SIMPLE) · [Docs](https://psi-lab.ai/SIMPLE/docs) · [Paper](https://arxiv.org/abs/2606.08278) <br> [![GitHub stars](https://img.shields.io/github/stars/physical-superintelligence-lab/SIMPLE?style=flat-square&label=stars)](https://github.com/physical-superintelligence-lab/SIMPLE) |
| **LIBERO** | Manipulation tasks and demonstrations for studying transfer across spatial, object, goal, and task variations | [Code and datasets](https://github.com/Lifelong-Robot-Learning/LIBERO) |
| **RoboCasa / RoboCasa365** | Kitchen manipulation, atomic and composite tasks, and demonstration data | [Project, code, and datasets](https://robocasa.ai/) |
| **BEHAVIOR-1K / OmniGibson** | Long-horizon household activities and rich object interactions | [Project and documentation](https://behavior.stanford.edu/) |

[Back to top](#awesome-robot-use-agent-rua)

</details>

<details class="project-group">
<summary><h4>Tool Box</h4></summary>

<a id="components"></a>
<a id="supporting-components"></a>

Reusable tools and libraries for perception, grasp generation, motion planning, execution, and robot learning. Connect them through robot APIs to build an observation–action–feedback loop; each entry describes its capabilities and integration requirements.

<a id="perception-and-spatial-understanding"></a>

**Perception and spatial understanding**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **Grounded SAM 2** | Text-guided object detection, segmentation, and video tracking | A perception pipeline, not a robot-use interface. Converting masks into robot-frame targets requires depth, calibration, and a control adapter; local-model and cloud-API paths have different dependencies. | [Code and documentation](https://github.com/IDEA-Research/Grounded-SAM-2) |
| **SAM 3** | Text- and visual-prompted segmentation for images and video | Integrated in ASPIRE and ENPIRE for object localization; robot-frame targets require depth and calibration. Model checkpoints require access approval. | [Code and models](https://github.com/facebookresearch/sam3) · [ASPIRE integration](https://github.com/NVlabs/ASPIRE/blob/main/aspire/sim/docs/configuration.md) |
| **FoundationPose** | 6D object pose estimation and tracking from CAD models or reference images | Requires the corresponding object inputs and inference setup. Its source license limits use to non-commercial research or evaluation. | [Code](https://github.com/NVlabs/FoundationPose) · [License](https://github.com/NVlabs/FoundationPose/blob/main/LICENSE) |
| **BundleSDF** | 6-DoF tracking and 3D reconstruction of unknown objects from RGB-D video | Requires RGB-D observations and an initial object mask. ASPIRE and ENPIRE include tracking-service integrations; deployment still requires camera calibration and runtime dependencies. | [Code](https://github.com/NVlabs/BundleSDF) · [ENPIRE integration](https://github.com/NVlabs/ENPIRE/blob/main/enpire/env/forge/tools/vision/serve_bundlesdf.py) |
| **ConceptGraphs** | Open-vocabulary 3D scene graphs from posed RGB-D observations | Can support object and spatial-relation queries; requires upstream perception and camera poses. Inclusion does not establish dynamic-world consistency or a complete agent memory system. | [Code and documentation](https://github.com/concept-graphs/concept-graphs) |

<a id="grasp-generation"></a>

**Grasp generation**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **Contact-GraspNet** | Generates 6-DoF grasp candidates from scene point clouds | ASPIRE uses a PyTorch port as a default simulation service. Grasp candidates still require robot-specific feasibility checks, motion planning, and execution. | [Official code](https://github.com/NVlabs/contact_graspnet) · [PyTorch port used by ASPIRE](https://github.com/elchun/contact_graspnet_pytorch) · [ASPIRE setup](https://github.com/NVlabs/ASPIRE/blob/main/aspire/sim/README.md) |
| **AnyGrasp** | 6-DoF grasp-pose detection and tracking from RGB-D observations | Default grasp backend in ENPIRE’s public pickup example; optional in ASPIRE’s real-robot stack. The SDK, checkpoint, and license must be obtained separately. | [SDK and documentation](https://github.com/graspnet/anygrasp_sdk) · [ENPIRE example](https://github.com/NVlabs/ENPIRE/blob/main/enpire/env/examples/10_real_object_pick/README.md) |

<a id="motion-planning-and-control"></a>

**Motion planning and control**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **cuRobo** | GPU-accelerated kinematics, collision checking, and motion generation | Requires CUDA, robot and collision-world configuration, and an execution adapter. Planning a trajectory does not verify task success. | [Code and documentation](https://github.com/NVlabs/curobo) |
| **PyRoki** | JAX-based robot kinematic optimization, inverse kinematics, and configurable collision costs | A default ASPIRE simulation service and an ENPIRE planning backend. Collision handling depends on the integration; ENPIRE’s documented RoboCasa IK path has no scene collision checking. | [Code and documentation](https://github.com/chungmin99/pyroki) · [ASPIRE integration](https://github.com/NVlabs/ASPIRE/blob/main/aspire/sim/docs/configuration.md) |
| **MPlib** | Lightweight Python motion planning decoupled from ROS | A planning backend for a custom tool; robot models, collision geometry, and execution must be supplied by the application. | [Code and documentation](https://github.com/haosulab/MPlib) |
| **Mink** | MuJoCo-based differential inverse kinematics with joint limits and collision avoidance | A local kinematic solver, not a global task planner or a locomotion policy. The application supplies targets and the control loop. | [Code and documentation](https://github.com/kevinzakka/mink) |

<a id="execution-infrastructure"></a>

**Execution infrastructure**

| Resource | Capability | Integration boundary | Official source |
| --- | --- | --- | --- |
| **mjbatch** | Batched MuJoCo simulation on CPU through Python, with shared array access to states and controls and per-simulation model parameters; includes MPC, RL, system identification, and hardware co-design examples | A simulation backend for candidate-action rollouts and controller experiments; agent orchestration, tasks, and outcome evaluation must be supplied by the application. | [Code and documentation](https://github.com/kevinzakka/mjbatch) <br> [![GitHub stars](https://img.shields.io/github/stars/kevinzakka/mjbatch?style=flat-square&label=stars)](https://github.com/kevinzakka/mjbatch) |
| **BehaviorTree.CPP** | Behavior-tree execution and composition in C++ | An execution backend for application-defined actions and conditions; robot bindings, agent integration, and outcome checks must be supplied separately. | [Code and documentation](https://github.com/BehaviorTree/BehaviorTree.CPP) |

<a id="supporting-policies-and-learning-infrastructure"></a>

**Supporting policies and learning infrastructure**

These resources can supply action models, data workflows, or deployment components. They are listed as foundations rather than complete robot-use agents.

| Resource | Role | Official source |
| --- | --- | --- |
| **OpenVLA** | Vision-language-action model and tools for adaptation to robot manipulation | [Code and model links](https://github.com/openvla/openvla) |
| **openpi** | Physical Intelligence's robot-policy implementations, training utilities, and inference interfaces | [Code and model links](https://github.com/Physical-Intelligence/openpi) |
| **LeRobot** | Robot learning library with policies, datasets, hardware integrations, and training workflows | [Code and documentation](https://github.com/huggingface/lerobot) |

<a id="other-tools"></a>

**Other Tools**

<a id="robot-interfaces-and-tools"></a>

<a id="projects-and-tools"></a>

Interfaces and utilities for robot observations, actions, evaluation, execution feedback, and data workflows.

| Resource | Role | Interface | Deployment & evidence | Official source |
| --- | --- | --- | --- | --- |
| **ROSA — Robot Operating System Agent** | Natural-language agent for ROS systems | Tools for inspection, diagnosis, and robot operation | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Tool responses; capabilities depend on the configured robot.</p><p><strong>Setup:</strong> Appropriate tools and context for custom robots.</p><p><strong>Limits:</strong> Robot-specific task outcomes require the corresponding tools and context.</p></details> | [Code and documentation](https://github.com/nasa-jpl/rosa) · [Paper](https://arxiv.org/abs/2410.06472) |
| **ROS MCP Server** | MCP interface to ROS | MCP through ROS/rosbridge | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Robot communication and introspection.</p><p><strong>Setup:</strong> A connected agent and robot stack.</p><p><strong>Limits:</strong> Planning and outcome evaluation depend on the connected agent and robot stack.</p></details> | [Code and documentation](https://github.com/robotmcp/ros-mcp-server) |
| **Inspect Robots (RoboCurve)** | Evaluation framework connecting LLM-agent/VLA policies, robot embodiments, and benchmark tasks | Policy and embodiment adapters; task execution and audit logs | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Runs evaluations and records auditable trial logs; powers [StationeryBench](https://github.com/robocurve/stationerybench).</p><p><strong>Setup:</strong> Matching policy, task, and robot adapters. The linked GPT-6 Astra report uses version 0.58.0 on YAM arms.</p><p><strong>Limits:</strong> Alpha software; framework capabilities and results from a specific evaluation are distinct. See the [trial results and limitations](#real-robot-demonstrations).</p></details> | [Code](https://github.com/robocurve/inspect-robots) · [Docs](https://docs.inspectrobots.org/) · [GPT-6 Astra report](https://openai.robocurve.org/gpt-6-astra/) <br> [![GitHub stars](https://img.shields.io/github/stars/robocurve/inspect-robots?style=flat-square&label=stars)](https://github.com/robocurve/inspect-robots) |
| **ros-skill** | Agent Skill for ROS/ROS 2 | Python CLI over rosbridge WebSocket | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> JSON responses for topic, service, node, parameter, and action commands.</p><p><strong>Setup:</strong> A configured robot and rosbridge.</p><p><strong>Limits:</strong> Planning and outcome interpretation remain with the calling agent.</p></details> | [Code and command reference](https://github.com/lpigeon/ros-skill) <br> [![GitHub stars](https://img.shields.io/github/stars/lpigeon/ros-skill?style=flat-square&label=stars)](https://github.com/lpigeon/ros-skill) |
| **Video to Data (V2D)** | Agent-assisted video segmentation and retrieval, 3D reconstruction, human-to-robot motion retargeting, and Isaac Lab policy training | Composable data-processing and training pipeline | <details class="entry-notes"><summary>Feedback, setup & limits</summary><p><strong>Feedback / workflow:</strong> Organizes demonstration data and connects reconstruction, retargeting, and policy-training stages.</p><p><strong>Setup:</strong> GPU-enabled Docker, model weights, robot assets, and source datasets for the selected workflow.</p><p><strong>Limits:</strong> Hardware compatibility varies by module. Its ingestion agent organizes demonstration data; it is not itself an online robot-control agent.</p></details> | [Code and documentation](https://github.com/nvidia-isaac/video_to_data) <br> [![GitHub stars](https://img.shields.io/github/stars/nvidia-isaac/video_to_data?style=flat-square&label=stars)](https://github.com/nvidia-isaac/video_to_data) |


</details>

### Social Demos

<details class="project-group" open>
<summary>Browse 31 demos and evaluations</summary>

<a id="social-demos-and-evaluations"></a>

Selected X / Twitter posts about GPT-6 Astra, with dates in UTC+8. Updated through 2026-09-13: 32 demo/evaluation posts are grouped into 31 entries. Two research-discussion posts are listed under Articles. Results below are author-reported unless stated otherwise.

[Real robots](#real-robot-demonstrations) · [Simulation](#simulation-demonstrations) · [Perception and reconstruction](#perception-and-reconstruction) · [Research discussions](#articles)

<a id="real-robot-demonstrations"></a>

**Real-robot demonstrations**

| Preview | Name | Date | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://x.com/chooi_jeq/status/2098427488787730636"><img src="https://pbs.twimg.com/media/HR8eAsCacAACY8b.jpg" alt="Jay Chooi / Robocurve — StationeryBench — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098427417312546816/vid/avc1/1920x1080/EzYWIs63EscjJMd7.mp4?tag=29) | **Jay Chooi / Robocurve — StationeryBench** | 2026-09-11 | Real · bimanual YAM | Across 200 trials on five tasks, Astra and MolmoAct2 obtain mean progress scores of **46/100 vs 12/100**; complete-task outcomes are **7/100 vs 0/100**. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/chooi_jeq/status/2098427488787730636) · [Benchmark catalogue](#benchmarks-1) · [Project / code](https://github.com/robocurve/stationerybench) · [Further sources](https://openai.robocurve.org/stationerybench/). Progress scores are not success rates. Astra uses end-effector poses with IK; MolmoAct2 uses joint-action chunks. Budgets and training distributions differ, rigs are not always shared, and grading is human and non-blind. MolmoAct2 never leaves its initial pose in 47/100 trials. Demo videos remove waiting and accelerate playback.</details> |
| <a href="https://x.com/ax_pey/status/2098216469012283681"><img src="https://pbs.twimg.com/amplify_video_thumb/2098212559770013696/img/neTOctu-ZjIamRtG.jpg" alt="Axel — video-conditioned mobile manipulation — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098212559770013696/vid/avc1/1920x1080/BC4m4aPH1EDY6cor.mp4?tag=29) | **Axel — video-conditioned mobile manipulation** | 2026-09-11 | Real · mobile manipulator | Author reports learning a task from demonstration video without a text task prompt, across changed camera views and layouts, using end-effector or joint actions. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/ax_pey/status/2098216469012283681) · [Further sources](https://x.com/npew/status/2098229057955779039). No text task prompt does not imply no system prompt or tool definitions. This is an independent author’s demonstration; no aggregate success rate is supplied.</details> |
| <a href="https://x.com/_wenlixiao/status/2097801944119349455"><img src="https://pbs.twimg.com/amplify_video_thumb/2097801926503243776/img/3MeFRqvS3uGd5_tw.jpg" alt="Wenli Xiao / Tonghe Zhang — video-conditioned robot imitation — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097801926503243776/vid/avc1/1280x720/ub5N-7mSkBw9C_d-.mp4?tag=16) | **Wenli Xiao / Tonghe Zhang — video-conditioned robot imitation** | 2026-09-10 | Real · robot arm | A human demonstration video is supplied to a coding agent to guide a robot arm; authors report first-attempt success on the shown task. <details class="entry-notes"><summary>Sources & notes</summary>[Xiao post](https://x.com/_wenlixiao/status/2097801944119349455) · [Zhang post](https://x.com/TongheZhang01/status/2097801107602911243) · [ENPIRE](https://github.com/NVlabs/ENPIRE). Related posts, not independent replications; no aggregate task success rate supplied.</details> |
| <a href="https://x.com/k7agar/status/2097721660346683495"><img src="https://pbs.twimg.com/amplify_video_thumb/2097721551311486976/img/P9VLHB2Thyfvg7rJ.jpg" alt="k7agar — instruction-following manipulation — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097721551311486976/vid/avc1/224x224/gvHkK9Cqe8M219r6.mp4?tag=29) | **k7agar — instruction-following manipulation** | 2026-09-10 | Real · robot arm | Demonstrates instruction-following manipulation using Astra for high-level planning and a simple inverse-kinematics layer. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/k7agar/status/2097721660346683495) · [Further sources](https://x.com/k7agar/status/2097722392173052298). The author reports limited dexterity. Selected demonstrations do not establish a repeated task success rate.</details> |
| <a href="https://x.com/yassineyousfi_/status/2097362500455211343"><img src="https://pbs.twimg.com/media/HRtTc8oboAQk9nr.png?name=orig" alt="Yassine Yousfi — yad-use robot interface — original post preview" width="200"></a> | **Yassine Yousfi — yad-use robot interface** | 2026-09-09 | Tool · SO-101 / MuJoCo | An agent interface for an SO-101 arm, Insta360 camera, and MuJoCo replica, with function calls and optional MCP. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/yassineyousfi_/status/2097362500455211343) · [Project / code](https://github.com/YassineYousfi/yad-use). The original post contains a photograph rather than a task video; the specific run’s real-versus-sim execution and task success are unverified.</details> |
| <a href="https://x.com/cdngdev/status/2097339677128982873"><img src="https://pbs.twimg.com/amplify_video_thumb/2097210560727437312/img/GYHkMobXeJU1Ahb-.jpg" alt="Thijs — SO-101 brush painting — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097210560727437312/vid/avc1/1920x1080/QiY_vztFuc1VN4mF.mp4?tag=29) | **Thijs — SO-101 brush painting** | 2026-09-08 | Real · SO-101 | Camera-guided painting of the Golden Gate Bridge, with improvement over attempts. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/cdngdev/status/2097339677128982873) · [Control details](https://x.com/cdngdev/status/2097339677745516710). Author supplied calibration anchors and feedback; roughly one-minute action segments with background monitoring.</details> |
| <a href="https://x.com/dhvanil/status/2097350152713363812"><img src="https://pbs.twimg.com/amplify_video_thumb/2097345778972778497/img/fgyziwNY0X-ImCa1.jpg" alt="dhvanil — camera-guided brush calibration — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097345778972778497/vid/avc1/3840x2160/zuWV6a0LHI7e0JVs.mp4?tag=29) | **dhvanil — camera-guided brush calibration** | 2026-09-08 | Real · robot arm | Uses three cameras without supplied intrinsics or extrinsics, arm nudges, and brush-tip offsets for calibration. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dhvanil/status/2097350152713363812). The reported &lt;0.2 mm value describes camera-measured tip movement, not independently validated absolute positioning accuracy.</details> |
| <a href="https://x.com/ARXrobotics/status/2096328304794210604"><img src="https://pbs.twimg.com/amplify_video_thumb/2096328278588186624/img/4_NW3RqbOTj-1SDO.jpg" alt="ARX — washing-machine knob operation — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096328278588186624/vid/avc1/1022x720/HED2x80GR0g7UCQS.mp4?tag=29) | **ARX — washing-machine knob operation** | 2026-09-06 | Real · ARX | Natural-language instruction to turn a knob in a new room; author says GPT plus a custom control layer, without a VLA. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/ARXrobotics/status/2096328304794210604) · [Author clarification](https://x.com/ARXrobotics/status/2096449872782348475). Case demonstration; repeated success rate and control-layer capabilities remain unverified.</details> |
| <a href="https://x.com/k7agar/status/2096593654320341027"><img src="https://pbs.twimg.com/amplify_video_thumb/2096592948205080576/img/dB6FlSK0r4K3o2l_.jpg" alt="k7agar — table-wiping attempt — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096592948205080576/vid/avc1/640x700/7UEKkcq8dkg2-mkL.mp4?tag=29) | **k7agar — table-wiping attempt** | 2026-09-06 | Real · robot arm | Shows Astra attempting to wipe a table. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/k7agar/status/2096593654320341027). No repeated success rate, surface-coverage, force, or timing evaluation is supplied; the post does not provide an exact model-version run log.</details> |
| <a href="https://x.com/k7agar/status/2096590458369810679"><img src="https://pbs.twimg.com/amplify_video_thumb/2096590281072373760/img/urTD4ODSUnzhvxxj.jpg" alt="k7agar — standing a block upright — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096590281072373760/vid/avc1/640x480/QuJv1KdSYEGRzvu5.mp4?tag=29) | **k7agar — standing a block upright** | 2026-09-06 | Real · robot arm | Shows a robot picking up a green block and standing it upright. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/k7agar/status/2096590458369810679). A selected Astra demonstration without repeated trials or an exact model-version run log.</details> |
| <a href="https://x.com/chooi_jeq/status/2096064315115839904"><img src="https://pbs.twimg.com/media/HRa3vJWaEAAQSRT.jpg" alt="Jay Chooi / Robocurve — GPT-6 Astra on robotic manipulation — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096064287764885505/vid/avc1/1920x1080/DS7GMzj6bTNwOinu.mp4?tag=29) | **Jay Chooi / Robocurve — GPT-6 Astra on robotic manipulation** | 2026-09-05 | Real · YAM arms | Inspect Robots 0.58.0 on bimanual YAM arms: **19/20** block-into-bowl completions and **2/20** puzzle insertions. Each turn supplies three camera views plus proprioception; the agent requests absolute end-effector poses through `move_to`. Medium reasoning, a 20-LLM-call budget, and a 25% speed cap. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/chooi_jeq/status/2096064315115839904) · [Report (2026-09-04) and trial records](https://openai.robocurve.org/gpt-6-astra/) · [Framework](https://github.com/robocurve/inspect-robots). Human, non-blind grading and manual resets; trials were not interleaved. Bowl comparisons used different rigs; puzzle used the same rig. The 95% figure applies only to the bowl task.</details> |

<a id="simulation-demonstrations"></a>

**Simulation demonstrations**

| Preview | Name | Date | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://x.com/gclue_akira/status/2098300921658868185"><img src="https://pbs.twimg.com/amplify_video_thumb/2098297480752607232/img/Wn0NcGWBxngznKmZ.jpg" alt="Akira Sasaki — robot-dog training and design — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098297480752607232/vid/avc1/1440x1200/fDFQ9O6Z9JvGebZx.mp4?tag=29) | **Akira Sasaki — robot-dog training and design** | 2026-09-11 | Sim · RL / Fusion 360 | Author reports five days, 25 iterations, and nine motions while developing a robot dog through RL and CAD design. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/gclue_akira/status/2098300921658868185) · [Further sources](https://x.com/TheMoonMidas/status/2098530577989206331). A coding, training, and design workflow rather than Astra directly supplying a locomotion policy; hardware construction remains planned.</details> |
| <a href="https://x.com/thermalpastor/status/2098118000499171340"><img src="https://pbs.twimg.com/amplify_video_thumb/2098117558058758145/img/z-umC4AKtr6cmpkY.jpg" alt="H / thermalpastor — G1 stair-climbing failure — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098117558058758145/vid/avc1/1280x720/J9MFqSctza0Szosx.mp4?tag=29) | **H / thermalpastor — G1 stair-climbing failure** | 2026-09-11 | Sim · G1 | A direct-control attempt fails at the first stair when weight transfer causes the humanoid to fall. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/thermalpastor/status/2098118000499171340) · [Further sources](https://x.com/thermalpastor/status/2098118841947836647). Author reports 29 joints, 89 calls, and 1.27 million tokens, with physics paused between 20 ms simulation steps. A useful failure case, not real-time stair climbing.</details> |
| <a href="https://x.com/andonlabs/status/2098103320208712049"><img src="https://pbs.twimg.com/amplify_video_thumb/2098103113504968704/img/_WU7Qd3_rs6oMglX.jpg" alt="Andon Labs — Drone-Bench — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098103113504968704/vid/avc1/960x720/pNceFG3kmF46dIQO.mp4?tag=29) | **Andon Labs — Drone-Bench** | 2026-09-11 | Sim · drone tasks | Evaluates agent-written code for reconstruction, localization, navigation, detection, and following; each task has at least one Astra run beating the human baseline. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/andonlabs/status/2098103320208712049) · [Project / code](https://andonlabs.com/evals/drone-bench). Ten runs per model and up to ten submissions per run, selecting the best. Tasks receive baseline upstream outputs; the human baseline also uses coding-agent assistance. The end-to-end probability plot multiplies per-task probabilities rather than measuring a continuous full mission.</details> |
| <a href="https://x.com/Kuvvius/status/2098038921301311753"><img src="https://pbs.twimg.com/amplify_video_thumb/2098038779349192704/img/swE_A-WN1JE8H4KL.jpg" alt="Jiawei Gu — HumanCLAW — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098038779349192704/vid/avc1/932x1052/C_I9S-ILzBezAJcE.mp4?tag=29) | **Jiawei Gu — HumanCLAW** | 2026-09-10 | Sim · HSSD humanoid | A fixed harness with pretrained motion generation evaluates 1,218 episodes across 41 HSSD validation houses. Astra scores 75.5% on Find, 57.1% on Navigate, and 46.6% on Interact. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/Kuvvius/status/2098038921301311753) · [Project / code](https://human-claw.github.io/) · [Further sources](https://huggingface.co/datasets/Choiszt/humanclaw-gpt6-lowthinking-results-logs). Low-thinking configuration in a partially physical simulator; these are harness-level outcomes, not direct motor control or real-robot results.</details> |
| <a href="https://x.com/thermalpastor/status/2097802933429796873"><img src="https://pbs.twimg.com/amplify_video_thumb/2097802192610832386/img/rVcrj-F1C5hzETPC.jpg" alt="H / thermalpastor — G1 bicycle controller — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097802192610832386/vid/avc1/1920x1080/k3qo1t9iZpoJ8CGh.mp4?tag=29) | **H / thermalpastor — G1 bicycle controller** | 2026-09-10 | Sim · G1 | Astra writes and debugs a controller for approximately 30 seconds of simulated bicycle riding without virtual stabilizers, according to the author. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/thermalpastor/status/2097802933429796873). Controller synthesis rather than demonstrated online model control. The post’s rolling-start and from-rest descriptions are inconsistent, so the initial-condition claim remains unresolved.</details> |
| <a href="https://x.com/thermalpastor/status/2097496200631210136"><img src="https://pbs.twimg.com/amplify_video_thumb/2097495575558258688/img/glSoKNk_84aYukL_.jpg" alt="H / thermalpastor — two-robot juggling — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097495575558258688/vid/avc1/1920x1080/_GDd0jHJHResOoJ0.mp4?tag=29) | **H / thermalpastor — two-robot juggling** | 2026-09-09 | Sim · MuJoCo | Two robots exchange balls in MuJoCo, keeping at least one airborne. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/thermalpastor/status/2097496200631210136). Author labels the playback 1× simulation speed; this does not establish real-time model inference or hardware control.</details> |
| <a href="https://x.com/sri299792458/status/2097677796348715375"><img src="https://pbs.twimg.com/amplify_video_thumb/2097677785703796736/img/Y0XosYzWpAVS3LMO.jpg" alt="Srinivas — Go1 blind stair locomotion — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097677785703796736/vid/avc1/800x600/Ha2p_qkPa3XyVK86.mp4?tag=29) | **Srinivas — Go1 blind stair locomotion** | 2026-09-09 | Sim · Go1 | Demonstrates stair locomotion using direct model actions and shares two prompts. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/sri299792458/status/2097677796348715375) · [Further sources](https://x.com/sri299792458/status/2097349207795335424). Physics pauses during inference. The author raises possible memorization of raw joint-angle patterns; real-time execution and generalization are not established.</details> |
| <a href="https://x.com/dimentary/status/2097141042214797801"><img src="https://pbs.twimg.com/amplify_video_thumb/2097140400058503168/img/jdcbFn7DHbVRhf7T.jpg" alt="Dmytro Hrybov — dexterous-hand drawing — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097140400058503168/vid/avc1/1600x900/KMym95lPHX-kh0oc.mp4?tag=29) | **Dmytro Hrybov — dexterous-hand drawing** | 2026-09-08 | Sim · MuJoCo | A generated MuJoCo setup and controller use a Kinova Gen3 arm and Shadow Hand to draw a dove through pen–paper contact. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dimentary/status/2097141042214797801) · [Contact and timing details](https://x.com/dimentary/status/2097141323883327933). Two-finger grip despite a five-finger hand; video sped up 4×.</details> |
| <a href="https://x.com/sri299792458/status/2097349207795335424"><img src="https://pbs.twimg.com/amplify_video_thumb/2097346266044780544/img/PvyRkir9BOv8bzGD.jpg" alt="Srinivas — Go1 walking through direct actions — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097346266044780544/vid/avc1/800x600/TjcvsHxdG6rJWm9E.mp4?tag=14) | **Srinivas — Go1 walking through direct actions** | 2026-09-08 | Sim · Go1 | Author reports 250 model calls for five seconds of simulated walking, with actions at 50 Hz in simulation time. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/sri299792458/status/2097349207795335424). Physics pauses during each inference. The simulation action frequency is not the wall-clock inference or control rate.</details> |
| <a href="https://x.com/ludocomito/status/2097329417760440461"><img src="https://pbs.twimg.com/amplify_video_thumb/2097326030470230017/img/7ZIu7E1aqho1fnNS.jpg" alt="Ludovico Comito — CARLA driving planner — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097326030470230017/vid/avc1/1920x1080/uhSOXLYqJTK_jSu5.mp4?tag=29) | **Ludovico Comito — CARLA driving planner** | 2026-09-08 | Sim · CARLA | Uses Astra as a high-level driving planner in CARLA, including obstacle scenarios. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/ludocomito/status/2097329417760440461). Simulation demonstration; it does not establish real-vehicle control, low-level driving competence, or a benchmark success rate.</details> |
| <a href="https://x.com/dimentary/status/2096785235795181900"><img src="https://pbs.twimg.com/amplify_video_thumb/2096785124478390272/img/IGBjIu069D7LvrCx.jpg" alt="Dmytro Hrybov — six-legged, dual-arm transport — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096785124478390272/vid/avc1/1280x720/igU4w02KTPNMZ6yj.mp4?tag=29) | **Dmytro Hrybov — six-legged, dual-arm transport** | 2026-09-07 | Sim · MuJoCo | Building a MuJoCo embodiment and controller that move objects between tables. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dimentary/status/2096785235795181900). Simulation demonstration; an unusual morphology alone does not establish out-of-distribution generalization.</details> |
| <a href="https://x.com/Hakim_Fang/status/2096565038744252613"><img src="https://pbs.twimg.com/amplify_video_thumb/2096564871756451840/img/cnmv55yniWL6P6ET.jpg" alt="Hakim Phun — RoboDojo tasks — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2096564871756451840/vid/avc1/960x720/F4hJJa9CwgxKMbsS.mp4?tag=14) | **Hakim Phun — RoboDojo tasks** | 2026-09-06 | Sim · RoboDojo | Selected robot-simulation task demonstrations. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/Hakim_Fang/status/2096565038744252613). The collection records the author's caveat that inference pauses were removed and a full quantitative evaluation was not yet available.</details> |

<a id="perception-and-reconstruction"></a>

**Perception and reconstruction**

These are supporting capabilities for robot-use workflows, rather than direct evidence of a complete robot-control agent.

| Preview | Name | Date | Environment | Description |
| --- | --- | --- | --- | --- |
| <a href="https://x.com/dimentary/status/2098581216140366210"><img src="https://pbs.twimg.com/amplify_video_thumb/2098571195595751425/img/xkd6OAo0hK0KpwjY.jpg" alt="Dmytro Hrybov — tendon-hand model follow-up — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098571195595751425/vid/avc1/1440x1080/GH7_5nbowNmEJcNc.mp4?tag=29) | **Dmytro Hrybov — tendon-hand model follow-up** | 2026-09-12 | Sim model · MuJoCo | Models a hand with 25 motors and 50 tendon branches using simplified transmissions and CAD geometry. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dimentary/status/2098581216140366210) · [Further sources](https://x.com/dimentary/status/2097857980150763900). Cable routing remains difficult even with human guidance, and cable collisions are not simulated. This is a modeling follow-up, not a validated physical hand.</details> |
| <a href="https://x.com/Lingxiao234/status/2097717020540481630"><img src="https://pbs.twimg.com/amplify_video_thumb/2097716973899780096/img/IgOqn00YQoSzMzG7.jpg" alt="Lingxiao Guo — video-to-Wuji-hand retargeting — original video thumbnail" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097716973899780096/vid/avc1/1920x1080/gsFWFgb-G3egibZw.mp4?tag=16) | **Lingxiao Guo — video-to-Wuji-hand retargeting** | 2026-09-10 | Video · retargeting | Real2Sim and motion retargeting from two videos, without supplied states or actions. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/Lingxiao234/status/2097717020540481630). Execution environment, hardware deployment, repeatability, and this demo's code release remain unverified; the separate Real2Sim repository is not assumed to reproduce this result.</details> |
| <a href="https://x.com/m_wulfmeier/status/2097999274025927156"><img src="https://pbs.twimg.com/media/HR2W23ia0AAF7t3.jpg?name=orig" alt="Markus Wulfmeier — robot perception evaluation — original post preview" width="200"></a> | **Markus Wulfmeier — robot perception evaluation** | 2026-09-10 | Evaluation · perception | Author reports a nearly 8% improvement over Sol on a robot-perception evaluation. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/m_wulfmeier/status/2097999274025927156). The post does not clarify whether the change is relative or in percentage points and does not provide a complete evaluation protocol; this is perception evidence, not a closed-loop robot-task result.</details> |
| <a href="https://x.com/siyuanhuang95/status/2097894309274284267"><img src="https://pbs.twimg.com/amplify_video_thumb/2097893893719396352/img/NVPn1pd4qziQw7hf.jpg" alt="Siyuan Huang — articulated-scene Real2Sim — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097893893719396352/vid/avc1/768x432/Hrtc9ugwYYyVaW0C.mp4?tag=29) | **Siyuan Huang — articulated-scene Real2Sim** | 2026-09-10 | Real2Sim · articulated scene | Reconstructs an articulated scene from several photographs. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/siyuanhuang95/status/2097894309274284267). A visual reconstruction demonstration; dynamics accuracy, repeatability, and a reproducing code release are unverified.</details> |
| <a href="https://x.com/EnactraAI/status/2097777259382018088"><img src="https://pbs.twimg.com/amplify_video_thumb/2097777088233439232/img/PlAlh9AKk8hWrOg_.jpg" alt="Enactra — Madison Square Park reconstruction — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097777088233439232/vid/avc1/1600x864/qomOfFfXbYWm_AK3.mp4?tag=29) | **Enactra — Madison Square Park reconstruction** | 2026-09-10 | Scene · Unreal Engine | Builds a Madison Square Park scene in Unreal Engine and compares it with Google Earth imagery. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/EnactraAI/status/2097777259382018088). Scene and asset construction rather than an embodied task evaluation; physical fidelity and robot interaction are unverified.</details> |
| <a href="https://x.com/dimentary/status/2097857980150763900"><img src="https://pbs.twimg.com/amplify_video_thumb/2097853948313124864/img/9RZ5TB9n0FEj8SMU.jpg" alt="Dmytro Hrybov — video-to-1X-hand model — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2097853948313124864/vid/avc1/1440x1016/doJuLL3zdxEDE8sJ.mp4?tag=29) | **Dmytro Hrybov — video-to-1X-hand model** | 2026-09-10 | Sim model · MuJoCo | Constructs a simplified hand mechanism from video, with illustrative cable deformation. <details class="entry-notes"><summary>Sources & notes</summary>[Post](https://x.com/dimentary/status/2097857980150763900) · [Further sources](https://x.com/dimentary/status/2098581216140366210). Full tendon physics is future work. Related to the later tendon-hand post by the same author, not an independent replication.</details> |
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
| <a href="https://capgym.github.io/"><img src="https://arxiv.org/html/2603.22435v1/assets/figures/splash_figure_v3.png" alt="CaP-X paper overview: CaP-Bench and CaP-Gym" width="200"></a> | **CaP-X / CaP-Bench** | 2026 | Robosuite / LIBERO-PRO / BEHAVIOR | Evaluates robot-control coding agents across API abstraction levels, single-/multi-turn interaction, and visual grounding <details class="entry-notes"><summary>Sources & notes</summary>[Paper](https://arxiv.org/abs/2603.22435) · [Code](https://github.com/capgym/cap-x) · [Project](https://capgym.github.io/)<br>Preview: Figure 1 of the paper.</details> |
| <a href="https://x.com/chooi_jeq/status/2098427488787730636"><img src="https://pbs.twimg.com/media/HR8eAsCacAACY8b.jpg" alt="Jay Chooi / Robocurve — StationeryBench — original post preview" width="200"></a><br>[▶ Video](https://video.twimg.com/amplify_video/2098427417312546816/vid/avc1/1920x1080/EzYWIs63EscjJMd7.mp4?tag=29) | **StationeryBench** | 2026 | Real robots · bimanual YAM; abstract mock | Five desk-stationery tasks built on [Inspect Robots](https://github.com/robocurve/inspect-robots): uncap a marker, retrieve an eraser, extract a sticky pad, pour paper clips, and hand over a ruler. <details class="entry-notes"><summary>Sources & notes</summary>[Code](https://github.com/robocurve/stationerybench) · [Task reference](https://robocurve.github.io/stationerybench/) · [Evaluation report](https://openai.robocurve.org/stationerybench/) · [Community report](#social-demos). The package records binary operator verdicts; the report uses 0–4 stage scores. The package defaults to 120 seconds; the report's agent condition uses 90 seconds. The bundled mock has no physics and does not evaluate manipulation ability.</details> |

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
