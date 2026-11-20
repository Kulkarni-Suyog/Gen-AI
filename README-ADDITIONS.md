# GSTSaral CI and deployment additions

These are **new files / small README additions** for the existing GSTSaral repository. Copy them into the root of your existing project; do not replace your Day 1–Day 11 folders.

## Files in this package

```text
.github/
└── workflows/
    └── ci.yml
render.yaml
README-ADDITIONS.md
TRACKER-UPDATE.md
```

## 1. Add the GitHub Actions workflow

Copy `.github/workflows/ci.yml` into the same path in your repository.

It runs on pushes and pull requests targeting `main` or `master`. It:
1. Installs `day11/requirements-dev.txt`.
2. Runs `ruff check .`.
3. Runs `python -m pytest day11/tests -v`.
4. Builds the Docker image without pushing it to a registry.

The workflow assumes your repository already has the Day 11 tests, root `Dockerfile`, `requirements-ui.txt`, and `day9/requirements.txt`.

## 2. Add the CI badge to your existing README

At the top of the existing root `README.md`, add this Markdown line:

```markdown
[![GSTSaral CI](https://github.com/Kulkarni-Suyog/Gen-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Kulkarni-Suyog/Gen-AI/actions/workflows/ci.yml)
```

The badge turns green only after the workflow succeeds on the default branch. If your default branch is not `main` or `master`, update the branch filters in `ci.yml` to match it.

## 3. Deploy GSTSaral on Render

1. Push the new `render.yaml` file to your GitHub repository.
2. Sign in to Render and choose **New → Blueprint**.
3. Connect `Kulkarni-Suyog/Gen-AI`.
4. Render reads `render.yaml` and creates two services: `gstsaral-api` and `gstsaral-ui`.
5. For the `GROQ_API_KEY` prompt, enter your Groq API key if you want live LLM-generated answers. Do not put the key in GitHub or commit it to a file.
6. Start the deployment and wait for both services to finish.

The configuration expects these Render addresses based on the service names:

- UI: `https://gstsaral-ui.onrender.com`
- API: `https://gstsaral-api.onrender.com`
- Health check: `https://gstsaral-api.onrender.com/health`

After deployment, open the health URL. It should return JSON similar to:

```json
{"status":"ok","day":9}
```

If Render assigns different service URLs, use the actual URLs shown on the Render dashboard instead.

### Required UI environment setting

The current `ui/app.py` uses a fixed local API URL. To make the deployed UI call the Render API, make this small edit:

At the top of `ui/app.py`, add:

```python
import os
```

Replace:

```python
DEFAULT_API = "http://127.0.0.1:8000"
```

with:

```python
DEFAULT_API = os.getenv(
    "GSTSARAL_API_URL",
    "http://127.0.0.1:8000",
)
```

The `render.yaml` sets `GSTSARAL_API_URL` for the UI service.

## 4. Record the actual deployment URL

After deployment succeeds, add the actual UI and API URLs to the root `README.md`. Do not leave the example URLs if Render assigned different ones. A ready-to-edit example is in `README-ADDITIONS.md`.

Also copy the actual URLs and deployment date into your project tracker using `TRACKER-UPDATE.md`.

## 5. Create and merge one feature-branch PR after CI is green

Run these commands from PowerShell at your repository root:

```powershell
git checkout -b feature/ci-render-deployment
git add .github/workflows/ci.yml render.yaml README.md ui/app.py
git commit -m "Add CI workflow and Render deployment"
git push -u origin feature/ci-render-deployment
```

Then:

1. Open `https://github.com/Kulkarni-Suyog/Gen-AI`.
2. Select **Compare & pull request** for `feature/ci-render-deployment`.
3. Create the pull request into your default branch.
4. Wait until the **GSTSaral CI** check is green.
5. If it fails, open the failed check, fix the reported error, commit, and push again.
6. Merge the PR only after CI is green.

Do not mark the PR as merged in your tracker until GitHub shows that it is merged.

## 6. Notes

- Render free services may sleep when unused and can take time to wake up.
- The Day 9 app builds its Chroma index on startup. First deployment can take longer while the embedding model is downloaded and the index is built.
- The API's `/health` endpoint does not require a Groq key. The key is needed for LLM answer generation.
- This package configures CI and deployment; it cannot create a GitHub PR, merge it, or publish a real live URL on your behalf.
