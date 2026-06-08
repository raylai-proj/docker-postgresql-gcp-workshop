# docker-postgresql-gcp-workshop
Workshop Codespaces
## 1. Docker<sub>[1]</sub><br >
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
## 2. Venv and Data Pipeline<sub>[2]</sub><br >
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
## 3. Dockerfile<sub>[3]</sub><br >
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
6. `docker run -it --entrypoint=bash --rm test:pandas`: `test` is image name, `pandas` is tag name, `test:pandas` will be the whole thing how it will be called.<br >
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
## 4. Running PostgreSQL with Docker<sub>[4]</sub><br >
1. Q: Why Docker can run PostgreSQL without installation?<br >
   A: Docker has library <ins>Docker Hub which includes PostgreSQL image</ins>, so Docker can run PostgreSQL without installation.<br >
2. Docker run Postgre container setup:<br >
   1. Create a new directory to store Postgre data:<br >
   ```console
   mkdir ny_taxi_postgres_data
   ```
   2. Docker run Postgre container:<br >
   ```console
   docker run -it --rm \
   -e POSTGRES_USER=root \
   -e POSTGRES_PASSWORD=root \
   -e POSTGRES_DB=ny_taxi \
   -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
   -p 5432:5432 \
   postgres:18
   ```
   3. syntax:<br >
      1. `-e` = set environment variables, e.g. `POSTGRES_USER=[username]`, `POSTGRES_PASSWORD=[password]`, `POSTGRES_DB=[database name]`<br >
      2. `-v` = create a <ins>volume</ins>, e.g. `-v [folder in host machine to store data]:[default folder in container to store postgres data]`<br >
         1. 5W1H Docker volume:<br >
            1. What is Docker volume? Docker volume is a persistent exist folder to map to container and let postgres store data on host machine.<br >
            2. Why we use Docker volume? To prevent data disappear. Default place to store postgres data in container will disappear when the container updated, stopped, or deleted.<br >
            3. Who use Docker volume? Data engineer (to store data as local data warehouse), DevOps (to store log data, application states, configuration data for deployment).<br >
            4. When we use Docker volume? When we need application <ins>always remember data</ins> over time (called stateful application)<br >
            5. Where does Docker volume store? At local host machine: `$(pwd)/[folder_name]`, In container: `/var/lib/postgres`<br >
            6. How does Docker volume work? Docker volume setup the local machine directory, so everytime whene postgres save data inside container, <ins>the docker intercept it and save data to the local host machine directory.</ins><br > 
         2. Lesson learned:<br >
            - Issue: Both recommendations `/var/lib/postgresql` vs. `/var/lib/postgresql/data` were saw when setting docker volume.<br >
            - Solution:<br >
              1. `postgres:18`: Use `/var/lib/postgresql`, in `postgres:18`, the official upgrade and now only require `/var/lib/postgresql` in `-v`.<sub>[5]</sub><br >
              2. `postgres:17` or lower: Use `/var/lib/postgresql/data`, in `postgres:17` or lower, the default folder where postgres store data at `/var/lib/postgresql/data`, so docker will store data into local machine instead of `/var/lib/postgresql/data`. This provide advantages:<br >
                 1. Precision, to only store data from postgres and exclude server log and configurations.<br >
                 2. Avoid Permission Conflict, if set volume from `/var/lib/postgresql`, it may trigger permission conflict when other system try to write into `/var/lib/postgresql`.<br >
      3. `-p` = map host port to container port, syntax: `-p [host port]:[container port]`. When setup `pgcli` to connect postgres server, use <inv>`[host port]`</inv>.<br >
      4. `-d` = detached mode: postgres will run in the background, and terminal won't constantly stream postgres server log.<br >
         1. If want to keep postgres server streaming log, <ins>Open the Second Terminal</ins> and problem solved.<br >
         2. In detached mode, postgres server stop when container stop. To stop container:<br >
            ```console
            docker ps    # to find container id
            docker stop [container_id]
            ```
      5. `postgres:18` = use PostgreSQL version 18.<br >
3. 5W1H `pgcli`<br >
   1. What is `pgcli`? `pgcli` is PostgreSQL Command Line Interface.<br >
   2. Why use `pgcli`? `pgcli` has <ins>auto-completion</ins> and <ins>syntax highlight</ins> to reduce typo and speed up querying, which `psql` doesn't have these features.<br >
   3. Who use `pgcli`? Data engineer & analyst to query database<br >
   4. When use `pgcli`? Development & Debugging to verify <ins>pipeline successfully run</ins>, <ins>check schema definitions</ins>, or <ins>test queries</ins>.<br >
   5. Where to install `pgcli`? Install `pgcli` in local machine, not in docker container.<br >
   6. How to use `pgcli` to connect postgreSQL in docker container?<br >
      ```console
      pgcli -h localhost -p 5432 -u root -d ny_taxi
      ```
      1. syntax: `pgcli -h [the host] -p [local machine port] -u [POSTGRES_USER] -d [POSTGRES_DB]`<br >
      2. Because `[the host]` for `pgcli` is local machine, `[the host]` = `localhost`<br >
