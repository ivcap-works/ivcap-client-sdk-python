ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


list_services:
	env PYTHONPATH=${ROOT_DIR}/../src \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	python list_services.py

list_artifacts:
	env PYTHONPATH=${ROOT_DIR}/../src \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	python list_artifacts.py

upload_artifact:
	env PYTHONPATH=${ROOT_DIR}/../src \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	python upload_artifact.py

search_metadata:
	env PYTHONPATH=${ROOT_DIR}/../src \
		IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	python search_metadata.py
