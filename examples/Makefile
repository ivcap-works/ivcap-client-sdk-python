ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# ─── Credentials (fetched from the active ivcap context) ──────────────────────
# Using recursive '=' so the shell commands run only when a target actually fires.
IVCAP_URL    = $(shell ivcap context get url)
IVCAP_JWT    = $(shell ivcap context get access-token --refresh-token)
IVCAP_ACCT   = $(shell ivcap context get account-id)

# Common env + interpreter — always run from the examples directory so that
# relative imports (e.g. "from _common import …") resolve correctly.
RUN = cd $(ROOT_DIR) && \
    env PYTHONPATH=$(ROOT_DIR)/.. \
        IVCAP_URL=$(IVCAP_URL) \
        IVCAP_JWT=$(IVCAP_JWT) \
        IVCAP_ACCOUNT_ID=$(IVCAP_ACCT) \
    poetry run python

# ─── Help ─────────────────────────────────────────────────────────────────────
.PHONY: help
help:
	@echo ""
	@echo "Usage: make <target>   (run from the examples/ directory or the repo root)"
	@echo "Credentials are read automatically from the active 'ivcap' CLI context."
	@echo ""
	@echo "── Read-only (safe against any deployment) ──────────────────────────────"
	@echo "  list-services          List all registered services"
	@echo "  find-service           Find services by name / filter"
	@echo "  list-artifacts         List recent artifacts (limit 5)"
	@echo "  download-artifact      Download a specific artifact to /tmp"
	@echo "  search-aspect          Search aspects by schema + filter"
	@echo "  list-secrets           List secrets"
	@echo ""
	@echo "── Write / mutating ─────────────────────────────────────────────────────"
	@echo "  upload-artifact        Upload a test image artifact"
	@echo "  manage-aspect          Full aspect lifecycle (add/list/get/update/retract) — leaves nothing active"
	@echo "  manage-collection      Full collection lifecycle (create/add/remove/retract) — leaves nothing active"
	@echo ""
	@echo "── Jobs ─────────────────────────────────────────────────────────────────"
	@echo "  run-async-job          Submit a batch job and wait for result (async)"
	@echo "  run-go-mapper          Run the GO term mapper service"
	@echo "  find-unique-gene       Run the unique gene finder service"
	@echo "  test-failed-service    Submit a job to a deliberately failing service"
	@echo ""
	@echo "── Stress tests ─────────────────────────────────────────────────────────"
	@echo "  batch-stress-test      Batch service stress test"
	@echo "  lambda-stress-test     Lambda service stress test"
	@echo "  locus-stress-test      Locus stress test"
	@echo ""
	@echo "── Groups ───────────────────────────────────────────────────────────────"
	@echo "  test-read              All read-only examples"
	@echo "  test-write             Write/mutating examples"
	@echo "  test-jobs              All job-submission examples"
	@echo "  test-all               test-read + test-write (excludes stress tests)"
	@echo ""

# ─── Read-only targets ────────────────────────────────────────────────────────

.PHONY: list-services
list-services:
	$(RUN) list_services.py

.PHONY: find-service
find-service:
	$(RUN) find_service_by_name.py

.PHONY: list-artifacts
list-artifacts:
	$(RUN) list_artifacts.py

.PHONY: download-artifact
download-artifact:
	$(RUN) download_artifact.py

.PHONY: search-aspect
search-aspect:
	$(RUN) search_aspect.py

.PHONY: list-secrets
list-secrets:
	$(RUN) list_secrets.py

# ─── Write / mutating targets ─────────────────────────────────────────────────

.PHONY: upload-artifact
upload-artifact:
	$(RUN) upload_artifact.py

.PHONY: manage-aspect
manage-aspect:
	$(RUN) manage_aspect.py

.PHONY: manage-collection
manage-collection:
	$(RUN) manage_collection.py

# ─── Job targets ──────────────────────────────────────────────────────────────

.PHONY: run-async-job
run-async-job:
	$(RUN) run_async_job.py

.PHONY: run-go-mapper
run-go-mapper:
	$(RUN) run_go_mapper.py

.PHONY: find-unique-gene
find-unique-gene:
	$(RUN) find_unique_gene.py

.PHONY: test-failed-service
test-failed-service:
	$(RUN) test_failed_service.py

# ─── Stress tests ─────────────────────────────────────────────────────────────

.PHONY: batch-stress-test
batch-stress-test:
	$(RUN) batch_stress_test.py

.PHONY: lambda-stress-test
lambda-stress-test:
	$(RUN) lambda_stress_test.py

.PHONY: locus-stress-test
locus-stress-test:
	$(RUN) locus_stress_test.py

# ─── Group targets ────────────────────────────────────────────────────────────

.PHONY: test-read
test-read: list-services find-service list-artifacts search-aspect list-secrets

.PHONY: test-write
test-write: upload-artifact manage-aspect manage-collection

.PHONY: test-jobs
test-jobs: run-async-job run-go-mapper find-unique-gene

.PHONY: test-all
test-all: test-read test-write

# ─── Low-level helper (kept for ad-hoc use: make SCRIPT=foo.py run-script) ────

SCRIPT =
.PHONY: run-script
run-script:
	@$(RUN) $(SCRIPT)
