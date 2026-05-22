# # Dockerfile always start with FROM: What do we base on and we will build Docker image on it.
# FROM python:3.13.11-slim

# # execute command to setup our image by installing prerequisites, e.g. pandas, pyarrow.
# RUN pip install pandas pyarrow

# # setup working directory inside the container
# WORKDIR /app

# # copy the script to the container. syntax: COPY [source] [destination]
# # source . means current directory in host machine = everything in this folder
# # destination . means current directory in docker image = keep original filename
# COPY pipeline.py .

# # define the "first command" to run when the container runs
# # this ENTRYPOINT will execute "python pipeline.py"
# ENTRYPOINT ["python", "pipeline.py"]

# Dockerfile with uv
# docker image based on python:3.13.11-slim
FROM python:3.13.11-slim

# install uv by copying uv binary from official distroless Docker image
# system package manager dependency
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set up work directory in container
WORKDIR /app

# ENV setup environment variable PATH
# Add virtual environment path into PATH, so we can use packages installed in venv, and refer to variable in venv first
ENV PATH="/app/.venv/bin:$PATH"

# copy app dependency to directory /app WORKDIR (for better layer caching)
# ./ confirm the destination is a folder
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# run command uv sync --locked to install dependencies
# --locked checked and make sure pyproject.toml and uv.lock matched; if not matched, build fails
RUN uv sync --locked

# copy source code
COPY pipeline.py pipeline.py

# define first command when run container
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
