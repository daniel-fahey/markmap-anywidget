.PHONY: help build clean test check dev all ci build-js build-python

# =============================================================================
# HELP
# =============================================================================
# Default target when just running 'make'
.DEFAULT_GOAL := help

# Auto-generated help from target comments
help: ## Show this help message
	@echo "Usage: make [target] [VERSION=x.y.z]"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' | \
		sort
	@echo ""
	@echo "Version handling:"
	@echo "  Current version: $(VERSION)"
	@echo "  Override with:   make build VERSION=1.2.3"

# =============================================================================
# VERSION HANDLING
# =============================================================================
# Determine version: use git tag if on a tagged commit, otherwise use dev version
# Can be overridden by user: make build VERSION=1.2.3

VERSION ?= $(shell \
	if git describe --tags --exact-match HEAD >/dev/null 2>&1; then \
		git describe --tags --exact-match HEAD; \
	else \
		BASE_VERSION=$$(grep '^version = ' pyproject.toml | sd 'version = "([^"]+)"' '$$1'); \
		COMMIT_HASH=$$(git rev-parse --short HEAD); \
		echo "$${BASE_VERSION}.dev1+g$${COMMIT_HASH}"; \
	fi \
)

# =============================================================================
# PRIMARY TARGETS
# =============================================================================

all: clean build check ## Full build pipeline (clean, build, check)

build: build-js build-python ## Build JavaScript and Python packages
	@echo "✅ Build complete with version: $(VERSION)"

ci: build check ## Run CI checks (build + test + lint)
	@echo "✅ CI checks complete"

dev: ## Start development server (watch mode)
	cd js && pnpm dev

# =============================================================================
# BUILD COMPONENTS
# =============================================================================

build-js: ## Build JavaScript bundle only
	@echo "Building JavaScript bundle..."
	cd js && pnpm install && pnpm build
	@echo "✅ JavaScript bundle built"

build-python: ## Build Python package only
	@echo "Building Python package with version: $(VERSION)..."
	@cp pyproject.toml pyproject.toml.bak
	@sd '^version = ".*"' 'version = "$(VERSION)"' pyproject.toml
	@uv build || (mv pyproject.toml.bak pyproject.toml && exit 1)
	@mv pyproject.toml.bak pyproject.toml
	@echo "✅ Python package built"

# =============================================================================
# TESTING & VALIDATION
# =============================================================================

check: lint type-check test ## Run all quality checks
	@echo "✅ All checks passed!"

test: ## Run test suite
	uv run pytest

lint: ## Run code linter (ruff)
	uv run ruff check src/ examples/ tests/

type-check: ## Run type checker (mypy)
	uv run mypy src/

format: ## Format code with ruff
	uv run ruff format src/ examples/ tests/

# =============================================================================
# CLEANUP
# =============================================================================

clean: ## Remove all build artifacts and caches
	@echo "Cleaning build artifacts..."
	@rm -rf js/dist src/markmap_anywidget/static
	@rm -rf build dist *.egg-info
	@rm -rf .pytest_cache .mypy_cache .ruff_cache
	@rm -rf .coverage htmlcov
	@rm -rf .vscode
	@rm -f *.tmp *.temp *.log
	@rm -f .eslintcache .npm .yarn-integrity
	@rm -rf node_modules js/node_modules
	@rm -rf .venv
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "🧹 Cleaned to fresh git clone state!"