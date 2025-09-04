# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2025-09-04

### Changed

- Moved `watchdog` and `marimo` from main dependencies to dev dependencies only
- Updated all package dependencies to their latest versions

## [0.1.2] - 2025-09-04

### Fixed

- Fixed CI/CD workflow to build JavaScript bundle before packaging Python distribution
- Added `[tool.uv.build-backend]` configuration to include static files in package

### Changed

- Updated `make build` to build both JavaScript bundle and Python package
- Simplified GitHub Actions workflow to use `make` targets consistently

## [0.1.1] - 2025-09-04

### Added

- First tagged release