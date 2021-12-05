# Docker
## Docker example
The docker structure is setup, such that there can be multiple entrypoints in the future.
Basically, the *main.py* script will execute other scripts defined when running the docker image.

As an example:

`docker build -t python-test .`

`docker run python-test "src/example.py"`

This will create the docker image as *python-test* and then run the script *example.py*.

Using a script to run all commands can further simplify things.

### Dependencies
Since we are using python, most if not all libraries should be available via pip.
Every time *docker build* is called, it will install all libraries specified in the *requirements.txt*.
In case additional libraries are necessary, the *requirements.txt* can simply be extended.

### Remove docker containers
In case there are still unwanted containers on the host they can be handled one of two ways:

#### Remove single container
Use `docker ps` to find the container ID.

Then use `docker stop <ID>` to stop the container.

Lastly, use `docker rm <ID>` to remove the container.

#### Remove all containers 
In case unnecessary containers were created the following commands can be used.
**Use with caution! This will remove all containers.**

`docker stop $(docker ps -a -q)`

`docker rm $(docker ps -a -q)`

### Remove docker containers
In case there are still unwanted images on the host they can be handled one of two ways:

#### Remove single image

Then use  `docker image ls` to find the image ID.

Lastly, use `docker rmi <ID>` to remove the image.

#### Remove all images
In case unnecessary images were created the following commands can be used.
**Use with caution! This will remove all images.**

`docker rmi $(docker images -f dangling=true -q)`

