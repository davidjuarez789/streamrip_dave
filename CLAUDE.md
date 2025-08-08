# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Streamrip is a Python CLI application for downloading music from Qobuz, Deezer, Tidal, and SoundCloud. It supports high-resolution audio, concurrent downloads, and comprehensive metadata tagging.

## Development Commands

### Setup
```bash
poetry install              # Install dependencies
poetry install --all-extras # Install with optional SSL support
```

### Testing
```bash
pytest                     # Run all tests
poetry run pytest         # Run tests through Poetry
pytest -v                 # Verbose test output
pytest tests/test_specific.py::TestClass::test_method  # Run single test
```

### Linting and Formatting
```bash
# Linting (use Ruff as primary linter)
ruff check .              # Check for linting issues
ruff check --fix .        # Fix auto-fixable issues
poetry run ruff check .   # Run through Poetry

# Formatting
black .                   # Format code
poetry run black .        # Format through Poetry
```

### Building and Running
```bash
poetry build              # Build distribution packages
poetry run rip            # Run the CLI
rip --help               # Show CLI help (if installed)
```

## Architecture Overview

### Core Components

1. **Client Layer** (`streamrip/client/`)
   - Service-specific API clients (Deezer, Qobuz, Tidal, SoundCloud)
   - Each client implements async methods for authentication and content fetching
   - Handles rate limiting and connection pooling

2. **Media Layer** (`streamrip/media/`)
   - Domain objects for tracks, albums, playlists, artists
   - Coordinates downloading, conversion, and metadata tagging
   - Implements concurrent download strategies

3. **CLI Layer** (`streamrip/rip/`)
   - Click-based command interface
   - Handles user interaction, search, and configuration
   - Entry point: `streamrip.rip:rip`

### Key Patterns

- **Async Everything**: Uses asyncio throughout for concurrent operations
- **Configuration**: TOML-based config at `~/.config/streamrip/config.toml`
- **Database**: SQLite database tracks downloaded content to avoid duplicates
- **Error Handling**: Comprehensive error handling with retry logic for network operations

### Important Considerations

1. **Branch Strategy**: Development happens on `dev` branch, not `main`
2. **Testing**: Tests use fixtures for API responses - avoid making real API calls
3. **Dependencies**: Uses Poetry for dependency management - always use `poetry add` for new dependencies
4. **Type Hints**: Project uses type hints extensively - maintain this pattern
5. **Async Context**: Most operations are async - use `async`/`await` patterns consistently

### Common Tasks

- **Adding a new music service**: Create client in `streamrip/client/`, implement required methods
- **Modifying CLI commands**: Edit `streamrip/rip/cli.py`, follow Click patterns
- **Working with metadata**: See `streamrip/metadata/` for tagging logic
- **Database operations**: Check `streamrip/db.py` for schema and operations