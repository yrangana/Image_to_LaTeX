# Variables
FLASK_APP = app.py
FLASK_PORT = 5000
PYTHON = python
ENV = .env

# Default target
.PHONY: all
all: run

# Run the Flask application
.PHONY: run
run:
	@echo "Running Flask app..."
	$(PYTHON) $(FLASK_APP)

# Run unit tests with pytest
.PHONY: test
test:
	@echo "Running tests with pytest..."
	$(PYTHON) -m pytest -vv

# Run pylint for code linting
.PHONY: lint
lint:
	@echo "Running pylint for linting..."
	pylint --disable=R,C $(FLASK_APP)

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Format code with black
.PHONY: format
format:
	@echo "Formatting code with black..."
	black $(FLASK_APP)

# Clean up temporary files
.PHONY: clean
clean:
	@echo "Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name ".DS_Store" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# Load environment variables and run Flask app
.PHONY: run-env
run-env:
	@echo "Running Flask app with environment variables from $(ENV)..."
	@export $(shell sed 's/=.*//' $(ENV)) && $(PYTHON) $(FLASK_APP)

# Help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make run       - Run the Flask application"
	@echo "  make test      - Run tests with pytest"
	@echo "  make lint      - Run pylint for linting"
	@echo "  make format    - Format code with black"
	@echo "  make install   - Install dependencies from requirements.txt"
	@echo "  make clean     - Clean up temporary files"
	@echo "  make run-env   - Run Flask app with .env variables loaded"
