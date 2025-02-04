export POETRY_ENABLED := 1

.PHONY: help

SHELL=bash

# Show this help
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

# Install python dependencies
init_mac:
	./init_dos.sh
	source .venv/bin/activate

init_win:
	./init_win.sh
	.venv/Scripts/Activate.ps1

## Runs black formatter, and isort
fix:
	@printf " >>> $(CYAN)Running isort$(COFF)\n"
	isort src tests
	@printf " >>> $(GREEN)isort done$(COFF)\n"
	@printf "$(CYAN)Auto-formatting with black$(COFF)\n"
	black src tests
	@printf " >>> $(GREEN)black done$(COFF)\n"

test_coverage:
	@echo "Running tests with coverage..."
	pytest --cov=src/mdc_logger --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"