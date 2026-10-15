# Your Dockerfile. In this order:
#   - start FROM python:3.12-slim
#   - copy requirements.txt, pyproject.toml, llm/ and desk/ FIRST, then pip install
#     with --no-cache-dir. A code change must not reinstall every package.
#   - then copy everything else
#   - run as a user that is not root
#   - start uvicorn on 0.0.0.0 and the port in $PORT (default 8000)
