# Variables
PYTEST = python -m pytest

# Install dependencies
install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

# Run tests with coverage on multiple packages and notebook validation
test:
	$(PYTEST) -vvv --cov=hello --cov=greeting --cov=smath --cov=web tests
	$(PYTEST) --nbval notebook.ipynb

# Run tests in debug mode, dropping to pdb on failure
debug:
	$(PYTEST) -vv --pdb

# Run a single specific test
one-test:
	$(PYTEST) -vv tests/test_greeting.py::test_my_name4

# Run tests with pdb debugger, stop after 4 failures
debugthree:
	$(PYTEST) -vv --pdb --maxfail=4

# Format Python files using black
format:
	black *.py

# Lint Python files with pylint, disabling R and C messages (refactor and convention)
lint:
	pylint --disable=R,C *.py

# Run FastAPI app with uvicorn on all interfaces, port 8000 with autoreload
run:
	uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

# Clean pycache and compiled python files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Default target: install dependencies, lint, test, and format
all: install lint test format
