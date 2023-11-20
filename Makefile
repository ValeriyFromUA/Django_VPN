include .env
export $(shell sed 's/=.*//' .env)

define USAGE
Commands:
    docker_run		Run web application with Docker
    docker_tests		Run tests with Docker


endef


docker_run:
	sudo docker-compose up app

docker_tests:
	sudo docker-compose up test
