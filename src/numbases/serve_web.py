"""CLI entry point for serving the Streamlit web UI."""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    try:
        from streamlit.web import cli as stcli
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "streamlit is not installed. Run `pip install -e \".[web]\"` first."
        ) from exc

    app_path = Path(__file__).with_name("web_ui.py")
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.address",
        "0.0.0.0",
        "--server.port",
        "8501",
    ]
    raise SystemExit(stcli.main())


if __name__ == "__main__":
    main()
