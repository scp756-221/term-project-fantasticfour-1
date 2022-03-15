# Makefile for standalone User service (S1)

VER=v0.8

SERVER=`docker inspect s1 --format '{{.NetworkSettings.IPAddress}}'`
PORT=30000

build-mcli_s1:
	docker image build -f Dockerfile -t mcli_s1:$(VER) .

run-mcli_s1:
	docker container run -it --rm --name mcli_s1 mcli_s1:$(VER) python3 mcli_s1.py $(SERVER) $(PORT)
