# Git Branching Strategy — WhoKnows Project

## Chosen Strategy: GitHub Flow

After researching the main branching strategies (Git Flow, GitHub Flow, Trunk-Based Development, and GitLab Flow), I chose **GitHub Flow** for the WhoKnows project.

## What is GitHub Flow?

GitHub Flow is a lightweight, branch-based workflow with one simple rule: the `main` branch is always deployable.

The workflow:

1. Create a feature branch from `main` (e.g., `feature/add-docker-support`)
2. Make commits on that branch
3. Open a Pull Request when the work is ready for review
4. Review, discuss, and run CI checks on the PR
5. Merge into `main`
6. Deploy from `main`

```
main:     ──●──────────●──────────●──────────●──
              \        ↑           \         ↑
feature/x:     ●──●──●─┘            \       │
                                      ●──●──┘
                                 feature/y
```

## Why GitHub Flow?

### Fits the team size

I am working solo on this project. Git Flow's overhead with `develop`, `release`, and `hotfix` branches adds complexity that doesn't pay off for a single developer. GitHub Flow keeps things simple — one main branch, short-lived feature branches.

### Supports continuous deployment

The course involves deploying to Azure and setting up CI/CD pipelines. GitHub Flow aligns directly with this because `main` is always deployable. Every merge to `main` can trigger a deployment pipeline via GitHub Actions.

### Simple and well-documented

GitHub Flow is the default workflow on GitHub, which means Pull Requests, branch protection rules, and Actions all integrate naturally without extra configuration.

### Good enough for rapid iteration

During the rewrite of the legacy WhoKnows application, I need to move fast — upgrading Python, replacing the framework, adding Docker, setting up CI/CD. Short-lived feature branches let me work on one thing at a time without the ceremony of Git Flow.

## Strategies I Considered but Rejected

### Git Flow
- **Why not:** Too heavy for a solo/small team project. The separate `develop` branch and release branches add overhead with no real benefit when there's no release schedule or multiple parallel versions to maintain.

### Trunk-Based Development
- **Why not:** Works well for experienced teams with strong CI, but skipping branches entirely and committing straight to `main` means no PR review process — I'd lose the safety net of CI checks running before merge.

### GitLab Flow
- **Why not:** Adds environment branches (staging, production) on top of GitHub Flow. Could be useful later, but overkill at this stage of the project.

## Branch Naming Convention

| Branch type | Pattern | Example |
|-------------|---------|---------|
| Feature | `feature/<short-description>` | `feature/add-docker` |
| Bug fix | `fix/<short-description>` | `fix/sql-injection` |
| Chore/config | `chore/<short-description>` | `chore/setup-ci` |

## Branch Protection Rules

The following rules will be applied to the `main` branch:

- Require a pull request before merging (no direct pushes)
- Require CI status checks to pass before merging
- Require branches to be up to date before merging

## Summary

GitHub Flow gives me the right balance of simplicity and safety for this project. It's easy to set up, works naturally with GitHub's tooling, and supports the continuous deployment pipeline we need for the DevOps course.
