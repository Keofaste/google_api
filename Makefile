run: stop
	docker-compose up -d
stop:
	docker-compose down
build:
	docker-compose build
