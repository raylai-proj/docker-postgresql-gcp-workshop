# docker-postgresql-gcp-workshop
Workshop Codespaces
## docker<sub>[1]</sub><br >
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
## Venv and Data Pipeline<sub>[2]</sub><br >
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
## Dockerfile<sub>[3]</sub><br >
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
## Run postgreSQL on Docker<sub>[4]</sub><br >
1. Q: Why Docker can run PostgreSQL without installation?<br >
   A: Docker has library Docker Hub which includes <ins>PostgreSQL image</ins>, so Docker can run PostgreSQL without installation.<br >
2. Terminal run Docker container with PostgreSQL database:
3. ```Bash
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
      1. Issue: `/var/lib/postgresql/data` vs. `/var/lib/postgresql` (note: postgres:18+ upgrade and only require `/var/lib/postgresql`, no /data refer<sub>[5]</sub>
      2. Explain: `/var/lib/postgresql/data` is the default folder where postgresql store data. `/var/lib/postgresql` is the parent folder also include /data folder, so docker will create a `/data` folder in local machine folder.
      3. Reason to use `/var/lib/postgresql/data`:
         1. Precision, to only store data from PostgreSQL and exclude server log and configurations
         2. Avoid Permission Conflict, if set volume from `/var/lib/postgresql`, it may trigger permission conflict when other system try to write into `/var/lib/postgresql`
      4. Final solution: Since PosgreSQL officially upgrade and now only require `/var/lib/postgresql` in `-v`<sub>[5]</sub>
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
```sql
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
## Jupyter notebook<sub>[6]</sub>
To retrieve and preprocess data, we execute Jupyter notebook, process data, and pass the processed data to PostgreSQL.
1. Jupyter notebook setup:
   1. Install Jupyter: `uv add --dev jupyter`
   2. Create a Jupyter notebook: `uv run jupyter notebook`
2. Jupyter notebook code:
   1. import dependencies:
   ```Python
   import pandas as pd
   from sqlalchemy import create_engine
   from tqdm.auto import tqdm
   ```
   2. Define Macro to download and normalize data type in schema
   ```Python
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
   ```Python
   pd.__file__
   ```
   4. Download ny_taxi data
   ```Python
   df = pd.read_csv(DATA_SOURCE_PREFIX+DATA_VERSION)
   ```
   5. I found out the data type in "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime" are incorrect. The "VendorID" should be Int64, not float, and "tpep_pickup_datetime", "tpep_dropoff_datetime" should be datetime, not string, so I used Macro to download data again with data type specified.
   ```Python
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
   ```Python
   # setup sqlalchemy engine
   engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
   ```
   8. Preview SQL statement to create table.
   ```Python
   # 1. get schema from dataframe df,
   # 2. get table name from name='yellow_taxi_data',
   # 3. generate "postgresql" statement based on con=engine where engine was created for postgresql database in docker
   print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
   ```
   9. Create empty table with schema only (column name + dtype)
   ```Python
   # df.head(0) return only column names and data types (=schema)
   df.head(0).to_sql(
      name='yellow_taxi_data',
      con=engine,
      if_exists='replace',
   )
   ```
   10. I want to insert data in batches, so I downloaded data with chunksize to get dataframe iterator (dtype=TextFileReader)
   ```Python
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
         ```Python
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
         ```Python
         first_trunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append',
         )
         ```
   11. Install tqdm, and from tqdm.auto import tqdm to see progress of inserting data
   ```Bash
   !uv add tqdm
   ```
   12. Finally, I pass data into postgres database
   ```Python
   for df_chunk in tqdm(df_iter):
      df_chunk.to_sql(
         name='yellow_taxi_data',
         con=engine,
         if_exists='append'
      )
   ```
## Convert jupyter notebook to python script<sub>[7]</sub>
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
   ```Bash
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
## pgAdmin - a replacement database management tool for pgcli<sub>[8]</sub>
pgAdmin is a web-based tool to replace pgcli when the query become complicated.
### Run pgAdmin container:
```Bash
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
   ```Bash
   docker network create pg-network
   # Create a docker network called pg-network
   docker network ls
   # List all docker networks
   docker network rm pg-network
   # Remove pg-network from docker network
   ```
2. First, create a docker network:
   ```Bash
   docker network create pg-network
   ```
3. To connect pgAdmin to postgres, we need to rerun pgAdmin and postgres containers and add docker network variables:
   1. Rerun Postgres on docker network in one terminal:
      ```Bash
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
      ```Bash
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
## Dockerizing the Ingestion Script (add ingest_data.py into Dockerfile)<sub>[9]</sub>
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
```Bash
docker build -t taxi_ingest:v001 .
```
### Run Containized Ingestion
```Bash
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
   ```Bash
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
## Docker Compose<sub>[10]</sub>
Docker Compose let me run multiple docker containers in the same time.
### docker-compose.yaml
1. Create docker-compose.yaml
   ```Bash
   touch docker-compoase.yaml
   ```
