## Docker Set Up 

Sources:
* https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu
* https://techexpert.tips/postgresql/postgresql-docker-installation/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

### Basics (after installing Docker):
Get Image:

```docker pull postgres```

Create Volume:

```mkdir -p docker/postgres/volumes```

Create Postgres Instance:

```docker run --name G2H -e POSTGRES_USER=ubuntu -e POSTGRES_PASSWORD=ubuntu -p 5432:5432 -v /<path-to-docker>/docker/postgres/volumes:/var/lib/postgresql/data -d postgres```

To see running containers:

```docker ps```

To see all containers:

```docker ps -a ```

To Connect to Container:

```docker exec -ti G2H /bin/bash```

Connect to Postgres:

```psql -U ubuntu -W```

Create Database:

```CREATE DATABASE main_db;```

Connect to Database:

```\c main_db;```

Create Table:

```CREATE TABLE haros;```



### Connecting to Container
Connect to container using its name:
```
docker exec -ti LYS_psql /bin/bash
```
-ti — in foreground

Inside of Container to connect to Postgres using Username:
```
psql -U ubuntu -W
```
-W — to enter password
-U <username>

Inside of Postgres:
\q   — to quit
\l   - List of databases
\dn  - List of Schemas under current db
\c <database name>; — connect to specific database and enter a password for the user

### Postgres SQL Connection:
```
POSTGRES_DATABASE_URI = 'postgresql://ubuntu:ubuntu@0.0.0.0:5432/main_db'
```
Example: `postgresql://user:secret@localhost:5432/DB_NAME`