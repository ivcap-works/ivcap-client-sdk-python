
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SRC_DIR:=${ROOT_DIR}/src

# Docker image name for the docs build
DOCS_IMAGE   := ivcap-docs
# The whole repo is mounted at /project; workdir is /project/docs so that
# pymdownx.snippets base_path: [".."] resolves to the project root.
# PYTHONPATH=/project lets mkdocstrings/griffe find ivcap_client without installing it.
DOCS_DOCKER  := docker run --rm \
  -v "$(ROOT_DIR):/project" \
  -e PYTHONPATH=/project \
  -w /project/docs \
  $(DOCS_IMAGE)

.PHONY: help copyx lint typecheck check docs-image docs-build docs-serve docs-deploy docs docs-mkdocs docs-clean

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
	@echo "  docs-image    - Build the docs Docker image (run once, or after changing docs/requirements.txt)"
	@echo "  docs-build    - Build MkDocs static site via Docker"
	@echo "  docs-serve    - Serve MkDocs docs locally with live reload via Docker (http://localhost:8000)"
	@echo "  docs-deploy   - Deploy docs to gh-pages via Docker"
	@echo "  docs          - Alias for docs-build"
	@echo "  docs-mkdocs   - Alias for docs-build"
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
OPENAPI_CACHED=${ROOT_DIR}/openapi3.json

gen:
	@if ! poetry run bash -c "command -v openapi-python-client > /dev/null 2>&1"; then \
		echo ">>>\n>>> You need to first install 'openapi-python-client'\n>>>"; \
		exit -1; \
	fi
	@echo "Downloading OpenAPI spec..."
	@mkdir -p ${ROOT_DIR}/build
	@curl -s ${OPENAPI_URL} > ${ROOT_DIR}/build/openapi3.json.new
	@if [ -f "${OPENAPI_CACHED}" ] && diff -q "${OPENAPI_CACHED}" "${ROOT_DIR}/build/openapi3.json.new" > /dev/null 2>&1; then \
		echo "OpenAPI spec unchanged — skipping code generation."; \
		rm ${ROOT_DIR}/build/openapi3.json.new; \
	else \
		echo "OpenAPI spec changed (or not yet cached) — regenerating client..."; \
		cp ${ROOT_DIR}/build/openapi3.json.new ${OPENAPI_CACHED}; \
		rm -rf ${ROOT_DIR}/build/sdk_client; \
		cp ${OPENAPI_CACHED} ${ROOT_DIR}/build/openapi3.json; \
		cd ${ROOT_DIR}/build \
		  && poetry run python ${ROOT_DIR}/patch_openapi.py openapi3.json \
			&& poetry run openapi-python-client generate --path openapi3.json --config ${ROOT_DIR}/config.yml \
			&& poetry run python ${ROOT_DIR}/fix_auto_generated.py \
			&& cd sdk_client/ivcap_client && mkdir client && mv *.py client \
			&& cd ${ROOT_DIR}; \
		rm -fr ${SRC_DIR}/api ${SRC_DIR}/models ${SRC_DIR}/client \
			&& mkdir -p ${SRC_DIR}/api ${SRC_DIR}/models ${SRC_DIR}/client \
			&& mv ${ROOT_DIR}/build/sdk_client/ivcap_client/* ${SRC_DIR} \
			&& mv ${SRC_DIR}/client/errors.py ${SRC_DIR}/client/types.py ${SRC_DIR} \
			&& sed -i '' '1s/^/#\n#### DO NOT EDIT ####\n#\n/' ${SRC_DIR}/types.py ${SRC_DIR}/errors.py; \
	fi

#	rm -r ${ROOT_DIR}/build
#	  && curl ${OPENAPI_URL} | jsonpatch - ${ROOT_DIR}/openapi-patch.json > openapi3.json \

gen-test:
	rm -rf ${ROOT_DIR}/build/sdk_client
	cd ${ROOT_DIR}/build \
		&& curl ${OPENAPI_URL} > openapi3.json \
		&& openapi-python-client generate --path openapi3.json --config ${ROOT_DIR}/config.yml \


add-license:
	poetry run licenseheaders -t .license.tmpl -y 2023-$(shell date +%Y) -f ivcap_client/*.py
	poetry run licenseheaders -t .license.tmpl -y 2023-$(shell date +%Y) -d ivcap_client/client

docs-image:
	@echo "Building docs Docker image ($(DOCS_IMAGE))..."
	docker build -t $(DOCS_IMAGE) docs/

docs-build:
	@echo "Building MkDocs static site via Docker..."
	$(DOCS_DOCKER) build --strict

docs: docs-build

docs-mkdocs: docs-build

docs-serve:
	@echo "Serving MkDocs documentation at http://localhost:8000 (via Docker)..."
	docker run --rm -it -p 8000:8000 \
	  -v "$(ROOT_DIR):/project" \
	  -e PYTHONPATH=/project \
	  -w /project/docs \
	  $(DOCS_IMAGE) serve --dev-addr=0.0.0.0:8000

docs-deploy:
	@echo "Deploying docs to gh-pages via Docker..."
	docker run --rm \
	  -v "$(ROOT_DIR):/project" \
	  -v "$(HOME)/.ssh:/root/.ssh" \
	  -e PYTHONPATH=/project \
	  -w /project/docs \
	  $(DOCS_IMAGE) gh-deploy --force

docs-clean:
	@echo "Cleaning MkDocs build artifacts..."
	rm -rf $(ROOT_DIR)/docs/site $(ROOT_DIR)/docs/.mkdocs_cache

clean:
	rm -rf *.egg-info
	rm -rf dist
	find ${ROOT_DIR} -name __pycache__ | xargs rm -r
	rm -rf ${ROOT_DIR}/docs/site
