# docker-postgresql-gcp-workshop
Workshop Codespaces
## docker<br >
1. docker is a containerization software, means can create container to let us isolate software like simple version of virtual machines.<br >
2. `docker` vs. `.venv`:
   1. `.venv` have same os as system, only different in `Python version` and `dependencies`<br >
      1. `packages` vs. `dependencies`:<br >
         1. `package` is an object (a bundle of code, e.g. module, library)<br >
         2. `dependency` is a relationship (the state of relying on another piece of code)<br >
         3. `package` becomes `dependency` when my code need that `package` to run, e.g. `import pandas as pd` (pandas is a dependency of my code)<br >
   2. `docker` have different `os`, `Python version`, and `dependencies`<br >
4. a docker image is a snapshot of a container, which we can run our data pipeline in it. Additionally, we can export docker images to cloud service, e.g. AWS or Google Cloud Platform (GCP) and run our container on it.<br >
5. `docker --version`		#check if docker installed and version<br >
6. `docker run -it ubuntu`	#docker use ubuntu image to create a container with ubuntu and open terminal for user to interact<br >
  1). `-i` = interactive	#keep Standard Input (STDIN) open for user to input<br >
  2). `-t` = TTY = TeleTYpewriter	#allocate virtual terminal for user to input<br >
  
7. Ctrl + D		#exit current docker container<br >
8. After exit container, any changes inside containers won't be saved, this is why we call docker is <ins>stateless</ins><br >
9. `docker run -it python:3.13.11-slim`<br >
  1). docker run python:3.13.11-slim image and start coding by python<br >
  2). python is image name, 3.13.11-slim is a tag<br >
  3). name + tag = full image name<br >

10. `docker run -it --entrypoint=bash python:3.13.11-slim`<br >
  1). change entry point python => bash, so we can type command in command prompt<br >
  This is a way to change python version by using docker<br >

11. `docker ps`		#list only <ins>current running</ins> containers<br >
12. `docker ps -a`	#list <ins>all/ins> container that are executable(include stopped one)<br >
13. `docker ps -aq`	#only list all container <ins>IDs</ins><br >
  1). `-a` = all	#show all containers<br >
  2). `-q` = quiet	#only return ID<br >
14. `docker rm $(docker ps -aq)`		# remove all containers by IDs<br >
  1). first run inner substitution to get all container IDs<br >
  2). then run outer to remove all container by IDs<br >

15. `docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11-slim`:<br >
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
  4. uv lesson learned:
     1. `uv run python --version` means: uv execute command <ins>inside the project virtual environment</ins>.
### Python intepreter selection<br >
To change python intepreter in vs code:<br >
  1. `uv run which python` in folder and copy `python directory`<br >
  2. `ctrl + shift + p` and type: <ins>Python: select interpreter</ins><br >
  3. click: `Enter interpreter path`<br >
  4. click: `Find`<br >
  5. paste `python directory` from `uv run which python`<br >
  6. select `Python` in `.venv/bin/python`<br >
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
   2. `-t test:pandas` means Docker build an image from Dockerfile with `<repository_name>:<tag_name/version_name>` as `test:pandas` (can be `test:v1`, `test:v2`...etc.)<br >
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
## Run postgreSQL on Docker:<br >
1. Q: Why Docker can run PostgreSQL without installation?<br >
   A: Docker has library Docker Hub which includes <ins>PostgreSQL image</ins>, so Docker can run PostgreSQL without installation.<br >
