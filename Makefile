# ipam-o-nator make file


hubusername=chris17453
youremail=chris17453@gmail.com
image_name=ipam-o-nator
image_version=latest
# openshift token
os_toklen=<xyz>
os_server=https://openshift_server.com
app_hostname=ipam-o-nator.website.com

.DEFAULT: help
.PHONY: all test clean profile

help:
	@echo "ipam-o-nator"
	@echo ""
	@echo "build           | build the container used to host this webui"
	@echo "build-proxy     | build the container used to host this webui from behind a proxy"
	@echo "run             | run the container"
	@echo "ldap {endpoint} | configure LDAP authentication for the webui"
	@echo "stop            | stop the container"
	@echo "delete          | stop and delete container"
	@echo "status          | show the status of the container"
	@echo ""
	

build-proxy:
	@docker build -f ./deployment/Dockerfile --build-arg http_proxy=http://172.17.0.1:3128 --build-arg https_proxy=http://172.17.0.1:3128 -t $(image_name):$(image_version) .

build:
	@docker build -f ./deployment/Dockerfile  -t $(image_name):$(image_version) .

run:
	@docker run -p 8080:8080 -u 112233 $(image_name):$(image_version)

export:
	@docker save --output $(image_name).$(image_version).tar $(image_name):$(image_version)
#ldap:
#stop:
#delete:
#status:
login:
	@docker login --username=$(hubusername) --email=$(youremail)

push:
	@docker tag $(docker images | grep ^$(image_name) |awk '{print $3}') $(hubusername)/$(image_name):$(image_version)
	@docker push $(hubusername)/$(image_name):$(image_version)

deploy-new_openshift:
	@oc login $(os_server)--token=$(os_token)
	@oc new-app $(hubusername)/$(image_name)
	@oc create route edge --service=$(image_name) --hostname=$(app_hostname) --port=8080-tcp

deploy-update-openshift:
	@oc import-image $(image_name):$(image_version) --from=$(hubusername)/$(image_name) --confirm

debug:
#	@. src/load_env.sh
	@python ./src/wsgi.py

test:
	@python -m src.test 

set_vars:
	@src/setup_env.sh

	