## Docker Set Up 

Sources:
* https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu
* https://techexpert.tips/postgresql/postgresql-docker-installation/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

Install Docker:
```
sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io
sudo snap install docker
docker --version

sudo apt-get install docker.io


#To set up a user and user docker without sudo 
sudo usermod -aG docker ${USER}
```
Then EXIT and enter the system 


To install postgres image:
```
docker pull postgres
```

List all Docker Images:
```
docker images
```

Create folder for volumes of postgres:
```
#!!Create volumes of postgres in empty table 
mkdir -p docker/postgres/volumes
```

Create and Run container:
```
docker run --name LYS_psql -e POSTGRES_USER=ubuntu -e POSTGRES_PASSWORD=ubuntu -p 5432:5432 -v /home/ubuntu/lightyear/docker/postgres/volumes:/var/lib/postgresql/data -d postgres
```
* --name <name_of_container>
* -d <image>  — in detached mode
* -v /<localpath>:/var/lib/postgresql/data


See Active and Inactive Containers:
```
docker ps
docker ps -a 
```

### Connecting to Container
Connect to container using its name:
```
docker exec -ti LYS_psql /bin/bash
```
-ti — in foreground


### Basics (after installing Docker):
Get Image:

```docker pull postgres```

To see running containers:

```docker ps```

To see all containers:

```docker ps -a ```

To Connect to Container:

```docker exec -ti LYS_psql /bin/bash```


