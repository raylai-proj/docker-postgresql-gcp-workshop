# docker-postgresql-gcp-workshop
Workshop Codespaces
## docker<br >
1. docker is a containerization software, means can create container to let us isolate software like simple version of virtual machines.<br >
2. a docker image is a snapshot of a container, which we can run our data pipeline in it. Additionally, we can export docker images to cloud service, e.g. AWS or Google Cloud Platform (GCP) and run our container on it.<br >
3. `docker --version`		#check if docker installed and version<br >
4. `docker run -it ubuntu`	#docker use ubuntu image to create a container with ubuntu and open terminal for user to interact<br >
  1). `-i` = interactive	#keep Standard Input (STDIN) open for user to input<br >
  2). `-t` = TTY = TeleTYpewriter	#allocate virtual terminal for user to input<br >
  
5. Ctrl + D		#exit current docker container<br >
6. After exit container, any changes inside containers won't be saved, this is why we call docker is <ins>stateless</ins><br >
7. `docker run -it python:3.13.11-slim`<br >
  1). docker run python:3.13.11-slim image and start coding by python<br >
  2). python is image name, 3.13.11-slim is a tag<br >
  3). name + tag = full image name<br >

8. `docker run -it --entrypoint=bash python:3.13.11-slim`<br >
  1). change entry point python => bash, so we can type command in command prompt<br >
  This is a way to change python version by using docker<br >

9. `docker ps`		#list only <ins>current running</ins> containers<br >
10. `docker ps -a`	#list <ins>all/ins> container that are executable(include stopped one)<br >
11. `docker ps -aq`	#only list all container <ins>IDs</ins><br >
  1). `-a` = all	#show all containers<br >
  2). `-q` = quiet	#only return ID<br >
12. `docker rm $(docker ps -aq)`		# remove all containers by IDs<br >
  1). first run inner substitution to get all container IDs<br >
  2). then run outer to remove all container by IDs<br >

13. `docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11-slim`:<br >
  - docker use <ins>Volume Mount</ins> to link files from local computer into docker container<br >
  - with <ins>Volume Mount</ins>, advantage:<br >
    1. we can execute files outside of container<br >
    2. when local files change, it change in container immediately, so we don't need to exit, edit file, and rerun a new container<br >
  - <ins>Volume</ins> in CS means data storage unit, we use <ins>Volume</ins> means it is independent from container, and <ins>Volume Mount</ins> means we mount data storage unit from local to container<br >
  - To keep code organized, we use <ins>/app</ins> or <ins>/src</ins> to link local directory, e.g. `-v $(pwd)/test:/app/test`<br >
## Venv and Data Pipeline<br >
### sys.argv<br >
```
import sys
system_argv = sys.argv
month = int(sys.argv[1])
```
The `sys.argv` returns parameters in list:<br >
  1. First parameter = script name we run<br >
  2. Rest = rest parameters we inpu<br >
  3. e.g. `(venv) uv run pipeline.py 12`: `sys.argv = ['pipeline.py', 12]`<br >
### VS code extension: Python Debugger<br >
- A useful hint: <ins>Python Debugger Extension</ins> prompt user with syntax.<br >
### uv<br >
uv is a python package manager, like pip<br >
  1. To install uv: `pip install uv`<br >
  2. To initialize python project with uv: `cd` in the folder and `uv init --python=3.13`<br >
  3. To create <ins>.venv</ins> folder: uv will create .venv folder for activate virtual environment when either<br >
    1. when the first time run `uv run python pipeline.py` to execute file.<br >
    2. or when the first time run `uv add pandas pyarrow` to install library in venv.<br >
### Python intepreter selection<br >
To select python intepreter in vs code:<br >
  1. `ctrl + shift + p` and select <ins>python intepreter</ins><br >
  2. select python version in .venv<br >
### Include <ins>parquet</ins> file in .gitignore<br >
1. I can add `*.parquet` in .gitignore (whereever in file)<br >
2. Wait for .parquet file to turn gray, means git exclude it in record.<br >
## Dockerfile<br >
### 5W1H<br >
1. What is Dockerfile: Dockerfile is a <ins>text document</ins> contains script of instructions for building a Docker image.<br >
2. Why do we use Dockerfile:<br >
   1. To <ins>automatically</ins> configure system environment instead of do it manually.<br >
   2. To create <ins>absolute replicate</ins> of system environment, so local machine and cloud production will get same result when running Python script.<br >
3. Who use Dockerfile:<br >
   1. Data engineer uses Dockerfile to orchestrate (manage, schedule, monitor) data pipeline on cloud service.<br >
   2. Software engineer uses Dockerfile to build CI/CD pipeline which <ins>automatically test, build, and deploy applications</ins> on cloud service.<br >
4. When to use Dockerfile:<br >
   1. During development: <ins>when adding new system dependency</ins>, e.g. install new python library, we add the new library in Dockerfile.<br >
   2. During deployment or CI/CD: when pushing latest code, the <ins>Dockerfile gets updated and automatically compiles a new environment</ins>.<br >
