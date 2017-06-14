.PHONY: stop_all rm_all

help:
	@echo "make up | up2 | ab | watch | curl | down | fulldown | scale | ps | logs | stop_all | rm_all | ips"

stop_all:
	@docker stop `docker ps -q`

rm_all:
	@docker rm `docker ps -aq`

up:
	@docker-compose up -d

up2: 
	@docker-compose up -d --build

watch:
	@watch curl http:/127.0.0.1:8000/

curl:
	@curl -v http://127.0.0.1:8000/

ab:
	@ab -c 10 -n 2000 http://127.0.0.1:8000/

down:
	@docker-compose down

fulldown:
	@docker-compose down --rmi all -v --remove-orphans

scale:
	@docker-compose scale redis-slave=3 

ps:
	@docker-compose ps

logs:
	@docker-compose logs

ips:
	@docker inspect --format '{{ .Name }} - {{ .NetworkSettings.Networks.dpf_default.IPAddress }}' `docker-compose ps -q`
