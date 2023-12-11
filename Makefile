build:
	docker-compose up --build -d

up:
	docker-compose up -d

down:
	docker-compose down -v

logs_api:
	sudo docker logs -f backend_app_1

logs_db:
	sudo docker logs -f backend_db_1
