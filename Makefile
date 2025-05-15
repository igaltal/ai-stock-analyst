.PHONY: setup test run run-api run-ui clean

# Python executable path
PYTHON = venv/bin/python

# Set up the virtual environment and install dependencies
setup:
	python -m venv venv
	venv/bin/pip install -r requirements.txt

# Run all tests
test:
	$(PYTHON) -m unittest discover -s tests

# Run both API and UI
run:
	$(PYTHON) run.py

# Run only the API
run-api:
	$(PYTHON) run.py --api-only

# Run only the UI
run-ui:
	$(PYTHON) run.py --ui-only

# Clean temporary files and caches
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 