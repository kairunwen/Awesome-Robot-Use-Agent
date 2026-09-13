# Contributing to Awesome Robot Use Agent

Suggestions and corrections are welcome through an issue or pull request.

- Add a primary source: the authors' paper, project page, repository, or official documentation.
- Explain the resource's connection to robot-use agents in one sentence and place it in the closest existing category.
- Use the current sections: Articles for perspectives; Papers for research references (Surveys, Models & Frameworks, Datasets, Benchmarks); Projects for implementations and Social Demos; Benchmarks for evaluation protocols and projects.
- In Projects, distinguish Systems & Frameworks, Environment & Sandbox, and Tool Box (reusable libraries and agent-facing robot interfaces). Keep papers and their code links together in Papers; do not add a duplicate implementation-only row under Projects. Cross-link benchmark descriptions where useful. Repeated views are not additional distinct works.
- Keep a separate social post only when it adds a distinct demonstration, evaluation, or discussion. Link the underlying work and merge posts about the same demonstration.
- For papers, include the full title, first-release month (`YYYY-MM`), and verified official links. Describe the mechanism rather than repeating promotional claims.
- Check what is actually released. Label website-only repositories, partial releases, and unverified code availability explicitly.
- Cite the original work separately from third-party implementations. Social posts and demonstrations need an original source and clearly stated evidence scope.
- Keep general VLA, world-model, and dataset additions selective: explain their direct role as an agent component or evaluation resource.
- Preserve the distinction between a proposed method, an author-reported result, and an independently reproduced result.

Suggested paper row:

```markdown
| YYYY-MM | **Full paper title** <br> [Project](URL) | [Paper](URL) | [Code](URL) or Unverified | One-sentence mechanism. <details class="entry-notes"><summary>Release & evidence</summary>Release or deployment limits, if applicable.</details> |
```

For Systems & Frameworks and the Other Tools subsection of Tool Box, use the same fields: Resource, Role, Interface, Deployment & evidence, and Official source. Keep the role to one sentence; in Deployment & evidence, use `<details class="entry-notes">` with Feedback / workflow, Setup, and Limits. Record only documented capabilities. For other projects or model families, include their interface, intended role, official repository/docs, and current availability. For benchmarks, distinguish the released protocol from any particular evaluation report, including scoring and time budgets. Website entry counts include category views; do not describe them as counts of unique works.

Keep paper rows newest-first within a category. Use a focused commit message such as `docs: add <work>` or `docs: update <section>`, following `type: description`.

## Previews, filters, and checks

- For Social Demos, use the matching Real-robot, Simulation, or Perception and reconstruction group. State the actual environment and put evidence limits in Sources & notes.
- Label direct implementation repository links `Code` or `Project / code`. The website's Code linked filter recognizes GitHub links with `code` in the label; a project page or framework link alone does not establish that a demo can be reproduced.
- Keep dates in `YYYY-MM-DD` for demos. Website date sorting stays within the three demo groups.
- Use an official or original-post preview URL over HTTPS, with meaningful alt text and a source link. Retain source text when a preview is unavailable; do not substitute an unrelated image.
- Before submitting, run `python -m unittest discover -s website -p 'test_*.py'` and `git diff --check`. Build checks cover table structure, duplicate entries within a table, internal anchors, and preview metadata.
- Run `python website/check_links.py` to check external destinations and image responses. You can pass `--url URL` repeatedly to check only changed links. Review HTTP failures before deleting anything: rate limits, login gates, and bot protection are not proof that a source is dead.
