.PHONY: setup-env setup-install setup code run-local run

setup-env:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Virtual environment created."

setup-install:
	@echo "Installing dependencies..."
	source .venv/bin/activate && pip install -r requirements.txt
	@echo "Dependencies installed."

setup: setup-env setup-install

code:
	source .venv/bin/activate && code .

run-local:
	sh .venv/bin/activate && python3 run/local/main.py

run: run-local