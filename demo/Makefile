ROOT = $(shell pwd)
STAGE = $(ROOT)/stage
DEMO_STAGE_DIR = $(STAGE)/demo
DEMO_NGINX_STAGE_DIR = $(STAGE)/demo-nginx
VERSION ?= latest
REPO ?= 742127912612.dkr.ecr.us-west-2.amazonaws.com
DOCKEROPTS ?=
DOMAIN ?= testsliderule.org
DOMAIN_ROOT = $(firstword $(subst ., ,$(DOMAIN)))

all: demo-docker

demo-docker: # make the python client demo docker image; needs VERSION
	-rm -Rf $(DEMO_STAGE_DIR)
	mkdir -p $(DEMO_STAGE_DIR)
	cp ../environment.yml $(DEMO_STAGE_DIR)
	cp voila_demo.ipynb $(DEMO_STAGE_DIR)
	cp docker/demo/* $(DEMO_STAGE_DIR)
	# used to install local copy of client (only if necessary during development, see dockerfile for additional steps)
	cp -R ../../sliderule $(DEMO_STAGE_DIR)
	chmod +x $(DEMO_STAGE_DIR)/docker-entrypoint.sh
	cd $(DEMO_STAGE_DIR) && docker build $(DOCKEROPTS) -t $(REPO)/demo-client:latest .
	docker tag $(REPO)/demo-client:latest $(REPO)/demo-client:$(VERSION)
	mkdir -p $(DEMO_NGINX_STAGE_DIR)
	cp docker/demo-nginx/* $(DEMO_NGINX_STAGE_DIR)
	cd $(DEMO_NGINX_STAGE_DIR) && docker build $(DOCKEROPTS) -t $(REPO)/demo-nginx:latest .
	docker tag $(REPO)/demo-nginx:latest $(REPO)/demo-nginx:$(VERSION)

demo-run: ## run the python client demo docker container locally; needs VERSION
	docker run -it --rm --name=python-app -p 8866:8866 --entrypoint /usr/local/etc/docker-entrypoint.sh $(REPO)/demo-client:$(VERSION)

demo-push:
	docker push $(REPO)/demo-client:$(VERSION)
	docker push $(REPO)/demo-nginx:$(VERSION)

demo-deploy: ## deploy demo using terraform; needs VERSION, DOMAIN
	cd terraform && terraform init
	cd terraform && terraform workspace select $(DOMAIN)-demo || terraform workspace new $(DOMAIN)-demo
	cd terraform && terraform apply -var docker_image_url_demo-client=$(REPO)/demo-client:$(VERSION) -var docker_image_url_demo-nginx=$(REPO)/demo-nginx:$(VERSION) -var domain=$(DOMAIN) -var domain_root=$(DOMAIN_ROOT)

demo-destroy: ## destroy demo using terraform; needs DOMAIN
	cd terraform && terraform init
	cd terraform && terraform workspace select $(DOMAIN)-demo || terraform workspace new $(DOMAIN)-demo
	cd terraform && terraform destroy -var domain=$(DOMAIN) -var domain_root=$(DOMAIN_ROOT)

distclean: ## fully remove all non-version controlled files and directories
	- rm -Rf $(STAGE)
