# Dockerfile always start with FROM: What do we base on and we will build Docker image on it.
FROM python:3.13.11-slim

# execute command to setup our image by installing prerequisites, e.g. pandas, pyarrow.
RUN pip install pandas pyarrow

# setup working directory inside the container
WORKDIR /app

# copy the script to the container. syntax: COPY [source] [destination]
# source . means current directory in host machine = everything in this folder
# destination . means current directory in docker image = keep original filename
COPY pipeline.py .

# define the "first command" to run when the container runs
# this ENTRYPOINT will execute "python pipeline.py"
ENTRYPOINT ["python", "pipeline.py"]