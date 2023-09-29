
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SRC_DIR:=${ROOT_DIR}/src

.PHONY: copyx

build: gen add-license
	cd ${ROOT_DIR}
	rm -rf ${ROOT_DIR}/dist/*
	poetry build

# https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04
publish: build
	poetry publish

test:
	poetry run pytest ${ROOT_DIR}/tests/ --cov=ivcap_sdk_client --cov-report=xml


SRC_DIR=${ROOT_DIR}/src/ivcap_client
OPENAPI_URL=https://raw.githubusercontent.com/reinventingscience/ivcap-core-api/main/openapi3.json
gen:
	@if ! type "openapi-python-client" > /dev/null; then \
		echo ">>>\n>>> You need to first install 'openapi-python-client'\n>>>"; \
		exit -1; \
	fi
	rm -rf ${ROOT_DIR}/build && mkdir -p ${ROOT_DIR}/build
	cd ${ROOT_DIR}/build \
	  && curl ${OPENAPI_URL} -o openapi3.json \
		&& openapi-python-client generate --path openapi3.json --config ${ROOT_DIR}/config.yml \
		&& python ${ROOT_DIR}/fix_auto_generated.py \
		&& cd sdk_client/ivcap_client && mkdir client && mv *.py client \
		&& cd ${ROOT_DIR}
	rm -fr ${SRC_DIR}/api ${SRC_DIR}/models ${SRC_DIR}/client \
		&& mkdir -p ${SRC_DIR}/api ${SRC_DIR}/models ${SRC_DIR}/client \
		&& mv ${ROOT_DIR}/build/sdk_client/ivcap_client/* ${SRC_DIR} \
		&& mv ${SRC_DIR}/client/errors.py ${SRC_DIR}/client/types.py ${SRC_DIR} \
		&& sed -i '' '1s/^/#\n#### DO NOT EDIT ####\n#\n/' ${SRC_DIR}/types.py ${SRC_DIR}/errors.py
	rm -r ${ROOT_DIR}/build

add-license:
	licenseheaders -t .license.tmpl -y 2023 -f src/ivcap_client/*.py
	licenseheaders -t .license.tmpl -y 2023 -d src/ivcap_client/client

docs:
	rm -rf ${ROOT_DIR}/docs/_build
	cd ${ROOT_DIR}/docs && make html

clean:
	rm -rf *.egg-info
	rm -rf dist
	find ${ROOT_DIR} -name __pycache__ | xargs rm -r 

.PHONY: docs