2. Add postgres and pgAdmin in docker-compose.yaml
   ```yaml
   services:
      pgdatabase:
         image: postgres:18
      environment:
         - POSTGRES_USER=root
         - POSTGRES_PASSWORD=root
         - POSTGRES_DB=ny_taxi
      volumes:
         - "./ny_taxi_postgres_data:/var/lib/postgresql:rw"
      ports:
         - "5432:5432"

      pgadmin:
         image: dpage/pgadmin4
      environment:
         - PGADMIN_DEFAULT_EMAIL=admin@admin.com
         - PGADMIN_DEFAULT_PASSWORD=root
      volumes:
         - "pgadmin_data:/var/lib/pgadmin"
      ports:
         - "8085:80"

   volumes:
      pgadmin_data:
   ```
   1. Question: What does rw mean in `./ny_taxi_postgres_data:/var/lib/postgresql:rw` in docker-compose.yaml:
      - Answer: rw means permission to both read from and write to the volume.
   2. Question: How to bind mount ny_taxi data to local directory?
      - Answer: To store data locally with bind mount, use `./`, not `$(pwd)`. The code should be looked like 
      ```yaml
      volumes:
      	- "./ny_taxi_postgres_data:/var/lib/postgresql:rw"
      ```
3. Run docker-compose.yaml
   `docker-compose up`
- Docker compose commands:
  ```Bash
  docker-compose up
  # run docker compose
  docker-compose down
  # shut down docker compose
  ```
## Ingest data again
1. To rerun `ingest_data.py`, I have to check which docker network is used by docker compose:
   ```Bash
   docker network ls
   # check new docker network created by docker compose
   ```
2. The docker network created by docker compose follow naming standard `<current folder name>_default`. Since current folder is `pipeline`, the docker network is `pipeline_default`. So I modify command from `--network=pg-network` to `--network=pipeline_default`.
   ```Bash
   docker run -it --rm \
   --network=pipeline_default \
   taxi_ingest:v001 \
   --pg-user=root \
   --pg-pass=root \
   --pg-host=pgdatabase \
   --pg-port=5432 \
   --pg-db=ny_taxi \
   --target-table=yellow_taxi_data \
   --year=2021 \
   --month=1 \
   --chunksize=100000
   ```
## Ingest Data for SQL Refresher Chapter<sub>[11]</sub>
To move on to the next chapter, I still need download and ingest taxi_zone_lookup table.
### Build data pipeline on jupyter notebook
1. Download taxi_zone_lookup table:
   ```Python
   import pandas as pd
   from sqlalchemy import create_engine
   
   DATA_SOURCE_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/"
   ZONE_DATA = "taxi_zone_lookup.csv"
   
   zone_df = pd.read_csv(DATA_SOURCE_PREFIX+ZONE_DATA)
   ```
2. Setup Marco for SQLalchemy:
   ```Python
   POSTGRES = "postgresql"
   PG_USER = "root"
   PG_PASS = "root"
   PG_DB = "ny_taxi"
   PG_HOST = "localhost"
   PG_PORT = "5432"
   INGEST_TABLE_NAME = "zones"

   engine = create_engine(f"{POSTGRES}://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}")
   ```
3. Preview table schema and ingest table:
   ```Python
   print(pd.io.sql.get_schema(zone_df, name=INGEST_TABLE_NAME, con=engine))

   zone_df.to_sql(name=INGEST_TABLE_NAME, con=engine, if_exists='replace')
   ```
### Convert jupyter notebook to python script
```Bash
uv run jupyter nbconvert --to python ingest_zone_data.ipynb
```
### Refactor ingest_zone_data.py with click
```Python
import pandas as pd
from sqlalchemy import create_engine
import click
# from tqdm.auto import tqdm

DATA_SOURCE_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/"
ZONE_DATA = "taxi_zone_lookup.csv"

POSTGRES = "postgresql"
PG_USER = "root"
PG_PASS = "root"
PG_DB = "ny_taxi"
PG_HOST = "localhost"
PG_PORT = "5432"
INGEST_TABLE = "zones"

@click.command()
@click.option('--pg-user', default=PG_USER, help='PostgreSQL user (default:root)')
@click.option('--pg-pass', default=PG_PASS, help='PostgreSQL password (default:root)')
@click.option('--pg-host', default=PG_HOST, help='PostgreSQL host (default:localhost)')
@click.option('--pg-port', default=PG_PORT, help='PostgreSQL port (default:5432)')
@click.option('--pg-db', default=PG_DB, help='PostgreSQL db (default:ny_taxi)')
@click.option('--ingest-table', default=INGEST_TABLE, help='table name to ingest (default:zones)')
def ingest_taxi_zone_data(pg_user, pg_pass, pg_host, pg_port, pg_db, ingest_table):
    zone_df = pd.read_csv(DATA_SOURCE_PREFIX+ZONE_DATA)
    engine = create_engine(f"{POSTGRES}://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")
    zone_df.to_sql(name=ingest_table, con=engine, if_exists='replace')

if __name__ == "__main__":
    ingest_taxi_zone_data()
```
### Adjust Dockerfile for another image built
1. Adjust Dockerfile for ingest_zone_data.py
   ```Dockerfile
   # simply change ingest_data.py to ingest_zone_data.py
   COPY ingest_zone_data.py ingest_zone_data.py
   
   # define first command when run container
   ENTRYPOINT ["python", "ingest_zone_data.py"]
   ```
