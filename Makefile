.PHONY: build clean test check dev all ci

# Complete build process
all: clean build test

# Build JavaScript bundle
build:
	cd js && pnpm install && pnpm build
	@echo "✅ JavaScript bundle built"

# CI-specific build (assumes Nix environment)
ci: build check
	@echo "✅ CI checks complete"

# Development mode (watch for changes)
dev:
	cd js && pnpm dev

# Clean everything - back to fresh git clone state
clean:
	rm -rf js/dist src/markmap_anywidget/static
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf .coverage htmlcov
	rm -rf .vscode
	rm -f *.tmp *.temp *.log
	rm -f .eslintcache .npm .yarn-integrity
	rm -rf node_modules js/node_modules
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "🧹 Cleaned to fresh git clone state!"


# Run tests
test:
	uv run pytest

# Run all quality checks
check: lint type-check test
	@echo "✅ All checks passed!"

# Lint code
lint:
	uv run ruff check src/ examples/ tests/

# Type check
type-check:
	uv run mypy src/

# Format code
format:
	uv run ruff format src/ examples/ tests/
