# README #

The Scoring Server provides the software and interfaces to register and report score-related information for the DARPA Subterranean Challenge.

### Getting Started ###
Install Docker:

    $ sudo apt install docker.io

Install docker-compose:

    $ sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    $ sudo chmod +x /usr/local/bin/docker-compose

Create a docker user group to bypass running docker with sudo

    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER

Restart the computer

Make sure the docker daemon is running

    $ sudo service docker start

Confirm docker and docker-compose both work

    $ docker run hello-world
    $ docker-compose version

To start the server, enter the directory that contains the docker-compose.yml file and run the following:  
    $ docker-compose up --build


Add this header:

    Authorization: Bearer tokentokentoken1

to any request sent to the endpoints.


To run the API tests (with the server running as above):

    $ docker-compose exec django pytest -v
