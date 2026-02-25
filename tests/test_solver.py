"""
Pytest tests for markdown-math-solver
"""

import pytest
import sys
from pathlib import Path
from markdown_math_solver import (
    Expr,
    ReplaceThis,
    ReplaceAll,
    find_py_block,
    execute_py,
    fmt,
    process_block,
    process_markdown,
    store,
)
from markdown_math_solver.solver import _NoOutput


class TestExpr:
    """Test the Expr class"""

    def test_str(self):
        e = Expr("1+2")
        assert str(e) == "1+2"

    def test_repr(self):
        e = Expr("1+2")
        assert repr(e) == "1+2"

    def test_add_string(self):
        e = Expr("x")
        assert e + " = 5" == "x = 5"

    def test_radd_string(self):
        e = Expr("x")
        assert "Value: " + e == "Value: x"

    def test_bind_single(self):
        e = Expr(r"\frac{param(a)}{param(b)}")
        bound = e.bind(a=3)
        assert str(bound) == r"\frac{3}{param(b)}"

    def test_bind_multiple(self):
        e = Expr(r"\frac{param(a)}{param(b)}")
        bound = e.bind(a=3, b=4)
        assert str(bound) == r"\frac{3}{4}"

    def test_unbind_restores_original(self):
        e = Expr(r"\frac{param(a)}{param(b)}")
        bound = e.bind(a=3, b=4)
        unbound = bound.unbind()
        assert str(unbound) == r"\frac{param(a)}{param(b)}"

    def test_unbind_after_partial_bind(self):
        e = Expr(r"param(x) + param(y)")
        bound = e.bind(x=5)
        assert str(bound) == r"5 + param(y)"
        unbound = bound.unbind()
        assert str(unbound) == r"param(x) + param(y)"

    def test_unbind_chain(self):
        e = Expr(r"param(a) * param(b)")
        bound1 = e.bind(a=2)
        bound2 = bound1.bind(b=3)
        unbound = bound2.unbind()
        assert str(unbound) == r"param(a) * param(b)"

    def test_unbind_selective_single(self):
        e = Expr(r"\frac{param(a)}{param(b)}")
        bound = e.bind(a=3, b=4)
        unbound = bound.unbind("a")
        assert str(unbound) == r"\frac{param(a)}{4}"

    def test_unbind_selective_multiple(self):
        e = Expr(r"param(x) + param(y) + param(z)")
        bound = e.bind(x=1, y=2, z=3)
        unbound = bound.unbind("x", "z")
        assert str(unbound) == r"param(x) + 2 + param(z)"

    def test_unbind_nonexistent_var(self):
        e = Expr(r"param(a) + param(b)")
        bound = e.bind(a=5, b=10)
        # Unbinding a var that wasn't bound should have no effect
        unbound = bound.unbind("c")
        assert str(unbound) == r"5 + 10"

    def test_call_simple(self):
        e = Expr("1+2")
        assert float(e()) == 3.0

    def test_call_with_bind(self):
        e = Expr(r"\frac{param(x)}{2}")
        result = e(x=4)
        assert float(result) == 2.0

    def test_call_fraction(self):
        e = Expr(r"\frac{1}{2}")
        assert float(e()) == 0.5

    def test_call_with_text_stripped(self):
        e = Expr(r"\text{Label: }5+3")
        assert float(e()) == 8.0

    def test_call_with_equals(self):
        e = Expr("x = 5 + 3")
        assert float(e()) == 8.0


class TestReplaceThis:
    """Test ReplaceThis class"""

    def test_string_value(self):
        r = ReplaceThis("hello")
        assert r.value == "hello"

    def test_numeric_value(self):
        r = ReplaceThis(42)
        assert r.value == "42"


class TestReplaceAll:
    """Test ReplaceAll class"""

    def test_string_value(self):
        r = ReplaceAll("replaced")
        assert r.value == "replaced"

    def test_numeric_value(self):
        r = ReplaceAll(3.14)
        assert r.value == "3.14"


class TestFindPyBlock:
    """Test find_py_block function"""

    def test_simple(self):
        result = find_py_block("py(x = 1)")
        assert result == (0, 9, "x = 1")

    def test_with_prefix(self):
        result = find_py_block("hello py(code)")
        assert result == (6, 14, "code")

    def test_no_match(self):
        result = find_py_block("no python here")
        assert result is None

    def test_no_space_before_invalid(self):
        # 100py( should not match
        result = find_py_block("100py(x)")
        assert result is None

    def test_letter_before_invalid(self):
        # entropy( should not match
        result = find_py_block("entropy(5,9)")
        assert result is None

    def test_paren_before_valid(self):
        # param(x)py( IS valid - ) is not alphanumeric
        result = find_py_block("param(x)py(y)")
        assert result == (8, 13, "y")

    def test_space_before_valid(self):
        result = find_py_block("100 py(x)")
        assert result == (4, 9, "x")

    def test_nested_parens(self):
        result = find_py_block("py(func(a, b))")
        assert result == (0, 14, "func(a, b)")


