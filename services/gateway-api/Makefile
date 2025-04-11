# Variables
APP_NAME ?= gateway-api
PYTHON := $(shell command -v python3 || command -v python)
PYTHONPATH := $(shell pwd)

# Virtual enviroment paths
VENV_NAME ?= default_venv
VENV := .venv
VENV_DEV := .venv-dev

# Colors
USE_COLOUR ?= 1
COLOUR_RED := $(if $(USE_COLOUR),\033[0;31m,)
END_COLOUR := $(if $(USE_COLOUR),\033[0m,)

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make venv      - Create virtual environment and install dependencies"
	@echo "  make venv-dev  - Create virtual environment and install dev dependencies"
	@echo "  make clean     - Remove temporary files and virtual environment"


.PHONY: create-venv
create-venv:
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "$(COLOUR_RED)Virtual environment $(VENV_NAME) already exists.$(END_COLOUR)"; \
		exit 1; \
	fi
	$(PYTHON) -m venv $(VENV_NAME); \
	$(VENV_NAME)/bin/pip install --upgrade pip

.PHONY: venv
venv:
	$(MAKE) create-venv VENV_NAME="$(VENV)"
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: venv-dev
venv-dev:
	$(MAKE) create-venv VENV_NAME="$(VENV_DEV)"
	$(VENV_DEV)/bin/pip install -r requirements-dev.txt

.PHONY: clean
clean:
	rm -rf $(VENV) $(VENV_DEV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
