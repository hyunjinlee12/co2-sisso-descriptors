.PHONY: help check lint clean

help:
	@echo "Available targets:"
	@echo "  check   Verify SISSO++ binary and Python module are reachable"
	@echo "  lint    Run pre-commit on all tracked files"
	@echo "  clean   Remove Python caches and notebook checkpoints"
	@echo ""
	@echo "Activate the environment first:"
	@echo "  source scripts/activate_sisso.sh"

check:
	@command -v sisso++ >/dev/null \
		&& echo "sisso++ binary OK: $$(command -v sisso++)" \
		|| echo "sisso++ NOT FOUND — did you run 'source scripts/activate_sisso.sh'?"
	@python -c "import sissopp; print('sissopp module OK:', sissopp.__file__)" 2>&1

lint:
	pre-commit run --all-files

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