class TestExecutePy:
    """Test execute_py function"""

    def setup_method(self):
        store.clear()

    def test_assignment(self):
        result = execute_py("x = THIS", "1+2")
        assert isinstance(result, _NoOutput)
        assert "x" in store
        assert str(store["x"]) == "1+2"

    def test_replace_this(self):
        result = execute_py("ReplaceThis('hello')", "")
        assert isinstance(result, ReplaceThis)
        assert result.value == "hello"

    def test_replace_all(self):
        result = execute_py("ReplaceAll('world')", "")
        assert isinstance(result, ReplaceAll)
        assert result.value == "world"

    def test_builtin_str(self):
        store["x"] = Expr("1+2")
        result = execute_py("ReplaceThis(str(x))", "")
        assert result.value == "1+2"

    def test_builtin_abs(self):
        result = execute_py("ReplaceThis(str(abs(-5)))", "")
        assert result.value == "5"

    def test_chained_statements(self):
        result = execute_py("a = THIS; ReplaceThis(str(a))", "test")
        assert result.value == "test"


class TestProcessBlock:
    """Test process_block function"""

    def setup_method(self):
        store.clear()

    def test_no_py(self):
        result = process_block("1 + 2")
        assert result is None

    def test_assignment_removes_py(self):
        result = process_block("1+2 py(x = THIS)")
        assert result == "1+2"

    def test_replace_this(self):
        store["val"] = Expr("5")
        result = process_block("py(ReplaceThis(str(val)))")
        assert result == "5"

    def test_replace_all(self):
        result = process_block("ignored py(ReplaceAll('replaced'))")
        assert result == "replaced"

    def test_empty_replace_all_deletes(self):
        result = process_block("py(ReplaceAll(''))")
        assert result == "__DELETE__"

    def test_multiple_py_blocks(self):
        result = process_block("py(ReplaceThis('A')) py(ReplaceThis('B'))")
        assert result == "A B"


class TestProcessMarkdown:
    """Test process_markdown function"""

    def setup_method(self):
        store.clear()

    def test_no_math(self):
        result = process_markdown("Hello world")
        assert result == "Hello world"

    def test_math_without_py(self):
        result = process_markdown("$1 + 2$")
        assert result == "$1 + 2$"

    def test_inline_math_with_py(self):
        result = process_markdown("$5 py(x = THIS)$")
        assert result == "$5$"

    def test_display_math_with_py(self):
        result = process_markdown("$$10 py(y = THIS)$$")
        assert result == "$$10$$"

    def test_delete_empty_block(self):
        result = process_markdown("before $py(ReplaceAll(''))$ after")
        assert result == "before  after"

    def test_preserve_surrounding_text(self):
        result = process_markdown("Text $1+1 py(z = THIS)$ more text")
        assert result == "Text $1+1$ more text"


class TestFmt:
    """Test fmt formatting function"""

    def test_integer(self):
        assert fmt(5.0) == "5"

    def test_float(self):
        result = fmt(3.14159)
        assert result.startswith("3.14")

    def test_trailing_zeros_stripped(self):
        assert fmt(2.500000) == "2.5"

    def test_non_numeric(self):
        assert fmt("hello") == "hello"


class TestIntegration:
    """Integration tests"""

    def setup_method(self):
        store.clear()

    def test_define_and_use(self):
        # Define
        result1 = process_markdown("$1+2+3 py(sum = THIS)$")
        assert result1 == "$1+2+3$"

        # Use
        result2 = process_markdown("$py(ReplaceThis(str(sum)))$")
        assert result2 == "$1+2+3$"

    def test_define_and_evaluate(self):
        # Define
        process_markdown("$5+5 py(ten = THIS)$")

        # Evaluate
        result = process_markdown("$py(ReplaceThis(ten()))$")
        assert result == "$10$"

    def test_parameterized_expression(self):
        # Define with params
        process_markdown(r"$\frac{param(a)}{param(b)} py(ratio = THIS)$")

        # Bind and show
        result = process_markdown("$py(ReplaceThis(str(ratio.bind(a=3, b=4))))$")
        assert r"\frac{3}{4}" in result

    def test_bind_and_evaluate(self):
        # Define
        process_markdown(r"$param(x) + param(y) py(add = THIS)$")

        # Call with args
        result = process_markdown("$py(ReplaceThis(add(x=10, y=5)))$")
        assert result == "$15$"

    def test_full_computation_with_equals(self):
        # Define
        process_markdown("$1+2 py(expr = THIS)$")

        # Show expr = result
        result = process_markdown("$py(ReplaceAll(str(expr) + ' = ' + str(expr())))$")
        assert result == "$1+2 = 3$"

    def test_inline_bind_and_evaluate_with_fstring(self):
        result = process_markdown(
            r"$\frac{param(a)}{param(b)} py(ReplaceThis(f'= {THIS.bind(a=3, b=4)} = {THIS()}'))$"
        )
        assert result == r"$\frac{param(a)}{param(b)} = \frac{3}{4} = 0.75$"

    def test_implicit_output_like_jupyter(self):
        result = process_markdown(
            r"$\frac{param(a)}{param(b)} py(f'= {THIS.bind(a=3, b=4)} = {THIS()}')$"
        )
        assert result == r"$\frac{param(a)}{param(b)} = \frac{3}{4} = 0.75$"

    def test_implicit_output_simple_expr(self):
        result = process_markdown(r"$1 + 2 py(f'= {THIS()}')$")
        assert result == r"$1 + 2 = 3$"

    def test_implicit_output_variable(self):
        store["myvar"] = Expr("x^2")
        result = process_markdown(r"$py(myvar)$")
        assert result == r"$x^2$"


if __name__ == "__main__":
    pytest.main()
