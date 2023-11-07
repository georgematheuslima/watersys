
build:
	docker build -t watersys:latest .

stop:
	docker stop $(docker ps -q)
remove:
	docker rm $(docker ps -a -q)

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker logs watersys -f

restart:
	make stop && make remove && make build && make up

rebuild:
	make down && docker rmi watersys-app && make up

run:
	docker run -d -p 8000:8000 watersys 