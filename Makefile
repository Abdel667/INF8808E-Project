.PHONY: run clean lint install freeze setup format help


run:
	cd ./src && python server.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name __pycache__ -exec rm -rf {} \; 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} \; 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} \; 2>/dev/null || true

lint:
	ruff check .

install:
	pip install -r requirements.linux.txt

freeze:
	pip freeze > requirements.linux.txt
	@echo "Requirements frozen to requirements.linux.txt"

setup:
	@-if command -v deactivate >/dev/null 2>&1; then \
		echo "Deactivating current virtual environment..."; \
		deactivate; \
	fi
	@-if [ -d "venv" ]; then \
		echo "Removing existing virtual environment..."; \
		rm -rf venv; \
	fi
	@echo "Creating new virtual environment..."
	@python3.8 -m venv venv
	@echo "Virtual environment created. Activate it with 'source venv/bin/activate' (Linux/macOS) or 'venv\\Scripts\\activate' (Windows)"
	@echo "Activate it with 'source venv/bin/activate'"
	@echo "Then run 'make install' to install dependencies"

format:
	ruff format .

help:
	@echo "Available commands:"
	@echo "  make run      - Run the server application"
	@echo "  make clean    - Clean up Python cache files"
	@echo "  make lint     - Run linting with ruff"
	@echo "  make format   - Format code with ruff"
	@echo "  make install  - Install project dependencies"
	@echo "  make freeze   - Update requirements.linux.txt with current dependencies"
	@echo "  make setup    - Create virtual environment"
	@echo "  make test     - Run tests"
	@echo "  make remise   - Create a zip with all Python files at root level"
	@echo "  make help     - Show this help message"
