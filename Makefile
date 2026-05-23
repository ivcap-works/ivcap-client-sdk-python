
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SRC_DIR:=${ROOT_DIR}/src

.PHONY: help copyx lint typecheck check

help:
	@echo "Available targets:"
	@echo "  gen           - Generate client code from OpenAPI specification"
	@echo "  add-license   - Add license headers to source files"
	@echo "  build         - Build the package using Poetry"
	@echo "  publish       - Publish the package to PyPI using Poetry"
	@echo "  test          - Run tests with coverage reporting"
	@echo "  lint          - Run ruff checks"
	@echo "  typecheck     - Run pyright type checking"
	@echo "  check         - Lint + typecheck + tests"
	@echo "  docs          - Build MkDocs documentation"
	@echo "  docs-mkdocs   - Build MkDocs documentation (alias)"
	@echo "  docs-serve    - Serve MkDocs documentation locally (http://localhost:8000)"
	@echo "  docs-clean    - Clean MkDocs build artifacts"
	@echo "  clean         - Remove build artifacts and caches"

build: gen add-license
	cd ${ROOT_DIR}
	rm -rf ${ROOT_DIR}/dist/*
	poetry build

# https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04
publish: build
	poetry publish

test:
	poetry run pytest ${ROOT_DIR}/tests/ --cov=ivcap_client --cov-report=xml

lint:
	poetry run poe lint

typecheck:
	poetry run poe typecheck

check: lint typecheck test

SRC_DIR=${ROOT_DIR}/ivcap_client
OPENAPI_URL=https://raw.githubusercontent.com/ivcap-works/ivcap-core-api/develop/openapi3.json
gen:
	@if ! poetry run bash -c "command -v openapi-python-client > /dev/null 2>&1"; then \
		echo ">>>\n>>> You need to first install 'openapi-python-client'\n>>>"; \
		exit -1; \
	fi
	rm -rf ${ROOT_DIR}/build && mkdir -p ${ROOT_DIR}/build
	cd ${ROOT_DIR}/build \
	  && curl ${OPENAPI_URL} > openapi3.json \
		&& poetry run openapi-python-client generate --path openapi3.json --config ${ROOT_DIR}/config.yml \
		&& poetry run python ${ROOT_DIR}/fix_auto_generated.py \
		&& cd sdk_client/ivcap_client && mkdir client && mv *.py client \
		&& cd ${ROOT_DIR}
	rm -fr ${SRC_DIR}/api ${SRC_DIR}/models ${SRC_DIR}/client \
		&& mkdir -p ${SRC_DIR}/api ${SRC_DIR}/models ${SRC_DIR}/client \
		&& mv ${ROOT_DIR}/build/sdk_client/ivcap_client/* ${SRC_DIR} \
		&& mv ${SRC_DIR}/client/errors.py ${SRC_DIR}/client/types.py ${SRC_DIR} \
		&& sed -i '' '1s/^/#\n#### DO NOT EDIT ####\n#\n/' ${SRC_DIR}/types.py ${SRC_DIR}/errors.py

#	rm -r ${ROOT_DIR}/build
#	  && curl ${OPENAPI_URL} | jsonpatch - ${ROOT_DIR}/openapi-patch.json > openapi3.json \

gen-test:
	rm -rf ${ROOT_DIR}/build/sdk_client
	cd ${ROOT_DIR}/build \
		&& curl ${OPENAPI_URL} > openapi3.json \
		&& openapi-python-client generate --path openapi3.json --config ${ROOT_DIR}/config.yml \


add-license:
	licenseheaders -t .license.tmpl -y 2023-$(shell date +%Y) -f ivcap_client/*.py
	licenseheaders -t .license.tmpl -y 2023-$(shell date +%Y) -d ivcap_client/client

docs:
	@echo "Building MkDocs documentation..."
	poetry run poe docs

docs-mkdocs:
	@echo "Building MkDocs documentation..."
	poetry run poe docs

docs-serve:
	@echo "Serving MkDocs documentation at http://localhost:8000"
	poetry run poe docs-serve

docs-clean:
	@echo "Cleaning MkDocs documentation..."
	poetry run poe docs-clean

clean:
	rm -rf *.egg-info
	rm -rf dist
	find ${ROOT_DIR} -name __pycache__ | xargs rm -r
	rm -rf ${ROOT_DIR}/docs/site

.PHONY: docs docs-mkdocs docs-serve docs-clean help clean
