"""Core solver logic for Markdown Math Solver."""

import re
from sympy.parsing.latex import parse_latex
from sympy import Symbol, solve

store = {}


class Expr:
    """Wrapper for LaTeX expressions with bind/call support"""

    def __init__(self, latex, original=None, bindings=None):
        self.latex = latex
        self._original = original if original is not None else latex
        self._bindings = bindings if bindings is not None else {}

    def __str__(self):
        return self.latex

    def __repr__(self):
        return self.latex

    def __add__(self, other):
        return self.latex + str(other)

    def __radd__(self, other):
        return str(other) + self.latex

    def bind(self, **kwargs):
        result = self.latex
        new_bindings = dict(self._bindings)
        for k, v in kwargs.items():
            # Replace param(var) with value
            result = result.replace(f"param({k})", str(v))
            new_bindings[k] = v
        # Update self in place so THIS() uses bound values
        self.latex = result
        self._bindings = new_bindings
        return self

    def unbind(self, *args):
        """Return expression with param(var) placeholders restored.
        
        If no args: restore all placeholders (full unbind).
        If args provided: only restore those specific variables.
        """
        if not args:
            # Full unbind - restore original
            return Expr(self._original)
        
        # Partial unbind - only restore specified variables
        result = self.latex
        new_bindings = dict(self._bindings)
        for var in args:
            if var in self._bindings:
                # Replace the bound value back with param(var)
                result = result.replace(str(self._bindings[var]), f"param({var})")
                del new_bindings[var]
        return Expr(result, self._original, new_bindings)

    def __call__(self, **kwargs):
        # If kwargs given, bind first
        expr = self.bind(**kwargs) if kwargs else self
        clean = expr.latex
        # Remove \text{...} for evaluation
        while "\\text{" in clean:
            start = clean.find("\\text{")
            depth, end = 1, start + 6
            while depth > 0 and end < len(clean):
                if clean[end] == "{":
                    depth += 1
                elif clean[end] == "}":
                    depth -= 1
                end += 1
            clean = clean[:start] + clean[end:]
        # Replace unbound param(var) with just var (as a symbol)
        clean = re.sub(r"param\((\w+)\)", r"\1", clean)
        # Find last = and take everything after
        eq_idx = clean.rfind("=")
        if eq_idx != -1:
            clean = clean[eq_idx + 1 :]
        clean = clean.strip()
        if not clean:
            return 0
        try:
            return parse_latex(clean).evalf()
        except:
            return clean

    def solve(self, var_name):
        clean = self.latex
        eq_idx = clean.rfind("=")
        if eq_idx != -1:
            clean = clean[eq_idx + 1 :]
        try:
            var = Symbol(var_name)
            sols = solve(parse_latex(clean.strip()), var)
            return f"{var_name} = " + ", ".join(str(s) for s in sols)
        except Exception as e:
            return f"[Error: {e}]"


class ReplaceThis:
    """Marker to replace just py(...) with value"""

    def __init__(self, value):
        self.value = str(value)


class ReplaceAll:
    """Marker to replace entire block with value"""

    def __init__(self, value):
        self.value = str(value)


class _NoOutput:
    """Sentinel for assignments - no output"""

    pass


NoOutput = _NoOutput()


def find_matching_paren(s, start):
    """Find matching ) for ( at start position"""
    depth = 1
    i = start + 1
    in_string = None
    while i < len(s) and depth > 0:
        c = s[i]
        if in_string:
            if c == in_string and s[i - 1] != "\\":
                in_string = None
        else:
            if c in "\"'":
                in_string = c
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
        i += 1
    return i - 1 if depth == 0 else -1


def find_py_block(s, start=0):
    """Find next py(...) block, returns (start, end, content) or None"""
    idx = start
    while idx < len(s):
        pos = s.find("py(", idx)
        if pos == -1:
            return None
        # py( must be at start OR preceded by space/newline/special char
        # NOT allowed: param(x)py(, 100py(, wordpy(
        if pos > 0 and (s[pos - 1].isalnum() or s[pos - 1] == "_" or s[pos - 1] == ":"):
            idx = pos + 1
            continue
        paren_start = pos + 2
        paren_end = find_matching_paren(s, paren_start)
        if paren_end == -1:
            idx = pos + 1
            continue
        content = s[paren_start + 1 : paren_end]
        return (pos, paren_end + 1, content)
    return None


def get_latex_before(block_content, py_start):
    """Get LaTeX content before py(...) in the block"""
    before = block_content[:py_start].strip()
    return before


def get_latex_after(block_content, py_end):
    """Get LaTeX content after py(...) in the block"""
    after = block_content[py_end:].strip()
    # Remove any subsequent py(...) blocks for clean latex
    while "py(" in after:
        pb = find_py_block(after)
        if pb:
            after = after[: pb[0]] + after[pb[1] :]
        else:
            break
    return after.strip()


def get_this_latex(block_content, py_start, py_end):
    """Get THIS latex - before py() if exists, otherwise after"""
    before = get_latex_before(block_content, py_start)
    if before:
        return before
    return get_latex_after(block_content, py_end)


