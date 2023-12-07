# Variables
HOST_PORT=8080
CNTR_PORT=8000
TAG=v1.0
NAME=5500-team-krusty-krab
REPO_HOST=449503323972.dkr.ecr.us-east-1.amazonaws.com/kk-online-payment
TAGGED_IMAGE=$(REPO_HOST):$(TAG)
LOCAL_IMAGE_NAME=todo_app_test:$(TAG)

.PHONY: hello
hello:
	@echo "Hello, World"
	@echo "This line will print if a file named 'hello' does not exist unless 'hello' is phony"

image: Dockerfile
	docker build --pull -t $(LOCAL_IMAGE_NAME) .
	@echo "DONE"

run-app-local:
	docker run --detach --publish $(HOST_PORT):$(CNTR_PORT) --name $(NAME) $(LOCAL_IMAGE_NAME)

run-app-prod:
	docker run --detach --publish $(HOST_PORT):$(CNTR_PORT) --name $(NAME) $(TAGGED_IMAGE)

exec-app:
	docker exec -it $(NAME) bash

stop-app:
	docker stop $(NAME)

rm-app:
	docker rm $(NAME)

ecr-login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(REPO_HOST)

ecr-logout:
	docker logout $(REPO_HOST)

prod-image: ecr-login image
	docker tag $(LOCAL_IMAGE_NAME) $(TAGGED_IMAGE)
	docker push $(TAGGED_IMAGE)
	$(MAKE) ecr-logout

all:
	@echo ${USER}
