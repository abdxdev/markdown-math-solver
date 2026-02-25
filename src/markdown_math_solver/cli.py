"""Command-line interface for Markdown Math Solver."""

import sys
import argparse
from pathlib import Path

from . import __version__
from .solver import process_markdown, store


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="markdown-math-solver",
        description="Process Python code embedded in LaTeX math blocks in Markdown files.",
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the Markdown file to process",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path (default: <input>.output.md)",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    if not path.suffix == ".md":
        print(f"Warning: File does not have .md extension: {path}", file=sys.stderr)

    store.clear()

    content = path.read_text(encoding="utf-8")
    result = process_markdown(content)

    if args.output:
        out = Path(args.output)
    else:
        out = path.with_suffix(".output.md")

    out.write_text(result, encoding="utf-8")
    print(f"Output written to {out}")


if __name__ == "__main__":
    main()