def execute_py(code, this_expr):
    """Execute Python code with THIS bound to this_expr"""
    THIS = Expr(this_expr) if this_expr else Expr("")

    local_vars = {
        "THIS": THIS,
        "ReplaceThis": ReplaceThis,
        "ReplaceAll": ReplaceAll,
    }
    # Add stored expressions
    for k, v in store.items():
        local_vars[k] = v

    result = None
    # Split by ; and execute each statement
    statements = []
    current = ""
    depth = 0
    in_string = None

    for c in code:
        if in_string:
            current += c
            if c == in_string and (len(current) < 2 or current[-2] != "\\"):
                in_string = None
        elif c in "\"'":
            in_string = c
            current += c
        elif c == "(":
            depth += 1
            current += c
        elif c == ")":
            depth -= 1
            current += c
        elif c == ";" and depth == 0:
            statements.append(current.strip())
            current = ""
        else:
            current += c

    if current.strip():
        statements.append(current.strip())

    for stmt in statements:
        stmt = stmt.strip()
        if not stmt:
            continue

        # Check for assignment: name = value
        eq_pos = -1
        depth = 0
        in_str = None
        for i, c in enumerate(stmt):
            if in_str:
                if c == in_str and (i == 0 or stmt[i - 1] != "\\"):
                    in_str = None
            elif c in "\"'":
                in_str = c
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == "=" and depth == 0 and i > 0 and stmt[i - 1] != "!" and stmt[i - 1] != "=" and stmt[i - 1] != "<" and stmt[i - 1] != ">":
                if i + 1 < len(stmt) and stmt[i + 1] == "=":
                    continue
                eq_pos = i
                break

        if eq_pos > 0:
            name = stmt[:eq_pos].strip()
            value_code = stmt[eq_pos + 1 :].strip()

            if name.isidentifier():
                try:
                    value = eval(value_code, {"__builtins__": __builtins__}, local_vars)
                    local_vars[name] = value
                    store[name] = value
                    result = NoOutput  # Assignment - no output
                except Exception as e:
                    result = f"[Error: {e}]"
                continue

        # Just evaluate
        try:
            result = eval(stmt, {"__builtins__": __builtins__}, local_vars)
        except Exception as e:
            result = f"[Error: {e}]"

    return result


def process_block(content):
    """Process a $...$ block"""
    if "py(" not in content:
        return None

    result = content
    offset = 0
    replace_all_value = None

    while True:
        block = find_py_block(result, offset)
        if not block:
            break

        py_start, py_end, py_code = block
        this_latex = get_this_latex(result, py_start, py_end)

        py_result = execute_py(py_code, this_latex)

        if isinstance(py_result, ReplaceAll):
            replace_all_value = py_result.value
            # Remove py(...) but keep processing
            result = result[:py_start] + result[py_end:]
            # Don't change offset since we removed content
        elif isinstance(py_result, ReplaceThis):
            result = result[:py_start] + py_result.value + result[py_end:]
            offset = py_start + len(py_result.value)
        elif isinstance(py_result, _NoOutput):
            # Assignment - just remove py(...)
            result = result[:py_start] + result[py_end:]
        elif py_result is None:
            # None result - just remove py(...)
            result = result[:py_start] + result[py_end:]
        else:
            # Implicit output (like Jupyter) - replace py(...) with string value
            output = str(py_result)
            result = result[:py_start] + output + result[py_end:]
            offset = py_start + len(output)

    if replace_all_value is not None:
        # If ReplaceAll gives empty string, return special marker
        if not replace_all_value.strip():
            return "__DELETE__"
        return replace_all_value

    # If result is empty after processing, mark for deletion
    if not result.strip():
        return "__DELETE__"

    return result.strip() if result.strip() != content.strip() else None


def process_markdown(text):
    """Process entire markdown file"""
    result = []
    i = 0

    while i < len(text):
        # Check for $$ (display math)
        if text[i : i + 2] == "$$":
            end = text.find("$$", i + 2)
            if end == -1:
                result.append(text[i:])
                break
            content = text[i + 2 : end]
            processed = process_block(content)
            if processed == "__DELETE__":
                pass  # Delete the block entirely
            elif processed is not None:
                result.append("$$" + processed + "$$")
            else:
                result.append(text[i : end + 2])
            i = end + 2
        # Check for $ (inline math)
        elif text[i] == "$":
            end = text.find("$", i + 1)
            if end == -1:
                result.append(text[i:])
                break
            content = text[i + 1 : end]
            processed = process_block(content)
            if processed == "__DELETE__":
                pass  # Delete the block entirely
            elif processed is not None:
                result.append("$" + processed + "$")
            else:
                result.append(text[i : end + 1])
            i = end + 1
        else:
            result.append(text[i])
            i += 1

    return "".join(result)


def fmt(v):
    """Format number nicely"""
    try:
        f = float(v)
        if f == int(f):
            return str(int(f))
        # Round to reasonable precision
        return f"{f:.6f}".rstrip("0").rstrip(".")
    except:
        return str(v)


# Patch Expr.__call__ to use fmt
_orig_call = Expr.__call__


def _new_call(self, **kwargs):
    result = _orig_call(self, **kwargs)
    try:
        return fmt(result)
    except:
        return result


Expr.__call__ = _new_call