2. build another docker image
   ```Bash
   docker build -t taxi_zone_ingest:v001 .
   ```
### run docker taxi_zone_ingest:v001 to ingest taxi_zone_lookup table
```Bash
docker run -it \
  --network=pipeline_default \
  taxi_zone_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --ingest-table=zones
```
## SQL Refresher<sub>[12]</sub>
PostgreSQL practice:
1. `CONCAT()` and `CONCAT_WS()`:
   ```SQL
   SELECT
   	y.tpep_pickup_datetime,
   	y.tpep_dropoff_datetime,
   	y.total_amount,
   	CONCAT_WS(' | ', zpu."Borough", zpu."Zone") AS pickup_loc,
   	CONCAT(zdo."Borough", ' | ', zdo."Zone") AS dropoff_loc
   FROM
   	public.yellow_taxi_data y,
   	public.zones zpu,
   	public.zones zdo
   WHERE
   	y."PULocationID" = zpu."LocationID"
   	AND y."DOLocationID" = zdo."LocationID"
   LIMIT 10;	
   ```
   1. Lesson learned: Double quotes `" "` in PostgreSQL:
      - Issue: Why some columns in PostgreSQL need double quotes to identify?
      - Reason: PostgreSQL automatically convert all unquoted table, column, schema...etc. to <ins>lowercase<ins>, so without `" "`, PostgreSQL will convert PULocationID to pulocationid, and unable to find the column.
      - Solution:
        1. Use `" "` to avoid converting to lowercase before PostgreSQL process query.
        2. Convert column names to lowercase before push to SQL:
        ```Python
        df.columns = df.columns.str.lower()
        ```
        3. rename column names to snake_case:
        ```Python
        df.columns = ['pu_location_id', 'do_location_id']
        ```
   2. Question: What's the difference between `" "` and `' '`?<br >
      Answer: `" "` used on table, column, schema name, while `' '` used on string <ins>value</ins> in table (text, character, date)
   3. Lesson learned: `+` throw error in PostgreSQL
      - Issue: `zpu.borough + ' | ' + zpu.zone AS pickup_loc` throw error.
      - Reason: PostgreSQL reserve `+` for <ins>addition</ins> only. Other usage will throw error.
      - Solution: use `CONCAT(zpu.borough, ' | ', zpu.zone AS pickup_loc)` or `CONCAT_WS(' | ', zpu.borough, zpu.zone AS pickup_loc)`
2. Data quality check (`IS NULL`): Check NULL for `"PULocationID"` and `"DOLocationID"`
   ```SQL
   SELECT
   	tpep_pickup_datetime,
   	tpep_dropoff_datetime,
   	total_amount,
   	"PULocationID",
   	"DOLocationID"
   FROM
   	public.yellow_taxi_data
   WHERE
   	"PULocationID" IS NULL
   	OR "DOLocationID" IS NULL
   LIMIT 100;
   ```
3. Data quality check (`NOT IN`): Check `"PULocationID"` and `"DOLocationID"` are actually exist in `"LocationID"` in taxi zone lookup table
   ```SQL
   SELECT
   	tpep_pickup_datetime,
   	tpep_dropoff_datetime,
   	total_amount,
   	"PULocationID",
   	"DOLocationID"
   FROM
   	public.yellow_taxi_data
   WHERE
   	"PULocationID" NOT IN (
   		SELECT "LocationID" FROM zones
   	)
   OR	"DOLocationID" NOT IN (
   		SELECT "LocationID" FROM zones
   	);
   ```
4. `GROUP BY`, `ORDER BY`, `MAX`, `MIN`:
   ```SQL
   SELECT
   	CAST(tpep_dropoff_datetime AS DATE) drop_date,
   	COUNT(1) drop_times,
   	MAX(total_amount) max_amount,
   	MIN(passenger_count) lowest_passenger 
   FROM
   	public.yellow_taxi_data
   GROUP BY
   	CAST(tpep_dropoff_datetime AS DATE)
   ORDER BY
   	drop_times DESC
   LIMIT 100;
   ```
