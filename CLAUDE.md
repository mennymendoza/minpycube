# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

minpycube is a minimal Python library for Rubik's Cube simulation with zero dependencies. The library provides a single core class `RCube` that represents a 3x3 Rubik's Cube with standard move notation support.

## Architecture

### Core Components

**`src/minpycube/rcube.py`** - Contains the entire cube implementation:
- `RCube` class: Main cube representation using a 6x3x3 matrix (`cube_mat`) where each face is a 3x3 grid
- Face constants: F(0), R(1), B(2), L(3), U(4), D(5) representing Front, Right, Back, Left, Up, Down
- Operation system: 18 standard cube operations (U, D, R, L, F, B and their reverses denoted with `-` prefix, plus middle layer moves E, M, S)
- State representation: Each cell stores an integer 0-5 representing its original face color
- Fitness calculation: `calc_fit()` returns 54 when solved (9 matching cells per face)

### Key Implementation Details

- Operations are implemented through a combination of face rotations (`__rotatef_c`/`__rotatef_cc`) and layer rotations (horizontal, vertical, clockwise/counter-clockwise)
- Reverse operations are denoted with `-` prefix (e.g., `-U` is reverse of `U`)
- Color output uses ANSI escape codes for terminal display
- The `invert_op()` static method toggles between an operation and its inverse

## Development Commands

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_rcube.py

# Run single test
uv run pytest tests/test_rcube.py::test_rotate
```

### Package Management
```bash
# Add dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Sync dependencies
uv sync
```

### Building
```bash
# Build package (uses hatchling)
uv build
```

## Project Structure

- `src/minpycube/` - Single module library
- `tests/` - Pytest test suite validating rotation operations and fitness calculations
- Uses `uv` for package management with hatchling as build backend