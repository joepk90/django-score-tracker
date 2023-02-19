PROJECT_DIR=./score_tracker

DOCKER_REPOSITORY=django-score-tracker

# pipenv, version 2021.5.29
generate-requirements:
	pipenv lock -r > requirements.txt
	pipenv lock --dev --requirements > requirements-dev.txt 

runserver:
	python ${PROJECT_DIR}/manage.py runserver

migrations:
	python ${PROJECT_DIR}/manage.py makemigrations

migrate:
	python ${PROJECT_DIR}/manage.py migrate

tests:
	pytest ${PROJECT_DIR}

watch-tests:
	ptw  ${PROJECT_DIR}

ci-docker-test:
	docker build -f ./Dockerfile.test ./

ci-docker-build:
	docker build -t $(DOCKER_REPOSITORY):$(COMMIT_SHA) ./