5. `GROUP BY` multiple fields:
   ```SQL
   SELECT
   	CAST(tpep_dropoff_datetime AS DATE) drop_date,
   	"DOLocationID",
   	COUNT(1) drop_times,
   	MAX(total_amount) max_amount,
   	MIN(passenger_count) lowest_passenger 
   FROM
   	public.yellow_taxi_data
   GROUP BY
   	1, 2
   ORDER BY
   	drop_times DESC, drop_date ASC
   LIMIT 100;
   ```
   1. Question: What does multiple GROUP BY do?
      - Answer: PostgreSQL only collapse rows when values in all GROUP BY columns are the same.
   2. Question: What does `1, 2` do in GROUP BY?
      - Answer: `1, 2` means the first and the second column in `SELECT` list, and here `1, 2` means:
        ```SQL
        GROUP BY
           CAST(tpep_dropoff_datetime AS DATE) drop_date,
           "DOLocationID",
        ```
        PostgreSQL support number 1, 2,... in `GROUP BY` as No. of columns in `SELECT` list.
6. Lesson learned: `DESCRIBE` throw error in PostgreSQL:
   - Reason: `DESCRIBE <table_name>` is NOT a valid SQL command in PostgreSQL, while valid in MySQL.<sub>[13]</sub>
   - Solution:
     1. Select table name, Columns to view table columns in pgAdmin.
     2. Query with `LIMIT 1` to view table columns:
        ```SQL
        SELECT *
        FROM yellow_taxi_data
        LIMIT 1;
        ```
## GCP Introduction<sub>[14]</sub>
### GCP 5W1H
1. What is GCP?
   - Google Cloud Platform (GCP) is a enterprise level cloud computing service, e.g. AWS, and the service is provided by Google. GCP provides services include computing, <ins>Storage & Database</ins>, <ins>Big Data</ins>, machine learning, networking, and management, and these services allow user to migrate their development application from local to cloud. GCP runs on the same infrastructure on which Google internally use to develop products, e.g. Search, Youtube, Gmail..etc.
2. Why use GCP?
   - GCP is the industry-leading services for large-scale data engineering and analytics which align data engineer skills within company to build product and applications.
3. Who to use GCP?
   - GCP is for data engineer to build scalable data lake as well as data pipeline with data processing in real time and pass to the data warehouse. In addition, software engineer can use GCP to deploy microservices, host web applications and automate CI/CD workflows.
4. When to use GCP?
   - GCP is used when large scale data processing is required. When the <ins>data size</ins> become very large and manage physical infrastructure is impractical, migrate the data model to cloud service like GCP is a practical option. In addition, <ins>GCP replace localhost machine</ins> to run data pipeline and data model to <ins>free the localhost machine</ins> for staying powered on and being occupied 24/7.
5. Where to use GCP?
   - GCP can be used for distributed deployments, which allows different countries access applications that was deployed to the closest server in their region to reduce network latency. This also provides benefit for distributed computing, e.g. load balancing, capacity pooling, and fault tolerance and recovery. 
6. How people use GCP?
   - People use GCP by Google Cloud Console for web-based UI, gcloud in CLI for apps management and deployment, and Infrastructure as Code (IaC) tool, e.g. Terraform for automatic deployment.
## Terraform Introduction<sub>[15]</sub>
### Terraform 5W1H
1. What is Terraform?<br >
   Terraform is an open source tool of Infrastructure as Code (IaC) that allows developers to create <ins>human-readable configuration files</ins> to define, provision (automatically create, configure, deploy, reuse), and manage cloud services based on codes in a file(.tf). This replaces multiple <ins>clicking, selecting, and saving</ins> on cloud consoles in various services (e.g. IAM, BigQuery, Cloud Storage, EC2, RDS) from various cloud platforms (e.g. AWS, GCP...etc.)<sub>[16][17][18]</sub>
2. Why use terraform? (terraform advantages)<sub>[17]</sub><br >
   1. Create and maintain <ins>human-readable infrastructure configuration file(.tf)</ins> to replace <ins>clicking, selecting, saving</ins> on cloud service console. This help maintain infrastructure configuration, allow us to understand the configuration, and version control of complicated cloud service infrastructure/environment setup.
   2. Terraform enable <ins>automation</ins> to <ins>safely build</ins> infrastructure with plan, setup, create, modify, upgrade, setup sequence.
   3. With applying infrastructure based on code means the code <ins>can include our policy</ins>, e.g. cost limit, security requirement, compliance, operational best practice.
   4. Reusability and modularity: Terraform enable infrastructure as a module/library (e.g. with database, container, virtual environment, cloud service setup in it) to be able to recreate the infrastructure and setup for next application.
   <img width="265" height="259" alt="image" src="https://github.com/user-attachments/assets/55ea3d69-80da-4eee-8984-b27b15b20eac" />
3. Who use terraform?<sub>[19]</sub><br >
   Terraform is built for infrastructure configuration setup and it's suit for:
   - DevOps Engineer: to automatically setup cloud infrastructure with CI/CD infrastructure pipeline.
   - Cloud Architects: to apply policy on infrastructure setup.
   - Data Engineer: to help themselves setup self-service environment, e.g. BigQuery, Google Cloud Storage buckets...etc. 
