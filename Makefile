# DOCKER_REGISTRY = # githib secret
PROJECT_DIR=./score_tracker
LATEST_TAG=latest
DOCKER_CONTAINER=django-score-tracker
DOCKER_REPOSITORY=$(DOCKER_REGISTRY)/$(DOCKER_CONTAINER)
GOOGLE_REPOSITORY=gcr.io/automated-deployment-test-01/$(DOCKER_CONTAINER)

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

docker-build:
	# docker build -t $(DOCKER_CONTAINER) ./  --progress=plain --no-cache
	docker build -t $(DOCKER_CONTAINER) ./

# .env-docker file required in root directory
# PYTHONUNBUFFERED = enable print logging
# help docker respond to ctr + c when not detatched:  -it --init = 
docker-run:
	docker run --env-file ./.env.docker \
	-it --init \
	-e PYTHONUNBUFFERED=1 \
	-d -p 8080:8080 $(DOCKER_CONTAINER)
	@echo "View instance: http://0.0.0.0:8080"

# example docker run command using environment variables
docker-run-env-vars:
	docker run \
	--env SECRET_KEY='1234' \
	--env DEBUG=TRUE \
	--env ENVIRONMENT=PROD \
	--env ALLOWED_HOSTS=* \
	--env DATABASE_NAME=dbname \
	--env DATABASE_USER=dbuser \
	--env DATABASE_PASS=dbpassword \
	--env DATABASE_HOST=127.0.0.1 \
	--env DATABASE_PORT=5432 \
	-d -p 8080:8080 $(DOCKER_CONTAINER)
	@echo "View instance: http://0.0.0.0:8080"

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

ci-gcloud-configure-docker:
	gcloud auth configure-docker -q
	@echo "configured gcloud for docker"

# push to google container registry
ci-gcr-push: ci-gcloud-configure-docker ci-gcr-build
	docker push ${GOOGLE_REPOSITORY}:$(COMMIT_SHA)
	docker push ${GOOGLE_REPOSITORY}:$(LATEST_TAG)
	@echo "Deployed tagged image: $(GOOGLE_REPOSITORY):$(COMMIT_SHA)"
	@echo "Deployed tagged image: $(GOOGLE_REPOSITORY):$(LATEST_TAG)"

docker-compose-build:
	docker-compose build --no-cache django