5. `pgcli` lesson learned:<br >
   1. Issue: To turn on <ins>Multiline</ins> in `pgcli`, press <ins>F3</ins>, but vs code has keyword binding F3 = search in terminal, so press F3 won't turn on Multiline in `pgcli`<br >
   2. Solution:<br >
      1. <ins>Ctrl+k</ins> then <ins>Ctrl+s</ins> to open keyboard shortcut.<br >
      2. search for <ins>terminal.find</ins>.<br >
      3. change keybinding from <ins>F3</ins> to <ins>ctrl+shift+f</ins>.<br >
      4. restart vs code, next reconnect `pgcli`, then press F3 to turn on Multiline.<br >
7. `pgcli` query example (`\dt`, `\q`): <br >
   ```sql
   \dt
   --  List tables

   CREATE TABLE test (
     id INTEGER,
     name VARCHAR(50)
   );
   --  Create a test table

   INSERT INTO test VALUES (
     1, 'Hello Docker'
   );
   --  Insert data

   \q
   --  Exit pgcli = Ctrl+D
   ```
## 5. PostgreSQL<br >
This section decribes PostgreSQL database setup as well as query, phrase, operator,...etc. that differ from MySQL. To review basic SQL, refer to [SQL_review_note](https://github.com/raylai-proj/SQL_review_note)<sub>[6]</sub>.<br >
### 1. Download sample database and restore it to local database with pgcli and docker container:<br >
   1. Create new Postgres container for PostgreSQL workshop:<br >
      ```console
      mkdir dvdrental_postgres_data
      # create new folder for postgers server to store data in local machine

      docker run -it --rm \
      --name dvdrental_database \
      -e POSTGRES_USER=root \
      -e POSTGRES_PASSWORD=root \
      -e POSTGRES_DB=dvdrental \
      -v $(pwd)/dvdrental_postgres_data:/var/lib/postgresql \
      -p 5433:5432 \
      postgres:18
      ```
   2. Download sample database<sub>[7]</sub>:<br >
      1. Download sample data zip archive:<br >
         ```console
         curl -O https://neon.com/postgresqltutorial/dvdrental.zip
         ```
      2. Extract the zip to get the raw dvdrental.tar file:<br >
         ```console
         unzip dvdrental.zip
         ```
   3. `pgcli` create new database:<br >
      ```console
      uv run pgcli -p 5433 -u root -d dvdtental
      ```
      ```sql
      CREATE DATABASE dvdrental;
      --  create new empty database dvdrental
      \q
      --  exit = ctrl+D
      ```
   4. Restore downloaded database to new database:<br >
      ```console
      docker exec -i dvdrental_database pg_restore -U root -d dvdrental < dvdrental.tar
      ```
      1. `docker exec` vs. `docker run`: `docker run` create and start a new container, and `docker exec` reach a current running container to execute rest command.<br >
      2. Why `-i`, not `-it`, or omit `-i`: `-i` keeps the Standard Input (stdin) open, so the `dvdrental.tar` can stream from <ins>outside</ins> of container to <ins>inside</ins> of container. If use `-it`, the `-t` will wrap original data with ANSI Escape Codes which will corrupt the binary data stream. If omit `-i`, the Standard Input (stdin) will close before `dvdrental.tar` can stream to the inside of container, so `pg_restore` inside of container will fail.<br >
      3. what does `pg_restore < dvdrental.tar` do: The `<` is a <ins>Linux input redirection operator</ins> which pass data from `dvdrental.tar` through stdin (keep being opened by `-i`), go inside of container (dvdrental_database by `docker exec`), and finally stream to `pg_restore` to restore to database `-d dvdrental`.<br > 
   5. `pgcli` verify new downloaded database restored:<br >
      ```console
      uv run pgcli -p 5433 -u root -d dvdrental
      ```
      ```sql
      \dt
      --  List tables
      DESCRIBE customer;
      --  Show columns detail of table customer
      ```
### 2. Concatenation operator `||`<sub>[8][9]</sub>
```sql
SELECT
  first_name || ' ' || last_name AS full_name,
  email
FROM
  customer;

-- || is concatenation operator to concatenate columns
-- syntax: [column1] || [delimiter] || [column2]
```

## Reference
[1] [Introduction to Docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/01-introduction.md)<br >
[2] [Virtual Environments and Data Pipelines](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/02-virtual-environment.md)<br >
[3] [Dockerizing the Pipeline](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/03-dockerizing-pipeline.md)<br >
[4] [Running PostgreSQL with Docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/04-postgres-docker.md)<br >
[5] [Upgrading between major versions? #37](https://github.com/docker-library/postgres/issues/37#issuecomment-4435452264)<br >
[6] [SQL_review_note](https://github.com/raylai-proj/SQL_review_note)<br >
[7] [Install PostgreSQL Linux - Load the sample database](https://neon.com/postgresql/getting-started/install-postgresql-linux#load-the-sample-database)<br >
[8] [PostgreSQL SELECT](https://neon.com/postgresql/tutorial/select)<br >
[9] [Introduction to PostgreSQL CONCAT() function](https://neon.com/postgresql/string-functions/concat-function#introduction-to-postgresql-concat-function)<br >
