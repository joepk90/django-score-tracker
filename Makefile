PROJECT_DIR=./score_tracker

DOCKER_REPOSITORY=django-score-tracker
LATEST_TAG=latest

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

ci-docker-auth:
	@echo "Logging in to $(DOCKER_REGISTRY) as $(DOCKER_ID)"
	@docker login -u $(DOCKER_ID) -p $(DOCKER_PASSWORD)

ci-docker-test:
	docker build -t $(DOCKER_REPOSITORY):test -f ./Dockerfile.test ./

ci-docker-build:
	docker build -t $(DOCKER_REPOSITORY):$(COMMIT_SHA) ./
	docker build -t $(DOCKER_REPOSITORY):$(LATEST_TAG) ./

ci-docker-push: ci-docker-auth
	docker push $(DOCKER_REGISTRY)/$(DOCKER_REPOSITORY):$(COMMIT_SHA)
	docker push $(DOCKER_REGISTRY)/$(DOCKER_REPOSITORY):$(LATEST_TAG)


