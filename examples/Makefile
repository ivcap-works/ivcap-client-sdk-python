ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


list-services:
	@${MAKE} SCRIPT=list_services.py run-script

list-artifacts:
	@${MAKE} SCRIPT=list_artifacts.py run-script

upload-artifact:
	@${MAKE} SCRIPT=upload_artifact.py run-script


search-aspect:
	@${MAKE} SCRIPT=search_aspect.py run-script

x:
	env PYTHONPATH=${ROOT_DIR}/.. \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	poetry run python search_aspect.py

place-job:
	env PYTHONPATH=${ROOT_DIR}/.. \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	poetry run python place_job.py

SCRIPT=
run-script:
	@env PYTHONPATH=${ROOT_DIR}/.. \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	poetry run python ${SCRIPT}
