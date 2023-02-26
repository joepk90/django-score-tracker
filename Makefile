PROJECT_DIR=./score_tracker
LATEST_TAG=latest
DOCKER_CONTAINER=django-score-tracker
DOCKER_REPOSITORY=$(DOCKER_REGISTRY)/$(DOCKER_CONTAINER)
GOOGLE_REPOSITORY=gcr.io/$(DOCKER_CONTAINER)/$(DOCKER_CONTAINER)

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
	@echo "Created new tagged image: $(DOCKER_REPOSITORY):$(COMMIT_SHA)"
	@echo "Created new tagged image: $(DOCKER_REPOSITORY):$(LATEST_TAG)"

ci-gcr-build:
	docker build -t $(GOOGLE_REPOSITORY):$(COMMIT_SHA) ./
	docker build -t $(GOOGLE_REPOSITORY):$(LATEST_TAG) ./
	@echo "Created new tagged image: $(GOOGLE_REPOSITORY):$(COMMIT_SHA)"
	@echo "Created new tagged image: $(GOOGLE_REPOSITORY):$(LATEST_TAG)"

ci-docker-push: ci-docker-auth
	docker push $(DOCKER_REPOSITORY):$(COMMIT_SHA)
	docker push $(DOCKER_REPOSITORY):$(LATEST_TAG)
	@echo "Deployed tagged image: $(DOCKER_REPOSITORY):$(COMMIT_SHA)"
	@echo "Deployed tagged image: $(DOCKER_REPOSITORY):$(LATEST_TAG)"


# google container registry
ci-gcr-push: ci-gcr-build
	docker push gcr.io/django-score-tracker/django-score-tracker:latest
	@echo "Deployed tagged image: $(GOOGLE_REPOSITORY):$(LATEST_TAG)"