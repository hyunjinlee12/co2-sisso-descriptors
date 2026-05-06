.PHONY: help setup lint clean

help:
	@echo "Available targets:"
	@echo "  setup   Create/update conda env (run 'pre-commit install' after activate)"
	@echo "  lint    Run pre-commit on all tracked files"
	@echo "  clean   Remove Python caches and notebook checkpoints"

setup:
	conda env create -f environment.yml || conda env update -f environment.yml
	@echo ""
	@echo "Next: conda activate co2-sisso && pre-commit install"

lint:
	pre-commit run --all-files

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
