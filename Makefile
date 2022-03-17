#NAME ?= vjannu0711

all: build run push

images:
	docker images | grep vjannu0711

ps:
	docker ps -a | grep vjannu0711

build:
	docker build -t vjannu0711/iss-sighting-loc:midterm1 .

run:
	docker run --name "iss_sighting_loc" -d -p 5012:5000 vjannu0711/iss-sighting-loc:midterm1

push:
	docker push vjannu0711/iss-sighting-loc:midterm1
