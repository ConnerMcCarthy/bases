# numbases

`numbases` is a small Python library for converting integers to and from
different positional number systems.

It currently supports integer bases from **2 to 36** and includes a placeholder
for future non-integer base work (like base-phi).

## Features

- Convert Python `int` values to base-`N` strings with `to_base`
- Parse base-`N` strings back to Python `int` values with `from_base`
- Supports negative values
- Uses digits `0-9` and uppercase letters `A-Z` (case-insensitive on parse)
- Includes a visual desktop UI for exploring base conversions
- Includes a browser-based web UI for EC2 and remote usage
- Includes a second web page for experimental non-integer bases (starting with base-phi)
- Validated by unit tests with `pytest`

## Install

From the project root:

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from numbases.bases import to_base, from_base

to_base(31, 16)      # "1F"
to_base(-10, 10)     # "-10"
to_base(5, 2)        # "101"

from_base("1f", 16)  # 31
from_base("-10", 10) # -10
from_base("101", 2)  # 5
```

## Visual Explorer UI

Launch the desktop app:

```bash
numbases-ui
```

Or without installing scripts:

```bash
python -m numbases.ui
```

If Tkinter is missing on Linux, install it first:

```bash
sudo apt-get install python3-tk
```

The UI requires a desktop session (an active display server).

The UI lets you:

- Enter a number and its input base
- Convert to decimal and common bases (`2`, `8`, `10`, `16`, `36`)
- Pick any custom output base from `2..36`
- Quickly test negative values and invalid input handling

## Web UI (Recommended for EC2)

Install web dependencies:

```bash
pip install -e ".[web]"
```

Run Streamlit bound to all interfaces:

```bash
numbases-web
```

Open port `8501` in your EC2 Security Group:

- Inbound rule: `Custom TCP`, port `8501`
- Source: your IP (recommended) or `0.0.0.0/0` (public)

Then open:

```text
http://<EC2_PUBLIC_IP>:8501
```

Example:

```text
http://54.123.45.67:8501
```

The web app now has multiple pages:

- `Base Explorer` (integer bases)
- `Non-Integer Bases` (experimental; starts with base-phi)

## API

### `to_base(n: int, base: int) -> str`

Converts an integer `n` into a string representation in `base`.

- `base` must be an integer in `2..36`
- Raises `TypeError` if `n` or `base` has the wrong type
- Raises `ValueError` if `base` is out of range

### `from_base(s: str, base: int) -> int`

Parses string `s` in `base` into an integer.

- Accepts leading `-` for negative values
- Parsing is case-insensitive
- `base` must be an integer in `2..36`
- Raises `TypeError` if `base` has the wrong type
- Raises `ValueError` for invalid strings/digits/base

### `to_base_phi(n: int) -> str`

Converts an integer to an approximate base-phi representation
using finite-precision greedy expansion.

## Run Tests

```bash
pytest
```

## Roadmap

- Implement non-integer base conversion algorithms (starting with base-phi)
- Add round-trip property tests across a wider input range
- Expand API docs and examples
