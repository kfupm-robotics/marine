# Branch protection for `main`

Set these once, in **Settings → Branches → Add branch ruleset** (or classic branch protection) for `main`:

- Require a pull request before merging
  - Require 1 approval
  - Dismiss stale approvals when new commits are pushed
- Require status checks to pass: **Build and publish / build-deploy**
- Require branches to be up to date before merging
- Block force pushes and deletion
- Optionally: require review from Code Owners (add a `CODEOWNERS` file naming the PI and Co-PI)

Also:

- Settings → Pages: deploy from the `gh-pages` branch (created by the first run of the workflow).
- Settings → Actions → General: workflow permissions "Read and write" (needed to push to `gh-pages`).
- Keep the organization's membership small. Give students **Write** access, and give PI and Co-PI **Admin**.
- Before making the repository public, check the full history for confidential files: `git log --all --name-only`.
