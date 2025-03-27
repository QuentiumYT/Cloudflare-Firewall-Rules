# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

- Nothing yet!

## [2.1.0] - Misc bugs & rule position (2025-03-27)

- Fix misc bugs & examples (Thanks @chaud #2)
- Add support for rule position (Thanks @chaud #2)
- Lint & format code with ruff

## [2.0.0] - Complete rewrite for new WAF API (2024-01-26)

> ### Renamed the project to Cloudflare WAF custom rules since the API changed and will be removed on may 2024

### Added

- Raise multiple `Error` in some methods (added docstring)
- New ruleset methods before accessing rules: `get_rulesets`, `rulesets`, `get_custom_ruleset`
- Timeout for each requests to Cloudflare
- Pass more IDs in method's responses (zone_id, custom_ruleset_id)
- Rule by ID or name are named arguments now
- More examples in the documentation & explain void methods

### Fixed

- Updated wrong docstrings & few mistakes
- Count of results key no longer provided
- Updated available actions to `managed_challenge, js_challenge, challenge, block, skip, log`
- Prefer .patch method instead of .put for updating rules

### Changed

- Updated examples & documentation for new API wrapper
- Complete rewrite of the core with new WAF API
- Adapted docstrings to new API responses (i.e. filter removed)
- Methods do not return an `Error` but raise it instead
- Moved `beautify()` method into `Utils` class
- Renamed "Test" rules to more concise examples
- "paused" rule parameter (renamed to "active")
- A file extension for rule_file is now recommended (.txt fallback)
  
### Project changes

- Switched from setup.py to pyproject.toml
- Moved all source to src/ directory for pyproject.toml convention
- Use vx.x.x tags now for semver convention
- Updated github action to keep documentation changes history
- Updated requirements & added optional sphinx-autobuild
- Simplified gitignore file with less entries
- Added a new CHANGELOG file

### Removed

- .env.example file because it's user's choice to use it
- setup.py as it's a deprecated way of installing packages
- `auth_bearer()` & `auth()` methods because they were too global aliases
- "priority" rule parameter (no longer available)