4. Where to use terraform?<br >
   Terraform mainly used on cloud service platform (GCP, AWS), cloud service (GCS buckets, BigQuery), container (WSL, Docker, VMware).<sub>[17]</sub>
5. When to use terraform?<sub>[17]</sub><br >
   Terraform is used from <ins>initial deployment</ins> (day 1), continue <ins>configuration modification/maintenance</ins> (day 2 to day n-1), to <ins>decommission/service terminate/project destory</ins> (day n).<br >
   <img width="426" height="277" alt="image" src="https://github.com/user-attachments/assets/b2d6aac6-3474-4cc2-b9f1-aaee212b9d75" />
6. How to use terraform?<sub>[20]</sub><br >
   1. Write `.tf` code: create `.tf` file and write HCL code (HashiCorp Configuration Language) and include <ins>provider</ins> to specify cloud platform.<br >
   2. `terraform init`: download provider plugin specified by provider and initialize state tracking.<br > 
   3. `terraform plan`: compare current `.tfstate` to updated `.tf` code to output update path (dry-run preview) include addition(+), modification(~), deletion(-)<br >
   4. `terraform apply`: make API calls to update and build the infrastructure that matched updated `.tf` code file.<br >
### What is DevOps?
DevOps combines development (Dev) and IT operations (Ops) and in terraform. DevOps means <ins>using Infrastructure as Code (IaC) tools</ins> to replace <ins>manually point-and-click on cloud console method</ins> to setup infrastructure in cloud platform. With terraform, DevOps define infrastructure in `.tf` files for version control and maintenance.
### What is providers in terraform?<sub>[21]</sub>
Providers is a <ins>plugin that translate terraform code into API calls for target platform</ins> (e.g. GCP, AWS, Azure). Providers <ins>help replace complicated REST API calls</ins> to human-readable blocks. 
### What is resources in terraform?<sub>[22]</sub>
Resource block in terraform represent the infrastructure object that will create, modify, or destory (e.g. IAM roles, BigQuery dataset, GCS bucket).
- resource syntax: `resource "provider resource type" "local name"`, e.g. `resource "google_storage_bucket" "my_data_bucket"`
### What is Terraform Registry?<sub>[22]</sub>
Terraform registry is a repository where terraform community and cloud vendors share pre-built <ins>providers</ins> and <ins>modules</ins>.<br >
1. The providers enable terraform to communicate with various cloud platforms.
2. The modules are <ins>reusable code blueprints</ins> which are <ins>pre-packaged set of terraform code that was configured multiple resources together following the industry best practices</ins>.
## gcloud setup (in WSL)<sub>[23]</sub>
gcloud is command line tool (CLI), which let developer to directly manage services, create service account, assign roles, and deploy resource from local to GCP. gcloud is the cleanest way to manage GCP service instead of point and click on GCP website.
1. login gmail account and authorize it to use free-tier GCP:
   - login gmail: [https://mail.google.com](https://mail.google.com)
   - authorize gmail account to use GCP: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. gcloud installation in WSL:
   1. Prerequisites: update apt-get package:
      ```Bash
      sudo apt-get update
      ```
   2. Prerequisites: make sure install `ca-certificates`, `gnupg`, `curl`
      ```Bash
      sudo apt-get install ca-certificates gnupg curl
      ```
   3. Import Google Cloud public key:
      ```Bash
      # 1. curl download gcloud public key
      # 2. use `gpg` (from `gnupg`) to:
      #    1. convert public key to binary format (because package manager only read binary format)
      #    2. save to `/usr/share/keyrings/cloud.google.gpg`
      curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg -o /usr/share/keyrings/cloud.google.gpg
      ```
   4. Add the gcloud CLI distribution URI as a package source:
      ```Bash
      # 1. deb is Repository Directive to tell system https://packages.cloud.google.com/apt cloud-sdk main is a repo contain binary packages for installation.
      # 2. [signed-by=/usr/share/keyrings/cloud.google.gpg] means this repo can be verified by gpg key in directory saved previously.
      # 3. tee is tool to read standard input and write both standard output and one more files. Here tee does:
      #   1. solve permission limitation for (>), e.g. sudo echo "..." > /etc/apt/...
      #      - Because sudo only apply to echo, (>) will fail, so sudo tee ensure writeing operation have root permission.
      #   2. tee write repo entry to google-cloud-sdk.list 
      echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
      ```
   5. Update apt-get again and install gcloud:
      ```Bash
      #   1. apt-get update rescan to include new added google cloud repository
      #   2. then install gcloud
      sudo apt-get update && sudo apt-get install google-cloud-cli
      ```
   6. Verify gcloud installed:
      ```Bash
      gcloud --version
      ```

3. Initialize and Authenticate gcloud to connect to Google account and GCP:<sub>[24]</sub>
   ```Bash
   # gcloud init will prompt to sign in Google account to authorize access and ask permission to connect to GCP
   gcloud init
   ```
4. Create Service account<sub>[25]</sub>
   ```Bash
   gcloud iam service-accounts create <Service Account Name, e.g. cj-l-service-account> \
   --display-name="CJ L Service Account"
   ```
5. Grant service account with IAM roles on the project<sub>[25][26]</sub>
   1. assign <ins>viewer</ins> role to service account
      ```Bash
      # 1. give service account viewr role
      # 2. <Project ID> can be found in gcp console -> cloud overview -> dashboard
      # 3. <Service Account Name> is the service account name created previously (cj-l-service-account)
      gcloud projects add-iam-policy-binding <Project_ID> \
      --member="serviceAccount:<Service Account Name>@<Project ID>.iam.gserviceaccount.com" \
      --role="roles/viewer"
      ```
   3. assign <ins>Storage Object Admin</ins> role to service account
      ```Bash
      gcloud projects add-iam-policy-binding <Project_ID> \
      --member="serviceAccount:<Service Account Name>@<Project ID>.iam.gserviceaccount.com" \
      --role="roles/storage.objectAdmin"
      ```
   4. assign <ins>Storage Admin</ins> role to service account
      ```Bash
      gcloud projects add-iam-policy-binding <Project_ID> \
      --member="serviceAccount:<Service Account Name>@<Project ID>.iam.gserviceaccount.com" \
      --role="roles/storage.admin"
      ```
   5. assign <ins>BigQuery Admin</ins> role to service account
      ```Bash
      gcloud projects add-iam-policy-binding <Project_ID> \
      --member="serviceAccount:<Service Account Name>@<Project ID>.iam.gserviceaccount.com" \
      --role="roles/bigquery.admin"
      ```
   6. assign <ins>Compute Admin</ins> role to service account
      ```Bash
      gcloud projects add-iam-policy-binding <Project_ID> \
      --member="serviceAccount:<Service Account Name>@<Project ID>.iam.gserviceaccount.com" \
      --role="roles/compute.admin"
      ```
6. Enable IAM API and IAM Service Account Credentials API<sub>[27]</sub>
   ```Bash
   gcloud services enable iam.googleapis.com iamcredentials.googleapis.com --project=<Project_ID>
   ```
7. Refresh Google Application Default Credentials (ADC) by login google account<sub>[28][29]</sub>
   ```Bash
   # terminal will prompt a link to login google account and authenticate gcloud CLI
   gcloud auth application-default login
   ```
## Lesson learned from gcloud setup (in WSL)
1. Issue: I wonder if exposing Project_ID, Service Account Name, or Service Account Email is a risk?
   - Answer: No, <ins>Project_ID, Service Account Name, and Service Account Email are public information.</ins>
   - Lesson learned: An attacker cannot do anything without application credential key (.json), so only expose Project_ID, Service Account Name, Service Account Email is not a risk.
2. Issue: Creating and downloading Application Credential key is not allowed:
   ```Bash
   (pipeline) > gcloud iam service-accounts keys create ~/.gcp/gcp-key.json \
    --iam-account="chun-juei-lai-service-account@project-9c55cdb0-ce48-42d5-902.iam.gserviceaccount.com"
   ERROR: (gcloud.iam.service-accounts.keys.create)
   FAILED_PRECONDITION: Key creation is not allowed on this service account.
   ...
   type: constraints/iam.disableServiceAccountKeyCreation
   ```
   - Reason: GCP enabled Disable service account key creation policy for safety and security
   - Lesson learned: GCP enabled Disable service account key creation policy and recommend developers using Application Default Credentials.
3. Issue: Service Account Credential Key vs. Application Default Credentials (ADC)
   - Reason: Service Account Credential Key will save `.json` key in local, and GCP has warned it is a security risk if not managed correctly.<sub>[30]</sub>
   - Lesson learned: Application Default Credentials is safer in general. To setup ADC for project, simply input `gcloud auth application-default login` and connect with your google account.<sub>[31][32]</sub> GCP will automatically generate ADC key in `~/.config/gcloud/application_default_credentials.json` and authenticate it later.<sub>[33]</sub>
4. Issue: How to display what roles did I assign to my accounts:<sub>[34]</sub>
   - Answer: display with gcloud:
     ```Bash
     gcloud projects get-iam-policy <Project ID> \
     --flatten="bindings[].members" \
     --format="table(bindings.members:label=ACCOUNT, bindings.role:label=ROLE)"
     ```
5. Question: What is Application Default Credential (ADC) and what does it do?
   - Lesson Learned: ADC is <ins>automated lookup strategy</ins> by Google Cloud Library, Terraform, gcloud <ins>to authenticate requests</ins> from developers. when using gcloud or terraform google providers, the system will automatically authenticate requests, and it decrease workload from developer to generate path to verify manually by gcloud.
## Terraform setup (in WSL)<sub>[35][36]</sub>
1. Terraform installation in WSL:
   1. Prerequisites: update the latest package index and install available updates:
      ```Bash
      sudo apt update && sudo apt upgrade
      ```
   2. Prerequisites: update apt-get package and install `gnupg`, `software-properties-common`, `curl`
      ```Bash
      sudo apt-get update && sudo apt install -y gnupg software-properties-common curl
      ```
   3. Import HashiCorp's public key:
      ```Bash
      # 1. curl download HashiCorp's public key
      # 2. use `gpg` (from `gnupg`) to:
      #    1. convert public key to binary format (because package manager only read binary format)
      #    2. save to `/usr/share/keyrings/hashicorp-archive-keyring.gpg`
      curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
      ```
   4. Add the HashiCorp repository URI as a package source:
      ```Bash
      # 1. deb is Repository Directive to tell system https://apt.releases.hashicorp.com $(lsb_release -cs) main is a repo contain binary packages for installation.
      # 2. [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] means this repo can be verified by gpg key in directory saved previously.
      # 3. tee is tool to read standard input and write both standard output and one more files. Here tee does:
      #   1. solve permission limitation for (>), e.g. sudo echo "..." > /etc/apt/...
      #      - Because sudo only apply to echo, (>) will fail, so sudo tee ensure writeing operation have root permission.
      #   2. tee write repo entry to /hashicorp.list 
      echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
      ```
   5. Update apt-get again and install terraform:
      ```Bash
      #   1. apt-get update rescan to include new added HashiCorp repository
      #   2. then install terraform
      sudo apt update && sudo apt install terraform -y
      ```
   6. Verify terraform installed:
      ```Bash
      terraform --version
      ```
2. Add Terraform.gitignore:
   As always, adding tool gitignore (here: Terraform gitignore) is a __most__ configuration before generating `.tf` file as well as coding.<sub>[37]</sub>
3. Search and Install Extension of HashiCorp Terraform in vs code.<sub>[38]</sub>
   - HashiCorp Terraform is an extension in vs code, which is an useful tool for function prompting and auto-completion when coding in Terraform (.tf).<sub>[26]</sub><br >
   <img width="642" height="156" alt="image" src="https://github.com/user-attachments/assets/b4445a70-7ee7-4e87-aa46-035a7a018d71" />
## `terraform init`
The first step to initialize project infrastructure configuration with terraform and cloud service is `terraform init`. The following are steps for `terraform init`:<sub>[39]</sub>
1. Create `main.tf` in new directory `terraform_workshop`:
   ```Bash
   mkdir terraform_workshop
   cd terraform_workshop
   touch main.tf 
   ```
2. Add terraform block and provider block:
   - `terraform` block describes the terraform setting: __what__ provider (cloud platform) plugin is required to configure the project infrastructure. Here, terraform set the project to accept __Google__ providers for infrastructure configuration.<sub>[40][41]</sub>
   - `provider` block describes what project for connection and which region to deploy the project. Here, `provider` set to connect to __my-project-id__ at __us-central__ region.<sub>[42][43]</sub>
   ```terraform
   terraform {
     required_providers {
       google = {
         source  = "hashicorp/google"
         version = "7.45.0"
       }
     }
   }
   
   provider "google" {
     project     = "my-project-id"
     region      = "us-central1"
   }
   ```
   - Note: A quick way to format terraform, e.g. indention, alignment, is `terraform fmt`. `terraform fmt` automatically align terraform files in current directory.<sub>[44]</sub>
     ```Bash
     terraform fmt
     ```
3. Initialize project infrastructure with configuration in terraform files (`.tf`):
   - With `terraform init`, terraform prepares working directory with backend installation (generate .terraform.lock.hcl, terraform.tfstate, terraform.tfstate.backu) and provider plugin downloaded.<sub>[45]</sub>
   ```Bash
   terraform init
   ```
## `terraform plan`
Next, I am going to add resource blocks in `main.tf`, so `terraform plan` will specify that a GCP storage bucket and a BigQuery dataset will be created in my project on GCP.<sub>[46][47]</sub>
```terraform
# syntax:
# resource "provider resource type" "local name"
resource "google_storage_bucket" "demo-bucket" {
  name                        = "<Project ID>.terra.bucket"
  location                    = "us-central1"
  uniform_bucket_level_access = true
  force_destroy               = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "demo_dataset"
  location   = "us-central1"
}
```
```Bash
terraform plan
```
- Note:
  1. (Recommended) `terraform plan` is a safe way to check what is going to be done based on `main.tf` before `terraform apply`.
  2. Google Cloud Storage (GCS) vs. BigQuery: GCS is a Data Lake where raw data store, while BigQuery is a Data Warehouse where data were collected, organized, and reported.<sub>[48][49]</sub>
  3. What is a bucket in Google Cloud Storage (GCS)? a bucket is a basic container in GCS where data store. The uploaded data called <ins>objects</ins>.<sub>[50]</sub>
  4. Remember to assign the closest location and zone that GCP provide to reduce latency.<sub>[51]</sub>

## Reference<br >
1. [Introduction to Docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/01-introduction.md)
2. [Virtual Environments and Data Pipelines](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/02-virtual-environment.md)
3. [Dockerizing the Pipeline](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/03-dockerizing-pipeline.md)
4. [Running PostgreSQL with Docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/04-postgres-docker.md)
5. [Upgrading between major versions?](https://github.com/docker-library/postgres/issues/37#issuecomment-4435452264)
6. [NY Taxi Dataset and Data Ingestion](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/05-data-ingestion.md)
7. [Creating the Data Ingestion Script](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/06-ingestion-script.md)
8. [pgAdmin - Database Management Tool](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/07-pgadmin.md)
9. [Dockerizing the Ingestion Script](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/08-dockerizing-ingestion.md)
10. [Docker Compose](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/09-docker-compose.md)
11. [Taxi Zone Lookup Table](https://github.com/DataTalksClub/nyc-tlc-data/releases/)
12. [SQL Refresher](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/10-sql-refresher.md)
13. [115. DESCRIBE](https://github.com/raylai-proj/SQL_review_note#115-describe)
14. [GCP](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform#gcp)
15. [Terraform Overview](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/1_terraform_overview.md)
16. [What is Terraform?](https://developer.hashicorp.com/terraform/intro)
17. [Introduction to Terraform](https://www.youtube.com/watch?v=ZFLWA1kQ3ls)
18. [DE Zoomcamp 1.1.1 - Introduction to Google Cloud Platform](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=3)
19. [Infrastructure as code: What is it? Why is it important?](https://www.hashicorp.com/en/resources/what-is-infrastructure-as-code)
20. [terraform execution steps](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/1_terraform_overview.md#execution-steps)
21. [terraform providers](https://registry.terraform.io/browse/providers)
22. [terraform declaration](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/1_terraform_overview.md#declarations)
23. [Install the Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk)
24. [Initialize and authorize the gcloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk#initializing-the-cli)
25. [Create service accounts](https://docs.cloud.google.com/iam/docs/service-accounts-create#iam-service-accounts-create-gcloud)
26. [DE Zoomcamp 1.3.2 - Terraform Basics](https://www.youtube.com/watch?v=Y2ux7gq3Z0o&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=9)
27. [Enabling an API in your Google Cloud project](https://docs.cloud.google.com/endpoints/docs/openapi/enable-api)
28. [gcloud auth application-default login](https://docs.cloud.google.com/sdk/gcloud/reference/auth/application-default/login)
29. [GCP Overview - Setup for Access](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/2_gcp_overview.md#setup-for-access)
30. [Service account keys](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment#local-key)
31. [Set up Application Default Credentials](https://docs.cloud.google.com/docs/authentication/provide-credentials-adc)
32. [Set up ADC for a local development environment](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)
33. [How Application Default Credentials works](https://docs.cloud.google.com/docs/authentication/application-default-credentials)
34. [View current access](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access)
35. [Installing Terraform on Linux (Ubuntu) and Windows (WSL2 with Ubuntu)](https://codingarchitect.dev/blog/installing-terraform-on-linux-ubuntu-and-windows-wsl2-with-ubuntu/)
36. [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
37. [Terraform.gitignore](https://github.com/github/gitignore/blob/main/Terraform.gitignore)
38. [vs code extension - HashiCorp Terraform](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
39. [Write configuration](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#write-configuration)
40. [Terraform Registry - Google Providers](https://registry.terraform.io/providers/hashicorp/google/latest)
41. [Terraform Block](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#terraform-block)
42. [Terraform provider for Google Cloud](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
43. [provider block reference](https://developer.hashicorp.com/terraform/language/block/provider)
44. [terraform fmt command](https://developer.hashicorp.com/terraform/cli/commands/fmt)
45. [terraform init command](https://developer.hashicorp.com/terraform/cli/commands/init)
46. [Google Provider - Example Usage - Life cycle settings for storage bucket objects](https://registry.terraform.io/providers/hashicorp/google/4.35.0/docs/resources/storage_bucket#example-usage---life-cycle-settings-for-storage-bucket-objects)
47. [Google Provider - Example Usage](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/bigquery_dataset#example-usage)
48. [Data warehouse](https://en.wikipedia.org/wiki/Data_warehouse)
49. [BigQuery](https://cloud.google.com/bigquery)
50. [About Cloud Storage buckets](https://docs.cloud.google.com/storage/docs/buckets)
51. [Google Cloud Region Picker](https://cloud.withgoogle.com/region-picker/)






