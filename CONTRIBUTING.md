# Contributing to Awesome Robot Use Agent

Suggestions and corrections are welcome through an issue or pull request.

- Add a primary source: the authors' paper, project page, repository, or official documentation.
- Explain the resource's connection to robot-use agents in one sentence and place it in the closest existing category.
- Group by system role, not publication format: agents and frameworks, model and learning components, or evaluation. Keep a work's paper, code, model, project page, and official demos in one main entry; use cross-references when it spans roles.
- Keep a separate social post only when it adds a distinct demonstration, evaluation, or discussion. Link the underlying work and merge posts about the same demonstration.
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
