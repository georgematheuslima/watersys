
build:
	docker build -t watersys:latest .

stop:
	sudo docker stop $(docker ps -q)

select-none-images:
	docker images -f "dangling=true" -q

remove-none-images:
	docker rmi $(docker images -f "dangling=true" -q)

up:
	docker-compose up

up-rebuild:
	docker-compose up --build
down:
	docker-compose down

logs:
	docker logs watersys

restart:
	make stop && make remove && make build && make up

rebuild:
	make down && docker rmi watersys-app && make up

run:
	docker run --name watersys -d -p 8000:8000 watersys

restart:
	docker-compose down && docker-compose up