2. Terminal run Docker container with PostgreSQL database:
3. ```
   docker run -it --rm \
   -e POSTGRES_USER="root" \
   -e POSTGRES_PASSWORD="root" \
   -e POSTGRES_DB="ny_taxi" \
   -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
   -p 5432:5432 \
   postgres:18
   ```
   1. `-e` = set environment variables, e.g. `POSTGRES_USER=<username>`, `POSTGRES_PASSWORD=<password>`, `PROSGRES_DB=<database name>`
   2. `-v` = create a volume, syntax: `-v [folder in host machine]:[folder in container]`
      1. 5W1H Docker Volume:
         1. What is Docker Volume? Docker Volume is a persistent exist folder to map to container and let postgres store data on host machine.
         2. Why we use Docker Volume? To prevent postgres store data in container because the data will disappear if the container updated, stopped, or deleted.
         3. Who use Docker Volume? Data engineer (to store data as local data warhouse), DevOps (to store log data, application states, configuration data for deployment)
         4. When we use Docker Volume? When we need application "always remember data" over time (called stateful application)
         5. Where to store Docker Volume? local host machine: `$(pwd)/[folder_name]`, inside container: `/var/lib/postgresql/data` (local host machine will create new folder if not exist)
         6. How does docker volume work? Docker volume setup the local host machine directory, so everytime when postgreSQL save data inside container, the docker intercept it and save data to the local host machine directory.
   3. `-p` = map host port to container port, syntax: `-p [host port]:[container port]`, when setup `pgcli`, use <ins>host port</ins>
   4. `postgres:18` = use PostgreSQL version 18
   5. lesson learned:
      1. Issue: `/var/lib/postgresql/data` vs. `/var/lib/postgresql` (note: postgres:18+ upgrade and only require `/var/lib/postgresql`, no /data refer<sub>[1]</sub>
      2. Explain: `/var/lib/postgresql/data` is the default folder where postgresql store data. `/var/lib/postgresql` is the parent folder also include /data folder, so docker will create a `/data` folder in local machine folder.
      3. Reason to use `/var/lib/postgresql/data`:
         1. Precision, to only store data from PostgreSQL and exclude server log and configurations
         2. Avoid Permission Conflict, if set volume from `/var/lib/postgresql`, it may trigger permission conflict when other system try to write into `/var/lib/postgresql`
      4. Final solution: Since PosgreSQL officially upgrade and now only require `/var/lib/postgresql` in `-v`<sub>[1]</sub>
## Run pgcli for Postgres<br >
1. add pgcli in development dependencies: `uv add --dev pgcli`
2. run pgcli and link to Postgres: `uv run pgcli -h localhost -p 5432 -u root -d ny_taxi`
3. 5W1H pgcli:
   1. What is pgcli? pgcli is postgresql command line tool
   2. Why use pgcli? pgcli has auto-completion and syntax highlight to reduce typo and speed up querying, which psql doesn't have these features.
   3. Who use pgcli? Data engineer & analyst to query database.
   4. When use pgcli? Development & Debugging to verify pipeline successfully run, check schema definitions, or test queries.
   5. Where does pgcli live? pgcli live on local host machine, not in docker container.
   6. How to use pgcli to connect postgreSQL in docker container?
      1. `pgcli -h localhost -p 5432 -u root -d ny_taxi`
      2. syntax: `pgcli -h [the host] -p [local machine port] -u [postgres username] -d [postgres database name]`
      3. Because `[the host]` for pgcli is local machine, so it's `-h localhost`
4. Lesson learned:
   1. Issue: To turn on Multiline in pgcli, press F3. vs code has keyword binding F3 = search in terminal, so press F3 won't turn on Multiline in pgcli.
   2. Solution:
      1. Ctrl+k then Ctrl+s to open keyboard shortcut
      2. Search for terminal.find
      3. Change keybinding from F3 to ctrl+shift+f
      4. Restart vs code, and restart pgcli, then press F3 to turn on Multiline.
5. Lesson learned: `uv add --dev pgcli` means: uv add pgcli in dev group <ins>inside the project virtual environment</ins>.
## Quick PostgreSQL Demo:
```
\dt
--   List tables

CREATE TABLE test (
   id INTEGER,
   name VARCHAR(50)
);
--   Create a test table with schema

INSERT INTO test VALUES(
   1, 'Hello Docker'
);
--   Insert data

\q
--   exit pgcli = ctrl+D
```
## Jupyter notebook
To retrieve and preprocess data, we execute Jupyter notebook, process data, and pass the processed data to PostgreSQL.
1. Jupyter notebook setup:
   1. Install Jupyter: `uv add --dev jupyter`
   2. Create a Jupyter notebook: `uv run jupyter notebook`
2. Jupyter notebook code:
   1. import dependencies:
   ```
   import pandas as pd
   from sqlalchemy import create_engine
   from tqdm.auto import tqdm
   ```
   2. Define Macro to download and normalize data type in schema
   ```
   # Macro for download data
   DATA_SOURCE_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
   DATA_VERSION = 'yellow_tripdata_2021-01.csv.gz'
   # Macro for correct schema's data type
   DTYPE = {
      "VendorID": "Int64",
       "passenger_count": "Int64",
       "trip_distance": "Float64",
       "RatecodeID": "Int64",
       "store_and_fwd_flag": "str",
       "PULocationID": "Int64",
       "DOLocationID": "Int64",
       "payment_type": "Int64",
       "fare_amount": "Float64",
       "extra": "Float64",
       "mta_tax": "Float64",
       "tip_amount": "Float64",
       "tolls_amount": "Float64",
       "improvement_surcharge": "Float64",
       "total_amount": "Float64",
       "congestion_surcharge": "Float64",
   }
   PARSE_DATE = [
      "tpep_pickup_datetime",
      "tpep_dropoff_datetime"
   ]
   ```
   3. Double check if pandas exist
   ```
   pd.__file__
   ```
   4. Download ny_taxi data
   ```
   df = pd.read_csv(DATA_SOURCE_PREFIX+DATA_VERSION)
   ```
   5. I found out the data type in "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime" are incorrect. The "VendorID" should be Int64, not float, and "tpep_pickup_datetime", "tpep_dropoff_datetime" should be datetime, not string, so I used Macro to download data again with data type specified.
   ```
   df = pd.read_csv(
      DATA_SOURCE_PREFIX+DATA_VERSION,
      dtype=DTYPE,
      parse_dates=PARSE_DATE,
   )
   ```
   6. Then, I want to pass preprocessed data to postgres. For that, I installed SQLAlchemy.
   ```
   In jupyter notebook, use uv to add dependencies: SQLAIchemy, psycopg2-binary
   !uv add sqlalchemy
   !uv add psycopg2-binary
   ```
   7. To insert data into postgres: Setup sqlalchemy engine to connect local postgres database.
   syntax: `sqlalchemy.create_engine('<postgresql>://<username>:<password>@<host>:<port>/<database>')`
   ```
   # setup sqlalchemy engine
   engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
   ```
   8. Preview SQL statement to create table.
   ```
   # 1. get schema from dataframe df,
   # 2. get table name from name='yellow_taxi_data',
   # 3. generate "postgresql" statement based on con=engine where engine was created for postgresql database in docker
   print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
   ```
   9. Create empty table with schema only (column name + dtype)
   ```
   # df.head(0) return only column names and data types (=schema)
   df.head(0).to_sql(
      name='yellow_taxi_data',
      con=engine,
      if_exists='replace',
   )
   ```
   10. I want to insert data in batches, so I downloaded data with chunksize to get dataframe iterator (dtype=TextFileReader)
   ```
   df_iter = pd.read_csv(
      DATA_SOURCE_PREFIX+DATA_VERSION,
      dtype=DTYPE,
      parse_dates=PARSE_DATE,
      iterator=True,
      chunksize=100000,
   )
   ```
   - Lesson learned:
     - Issue: first trunk of data missed.
         ```
         df_iter = pd.read_csv(
            url,
            dtype=DTYPE,
            parse_dates=PARSE_DATE,
            iterator=True,
            chunksize=chunksize,
         )
      
          # create empty table with schema only (column name + dtype)
          first_trunk = next(df_iter)
          first_trunk.head(0).to_sql(
              name=target_table,
              con=engine,
              if_exists='replace',
          )
          # insert chunk of data
          for df_chunk in tqdm(df_iter):
              df_chunk.to_sql(
                  name=target_table,
                  con=engine,
                  if_exists='append'
         )
         ```
      - Reason: `pd.read_csv(..., iterator=True)` returns an iterator, which <ins>only moves forward and never resets</ins>. After `first_trunk = next(df_iter)`, `df_iter` already move forward 1 trunk. Therefore, `for df_chunk in tqdm(df_iter):` starts from <ins>second trunk of data</ins>.
      - Fix: Add first trunk of data `.to_sql` additionally.
         ```
         first_trunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append',
         )
         ```
   11. Install tqdm, and from tqdm.auto import tqdm to see progress of inserting data
   ```
   !uv add tqdm
   ```
   12. Finally, I pass data into postgres database
   ```
   for df_chunk in tqdm(df_iter):
      df_chunk.to_sql(
         name='yellow_taxi_data',
         con=engine,
         if_exists='append'
      )
   ```
## Convert jupyter notebook to python script
1. Jupyter notebook provides early stage data pipeline prototyping by interactive platform. When pipeline development almost done, I tend to convert Jupyter notebook to python script for production phase.
2. Jupyter notebook is <ins>plain text file as a JSON object</inns> and should be converted into python script for production.
3. Syntax: `uv run jupyter nbconvert --to=script notebook.ipynb`
     1. uv run command `jupyter nbconvert --to=script notebook.ipynb` to convert `notebook.ipynb` to python script.
     2. `jupyter` is the entry point for Jupyter package.
     3. `nbconvert` is the tool for Notebook Convert.
     4. `--to=script` is a flag of nbconvert to export input file as a python script.
     5. `notebook.ipynb` is the input file name.
## Rename python script
`mv notebook.py ingest_data.py`
1. Syntax: `mv [source] [destination]`
2. `mv` can be both rename and move file:
   1. If destination is a new file name => rename<br >
      `mv notebook.py ingest_data.py`
   2. If destination is an exist directory => move<br >
      `mv notebook.py /src/scripts/`
   3. If destination is exist directory + new file name => move + rename<br >
      `mv notebook.py /src/scripts/ingest_data.py`
## Use `click` to parse the arguments:
1. uv add click into dependency: `uv add click`
2. code:
   ```python
   import click
   
   @click.command()
   @click.option('--pg-user', default='root', help='PostgreSQL username')
   @click.option('--pg-pass', default='root', help='PostgreSQL password')
   @click.option('--pg-host', default='localhost', help='PostgreSQL host')
   @click.option('--pg-port', default='5432', help='PostgreSQL port')
   @click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
   @click.option('--year', default=2021, type=int, help='Year of the data')
   @click.option('--month', default=1, type=int, help='Month of the data')
   @click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
   @click.option('--target-table', default='yellow_taxi_data', help='Target table name')
   def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
   ```
3. terminal execute:
   ```bash
   uv run python ingest_data.py \
   --pg-user=root \
   --pg-pass=root \
   --pg-host=localhost \
   --pg-port=5432 \
   --pg-db=ny_taxi \
   --target-table=yellow_taxi_trips \
   --year=2021 \
   --month=1 \
   --chunksize=100000
   ```
### Verify Data in pgcli:
1. Start pgcli: `uv run pgcli -h localhost -p 5432 -u root -d ny_taxi`
2. verify data in postgreSQL: 
```sql
SELECT COUNT(*)
FROM yellow_taxi_data;
-- Count records

SELECT *
FROM yellow_taxi_data
LIMIT 10;
-- View sample data

SELECT
   DATE(tpep_pickup_datetime) AS pickup_date,
   COUNT(*) as trips_count,
   AVG(total_amount) AS avg_amount
FROM
   yellow_taxi_data
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY pickup_date;
-- Sample Analytics
```
## pgAdmin - a replacement database management tool for pgcli
pgAdmin is a web-based tool to replace pgcli when the query become complicated.
### Run pgAdmin container:
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```
1. Question: In `-v pgadmin_data:/var/lib/pgadmin`, where does pgadmin_data store in linux?
   - Answer: `pgadmin_data` means docker store data in docker internal file system.
   - Reason: pgadmin data are application setting data, e.g. which port to connect, what's the connection host, username, and password. Users will type in these data every time when login pgAdmin, so we don't have to keep this data outside of docker.
2. Lesson learned: There are <ins>Two type</ins> of volume:
   1. <ins>pgadmin_data</ins>:/var/lib/pgadmin: <ins>Named Volume</ins>: only <ins>provide volume name</ins>, and docker store data inside internal file system. Reason to use Named Volume: Only need docker hold application setting/preference.
   2. <ins>$(pwd)/ny_taxi_data</ins>:/var/lib/postgresql: <ins>Bind Mount</ins>: volume binds a specific folder in localhost machine , and docker store data inside local folder.
3. Question: Why `dpage/pgadmin4` instead of `pgadmin4`, like `postgres:18`?
   - Answer: There are 2 type of Images:
     1. Official Image: Docker maintain a set of official images which I can run with their <ins>single name</ins>, e.g. postgres, python, ubuntu...etc.
     2. Third-party Image: Third-party companies publish image follow standard format `<username>/<repository_name>`, e.g. <ins>dpage</ins> is third-party username of Dave Page which publish tool pgAdmin, and <ins>pgadmin4</ins> is the specific repository name contain pgAdmin 4 image. 
## Docker Network
The postgres container and pgAdmin container are isolated, means pgAdmin can't see postgres container. For pgAdmin to connect postgres, we need Docker Network.
1. Docker network commands:
   ```bash
   docker network create pg-network
   # Create a docker network called pg-network
   docker network ls
   # List all docker networks
   docker network rm pg-network
   # Remove pg-network from docker network
   ```
2. First, create a docker network:
   ```bash
   docker network create pg-network
   ```
3. To connect pgAdmin to postgres, we need to rerun pgAdmin and postgres containers and add docker network variables:
   1. Rerun Postgres on docker network in one terminal:
      ```bash
      docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
      -p 5432:5432 \
      --network=pg-network \
      --name pgdatabase \
      postgres:18
      ```
      - Question: What does `pgdatabase` mean in `--network=pg-network \ --name pgdatabase \`?
      - Answer: `--name pgdatabase` is the name of postgres in pg-network. When pgAdmin want to connect postgres in pg-network, I set host as pgdatabase in pgAdmin.
   2. Run pgAdmin on the same docker network in another terminal:
      ```bash
      docker run -it \
      -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
      -e PGADMIN_DEFAULT_PASSWORD="root" \
      -v pgadmin_data:/var/lib/pgadmin \
      -p 8085:80 \
      --network=pg-network \
      --name pgadmin \
      dpage/pgadmin4
      ```
   3. Connecting setting for pgAdmin to PostgreSQL database:
      1. Click <ins>Port</ins> in vs code, click <ins>Add Port</ins>, and type in <ins>8085</ins>
      2. Login with email: <ins>admin@admin.com</ins>, password: <ins>root</ins>
      3. Right-click "Servers" → Register → Server
      4. Configure server pgAdmin to connect database in postgres container:
         - General tab: Name: Local Docker
         - Connection tab:
           - Host: pgdatabase (the postgres container name in docker network (pg-network))
           - Port: 5432
           - Username: root
           - Password: root
      5. Save
## Dockerizing the Ingestion Script (add ingest_data.py into Dockerfile)
To add ingest_data.py in Dockerfile and run to ingest ny taxi data into postgres, all I need to do is to change the last 2 lines of Dockerfile:
### Edit Dockerfile:
```dockerfile
# copy source code
COPY ingest_data.py ingest_data.py

# define first command when run container
ENTRYPOINT ["python", "ingest_data.py"]
```
Because all dependencies are in pyproject.toml and uv.lock which is already included above: `COPY "pyproject.toml" "uv.lock" ".python-version" ./`, I only have to change the source code copy and entrypoint editing.<br >
1. Question: Which parameter of `docker run` command specify using Dockerfile?
   - Answer:
     1. `docker run` specify <ins>docker image</ins> <name>:<tag>, e.g. data_ingest:v001. `docker run` doesn't specify Dockerfile.
     2. `docker build` automatically use <ins>local Dockerfile</ins>, e.g. `docker build -t taxi_ingest:v001 .`
2. Question: Explain: Multi-stage build pattern copies uv from official image
   - Answer: The image created by docker build includes multi-stage pattern copies and dependency installed in Dockerfile.
3. Question: Explain: Copying dependency files before code improves Docker layer caching
   - Answer: Dockerfile is layer caching, means only rerun the update lines and <ins>the lines under update line</ins>. Because `COPY ingest_data.py ingest_data.py` at the bottom line, `docker build` can skip above lines and only rerun the very bottom 2 lines.
### Build the Docker Image
```bash
docker build -t taxi_ingest:v001 .
```
### Run Containized Ingestion
```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 \
  --month=1 \
  --chunksize=100000
```
1. Question: why `--network=pg-network` goes before the image `taxi_ingest:v001`?
   Answer: `--network` have to go before docker image name:
   ```
   --network=pg-network \ 
   taxi_ingest:v001 \

   --network=pg-network \
   --name=pgdatabase
   postgres:18

   --network=pg-network \
   --name=pgadmin \
   dpage/pgadmin4
   ```
2. Question: Why `--pg-host=pgdatabase`, not `--pg-host=localhost`?
   Answer: Because docker postgres in pg-network called pgdatabase, `docker run taxi_ingest:v001` have to specify `--pg-host=pgdatabase` not localhost to ingest data to postgres in pg-network.


## Reference<br >
1. [Upgrading between major versions?](https://github.com/docker-library/postgres/issues/37#issuecomment-4435452264)