5. Where to use Dockerfile:<br >
   1. Version Control (Git): Dockerfile saved in <ins>root directory of project</ins> as a environment configuration.<br >
6. How to use Dockerfile:<br >
   1. Dockerfile use <ins>Layered Cache</ins>: means if one line change, rest below lins have to <ins>rebuild</ins>, so Dockerfile follows <ins>least-to-most frequent change</ins> order.<br >
   2. General order of commands in Dockerfile:<br >
   ```
   FROM
   WORKDIR
   ENV
   RUN (install OS dependencies)
   COPY (App dependencies only)
   RUN (install App dependencies)
   COPY (rest source code)
   RUN (any complication)
   ENTRYPOINT
   ```
   3. Dockerfile syntax:<br >
      1. `FROM python:3.13.11-slim`: Dockerfile always start with <ins>FROM</ins>: means what do we base on and we will build Docker image base on it.<br >
      2. `WORKDIR /app`: Setup work directory in the container.<br >
      3. `ENV PATH="/app/.venv/bin:$PATH"`:<br >
         1. Setup environment variable for container: prepend `/app/.venv/bin` in front of original `$PATH`, so system look up python version from virtual environment folder first.<br >
         2. `$PATH` in linux refer to a list of folders, which are in PATH environment variable.<br >
            1. The `$PATH` variable is separated by `:` which is the delimiter<br >
            2. The `$PATH` variable has order of a list directory, the system will follow the order to look up command in each directory.<br >
      4. `RUN pip install pandas pyarrow`: Run command to setup our image by installing prerequisites, e.g. pandas, pyarrow.<br >
      5. `COPY pipeline.py .`:<br >
         1. `COPY [source] [destination]`: Copy the script to the container.<br >
         2. `COPY . .`:<br >
            - Source `.` means current directory in host machine = everything in this folder.<br >
            - Destination `.` means current directory in docker image = keep original filename.<br >
         3. `COPY "pyproject.toml" "uv.lock" ".python-version" ./`<br >
            1. In linux, <ins>the last argument is always `[destination]`</ins><br >
            2. `.` means current folder, `/` confirms destination is a directory, `./` is a safety way to say `[destination]` is a directory<br >
         4. `COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/`<br >
            1. With `--from` flag, docker download uv image from `ghcr.io/astral-sh/uv:latest`<br >
            2. In downloaded uv image, docker copy `/uv` and `/uvx` files to `/bin/` folder (destination)<br >
      6. `ENTRYPOINT ["python", "pipeline.py"]`:<br >
         1. `ENTRYPOINT` define the first command to run when the container runs<br >
         2. This `ENTRYPOINT` will execute `python pipeline.py`<br >
### Dockerfile lesson learned:<br >
1. `RUN uv sync --locked`:<br >
   - Check and if pyproject.toml and uv.lock <ins>matched</ins>: if matched, install dependencies from uv.lock, if no, build fail.<br >
2. `uv sync --locked` vs. `uv sync --frozen`:<br >
   - `--locked`: check if pyproject.toml and uv.lock matched before installing dependencies from uv.lock. <ins>If not matched, build fail.</ins> (good for /test before upload)<br >
   - `--frozen`: assume pyproject.toml and uv.lock matched and <ins>directly install dependencies from uv.lock.</ins> (good for docker)<br >
3. `docker build -t test:pandas .`:<br >
   1. `.` means Docker looks for Dockerfile in current directory, if you have line like COPY in Dockerfile, e.g. `COPY . .`, the first `.` = `.` in `docker build -t test:pandas .` = current directory<br > 
4. After `docker build -t test:pandas .`, check by `docker image ls`, remove image by `docker rmi <IMAGE>`<br >
   1. `docker build`: docker build create an image (bludprint)<br >
   2. `docker run`: docker run create a container (instance)<br >
5. `docker rm $(docker ps -aq)` vs `docker run -it --entrypoint=bash --rm test:pandas` vs `docker container prune --filter "until=24h"`<br >
   1. `docker rm $(docker ps -aq)`: Here `rm` is `<command>` to remove container, syntax: `docker <command> <options> <target>`<br >
   2. `docker run -it --entrypoint=bash --rm test:pandas`: Here `--rm` is `<option/flag>` and `test:pandas` is `<target>`: docker run container `test:pandas` with options `-it`=interactive, `--entrypoint=bash`=enterypoint as bash, and `--rm`=remove the container once stopped.<br >
   3. `docker container prune --filter "until=24h"`: prune remove container with filter only stopped for more than 24 hours.<br >
6. `docker run -it --entrypoint-bash --rm test:pandas`: `test` is image name, `pandas` is tag name, `test:pandas` will be the whole thing how it will be called.<br >
### Latest Dockerfile:<br >
```
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
```


