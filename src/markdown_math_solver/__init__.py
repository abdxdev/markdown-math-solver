"""Markdown Math Solver - Process Python code embedded in LaTeX math blocks in Markdown files."""

__version__ = "1.0.0"

from .solver import (
    Expr,
    ReplaceThis,
    ReplaceAll,
    NoOutput,
    store,
    find_py_block,
    execute_py,
    fmt,
    process_block,
    process_markdown,
)

__all__ = [
    "Expr",
    "ReplaceThis",
    "ReplaceAll",
    "NoOutput",
    "store",
    "find_py_block",
    "execute_py",
    "fmt",
    "process_block",
    "process_markdown",
]
