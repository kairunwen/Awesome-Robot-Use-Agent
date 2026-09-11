# Awesome Robot Use Agent

A curated list of agents that use robots through skills, code, tools, and feedback.

From language-guided skill selection to embodied coding agents and execution harnesses: **observe → reason → act → verify → recover**.

**Scope:** robot-use agents, embodied tool use, code-as-policy, policy orchestration, execution feedback, and evaluation. Selected VLA models and learning infrastructure are included as supporting resources.

**Last curated:** 2026-09-11 · **21 resources** · Initial curated selection, not an exhaustive survey.

## Contents

- [What is a robot-use agent?](#what-is-a-robot-use-agent)
- [Start here](#start-here)
- [Planning and code as policies](#planning-and-code-as-policies)
- [Execution feedback and recovery](#execution-feedback-and-recovery)
- [Embodied harnesses and policy orchestration](#embodied-harnesses-and-policy-orchestration)
- [Robot interfaces and tool frameworks](#robot-interfaces-and-tool-frameworks)
- [Agent benchmarks and evaluation frameworks](#agent-benchmarks-and-evaluation-frameworks)
- [Simulation environments and task suites](#simulation-environments-and-task-suites)
- [Supporting policies and learning infrastructure](#supporting-policies-and-learning-infrastructure)
- [How to compare systems](#how-to-compare-systems)
- [Contributing](#contributing)
- [License](#license)

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
| Language grounded in available robot skills | [SayCan](https://say-can.github.io/) |
| Robot behavior expressed as generated code | [Code as Policies](https://code-as-policies.github.io/) |
| Replanning from execution feedback | [Inner Monologue](https://innermonologue.github.io/) |
| Coding agents evaluated on manipulation | [CaP-X](https://github.com/capgym/cap-x) |
| A tool-based embodied harness | [Thea](https://github.com/EIT-HAI/Thea) |
| Runtime critics and recovery around a frozen policy | [Zetta](https://github.com/air-embodied-brain/Zetta-Embodiment) |
| Connecting an agent to ROS | [ROSA](https://github.com/nasa-jpl/rosa) / [ROS MCP Server](https://github.com/robotmcp/ros-mcp-server) |

## Planning and code as policies

Years refer to the first paper release. Links labeled **Code** point to official implementation resources; release scope is noted where relevant. A code link is not a claim that the complete paper setup can be reproduced from that repository alone.

| Work | Year | Why it belongs | Official resources |
| --- | --- | --- | --- |
| **SayCan — Do As I Can, Not As I Say: Grounding Language in Robotic Affordances** | 2022 | Combines language-model skill scoring with affordance/value estimates to select feasible robot behaviors. | [Paper](https://arxiv.org/abs/2204.01691) · [Project](https://say-can.github.io/) · [Code: tabletop simulation](https://github.com/google-research/google-research/tree/master/saycan) |
| **Code as Policies: Language Model Programs for Embodied Control** | 2022 | Generates programs that compose perception outputs, control APIs, and feedback loops. | [Paper](https://arxiv.org/abs/2209.07753) · [Project](https://code-as-policies.github.io/) · [Code](https://github.com/google-research/google-research/tree/master/code_as_policies) |
| **VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models** | 2023 | Uses generated code and visual grounding to construct 3D value maps for motion planning; the generated program can be reevaluated with visual feedback. | [Paper](https://arxiv.org/abs/2307.05973) · [Project](https://voxposer.github.io/) · [Code](https://github.com/huangwl18/VoxPoser) |
| **CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation** | 2026 | Studies embodied coding agents through CaP-Gym, CaP-Bench, CaP-Agent0, and CaP-RL, including execution feedback and skill synthesis. | [Paper](https://arxiv.org/abs/2603.22435) · [Code](https://github.com/capgym/cap-x) |

## Execution feedback and recovery

| Work | Year | Why it belongs | Official resources |
| --- | --- | --- | --- |
| **Inner Monologue: Embodied Reasoning through Planning with Language Models** | 2022 | Feeds success detection, scene descriptions, and human feedback into language-based planning; demonstrates replanning and responses to changed goals. | [Paper](https://arxiv.org/abs/2207.05608) · [Project and demos](https://innermonologue.github.io/) |
| **REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction** | 2023 | Summarizes multisensory execution history, explains failures, and conditions a planner on those explanations to produce corrective actions. | [Paper](https://arxiv.org/abs/2306.15724) · [Project](https://robot-reflect.github.io/) · [Code](https://github.com/real-stanford/reflect) |

## Embodied harnesses and policy orchestration

These works study the infrastructure and interaction loop around models and robot capabilities. Descriptions summarize the authors' stated methods; they do not equate release availability with independently verified performance.

| Work | Year | Main mechanism | Official resources / release boundary |
| --- | --- | --- | --- |
| **Guava: An Effective and Universal Harness for Embodied Manipulation** | 2026 | Studies iterative perception–reasoning–action, semantic action abstractions, and multimodal observations; also describes distillation into a smaller agent model. | [Paper](https://arxiv.org/abs/2606.18363). Implementation and checkpoint release not verified in this curation pass. |
| **RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning** | 2026 | Uses execution memory to route among heterogeneous policies and a Memory Bridge to improve handoffs between policies. | [Paper](https://arxiv.org/abs/2607.18060). Implementation release not verified in this curation pass. |
| **Thea — Towards the Harness of Embodied Agents** | 2026 | Wraps robot capabilities as callable tools, maintains symbolic scene context, and evaluates action termination, success, and failure causes. | [Paper](https://arxiv.org/abs/2608.11246) · [Project](https://eit-hai.github.io/thea/) · [Code](https://github.com/EIT-HAI/Thea). Public runtime and interfaces; robot/simulator deployment requires concrete adapters and capabilities. |
| **Zetta ζ: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence** | 2026 | Keeps the base policy frozen while developing runtime critics and recovery skills through execution, diagnosis, and gated updates. | [Paper](https://arxiv.org/abs/2608.16590) · [Project](https://air-embodied-brain.github.io/zetta/) · [Code](https://github.com/air-embodied-brain/Zetta-Embodiment). The separate `air-embodied-brain/zetta` repository hosts the project website. |

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

## Supporting policies and learning infrastructure

These resources can supply action models, data workflows, or deployment components. They are listed as foundations rather than complete robot-use agents.

| Resource | Role | Official source |
| --- | --- | --- |
| **OpenVLA** | Vision-language-action model and tools for adaptation to robot manipulation | [Code and model links](https://github.com/openvla/openvla) |
| **openpi** | Physical Intelligence's robot-policy implementations, training utilities, and inference interfaces | [Code and model links](https://github.com/Physical-Intelligence/openpi) |
| **LeRobot** | Robot learning library with policies, datasets, hardware integrations, and training workflows | [Code and documentation](https://github.com/huggingface/lerobot) |

## How to compare systems

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

## Contributing

Suggestions and corrections are welcome through an issue or pull request.

- Add a primary source: the authors' paper, project page, repository, or official documentation.
- Explain the resource's connection to robot-use agents in one sentence and place it in the closest existing category.
- For papers, include the full title, first-release year, and verified official links. Describe the mechanism rather than repeating promotional claims.
- Check what is actually released. Label website-only repositories, partial releases, and unverified code availability explicitly.
- Cite the original work separately from third-party implementations. Social posts and demonstrations need an original source and clearly stated evidence scope.
- Keep general VLA, world-model, and dataset additions selective: explain their direct role as an agent component or evaluation resource.
- Preserve the distinction between a proposed method, an author-reported result, and an independently reproduced result.

Suggested paper row:

```markdown
| **Full paper title** | First-release year | One-sentence mechanism and relevance | [Paper](URL) · [Project](URL) · [Code](URL), with release scope if needed |
```

## License

This collection is distributed under the [MIT License](LICENSE). Linked papers, code, models, and datasets retain their respective licenses.
