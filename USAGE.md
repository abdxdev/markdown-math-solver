# KaTeX Python Solver - User Guide

## What is this?

A tool that **processes Python code embedded in LaTeX math blocks** in Markdown files. Define expressions, bind parameters, evaluate math, and generate computed results.

## Quick Start

### 1. Install dependencies

```bash
pip install sympy antlr4-python3-runtime==4.11
```

### 2. Run the tool

```bash
python katex-py-solver.py yourfile.md
```

### 3. Check output

Your results will be in `yourfile.output.md`

## The Golden Rule

> **Only `py(...)` blocks inside `$...$` or `$$...$$` get processed.**  
> Everything else stays exactly as you wrote it.

```markdown
$1 + 1$ ← IGNORED (no py())
$1 + 1 py(myVar = THIS)$ ← PROCESSED (has py())
```

**Important:** There must be a **space before `py(`**. These are INVALID:

```markdown
$100py(...)$ ← INVALID (no space)
$param(x)py(...)$ ← INVALID (no space)
```

## Syntax Overview

| Syntax                   | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `expr py(name = THIS)`   | Store the expression before `py()` as `name`     |
| `param(var)`             | Parameter placeholder in expressions             |
| `py(ReplaceThis(value))` | Replace the `py(...)` with `value`               |
| `py(ReplaceAll(value))`  | Replace the entire `$...$` block with `value`    |
| `name.bind(var=value)`   | Bind parameters to expression                    |
| `name.unbind()`          | Reset to original with all `param(var)` restored |
| `name.unbind('a', 'b')`  | Selectively unbind only specified variables      |
| `name(var=value)`        | Bind and evaluate                                |
| `name()`                 | Evaluate expression                              |
| `str(name)`              | Get LaTeX string of expression                   |
| `THIS`                   | Reference to LaTeX before `py()` in same block   |

## Basic Operations

### 📝 Define an Expression

Store a LaTeX expression for later use:

```markdown
$5 + 3 py(mySum = THIS)$
$\frac{1}{2} py(half = THIS)$
```

**Output:**

```markdown
$5 + 3$
$\frac{1}{2}$
```

The `py(...)` is removed, expressions are stored in `mySum` and `half`.

### 🔢 Evaluate an Expression

Use `ReplaceThis()` to output a computed value:

```markdown
$py(ReplaceThis(mySum()))$
$py(ReplaceThis(half()))$
```

**Output:**

```markdown
$8$
$0.5$
```

### 📖 Show a Stored Expression

Use `str()` to get the LaTeX string:

```markdown
$py(ReplaceThis(str(mySum)))$
```

**Output:**

```markdown
$5 + 3$
```

### 🔄 Replace Entire Block

Use `ReplaceAll()` to replace the whole `$...$`:

```markdown
$py(ReplaceAll(str(mySum) + ' = ' + str(mySum())))$
```

**Output:**

```markdown
$5 + 3 = 8$
```

## Parameters with `param(var)`

### Define Expression with Parameters

Use `param(varname)` as placeholders:

```markdown
$\frac{param(a)}{param(b)} py(ratio = THIS)$
```

**Output:**

```markdown
$\frac{param(a)}{param(b)}$
```

### Bind Parameters

Use `.bind()` to substitute values:

```markdown
$py(ReplaceThis(str(ratio.bind(a=3, b=4))))$
```

**Output:**

```markdown
$\frac{3}{4}$
```

### Bind and Evaluate

Call with parameters to bind and evaluate in one step:

```markdown
$py(ReplaceThis(ratio(a=3, b=4)))$
```

**Output:**

```markdown
$0.75$
```

### Unbind Parameters

Use `.unbind()` to reset a bound expression back to its original form with all `param(var)` placeholders:

```markdown
$\frac{param(a)}{param(b)} py(expr = THIS)$
$py(bound = expr.bind(a=3, b=4); ReplaceThis(str(bound)))$
$py(ReplaceThis(str(bound.unbind())))$
```

**Output:**

```markdown
$\frac{param(a)}{param(b)}$
$\frac{3}{4}$
$\frac{param(a)}{param(b)}$
```

#### Selective Unbind

Pass variable names to unbind only specific parameters:

```markdown
$param(x) + param(y) + param(z) py(expr = THIS)$
$py(bound = expr.bind(x=1, y=2, z=3); ReplaceThis(str(bound)))$
$py(ReplaceThis(str(bound.unbind('x', 'z'))))$
```

**Output:**

```markdown
$param(x) + param(y) + param(z)$
$1 + 2 + 3$
$param(x) + 2 + param(z)$
```

This is useful when you want to reuse an expression with different parameter values after having bound some.

## Advanced: Chaining Operations

### Multiple Statements

Separate statements with `;`:

```markdown
$py(x = ratio.bind(a=1, b=2); ReplaceThis(str(x)))$
```

### Inline Multiple py() Blocks

```markdown
$py(ReplaceThis('A')) and py(ReplaceThis('B'))$
```

**Output:**

```markdown
$A and B$
```

### Full Computation Example

```markdown
$\frac{param(a)}{param(b)} + \frac{param(c)}{param(d)} py(expr = THIS)$
$py(ReplaceAll(str(expr.bind(a=1, b=2, c=1, d=3)) + ' = ' + str(expr(a=1, b=2, c=1, d=3))))$
```

**Output:**

```markdown
$\frac{param(a)}{param(b)} + \frac{param(c)}{param(d)}$
$\frac{1}{2} + \frac{1}{3} = 0.833333$
```

## Special Cases

### Empty Results Delete Block

If `ReplaceAll('')` or result is empty, the block is deleted:

```markdown
Before $py(ReplaceAll(''))$ After
```

**Output:**

```markdown
Before After
```

### Silent Assignment

Assignment without `ReplaceThis`/`ReplaceAll` just removes `py()`:

```markdown
$100 py(val = THIS)$
```

**Output:**

```markdown
$100$
```

### \text{} Handling

`\text{...}` is stripped before evaluation:

```markdown
$\text{Result: }5 + 3 py(labeled = THIS)$
$py(ReplaceThis(labeled()))$
```

**Output:**

```markdown
$\text{Result: }5 + 3$
$8$
```

## Python Builtins

All Python builtins are available:

```markdown
$py(ReplaceThis(str(abs(-5))))$
$py(ReplaceThis(str(max(1, 5, 3))))$
$py(ReplaceThis(str(round(3.14159, 2))))$
```

**Output:**

```markdown
$5$
$5$
$3.14$
```

## Complete Example: Entropy Calculation

```markdown
# Define entropy formula with parameters

$$-\frac{param(a)}{param(b)}\log_2\left(\frac{param(a)}{param(b)}\right) py(entropy = THIS)$$

# Use it with different values

$py(ReplaceThis(str(entropy.bind(a=5, b=14))))$ evaluates to $py(ReplaceThis(entropy(a=5, b=14)))$
```

**Output:**

```markdown
$$-\frac{param(a)}{param(b)}\log_2\left(\frac{param(a)}{param(b)}\right)$$

$-\frac{5}{14}\log_2\left(\frac{5}{14}\right)$ evaluates to $0.53051$
```

## Quick Reference

| Want to...         | Use...                                              |
| ------------------ | --------------------------------------------------- |
| Store expression   | `$expr py(name = THIS)$`                            |
| Show stored LaTeX  | `$py(ReplaceThis(str(name)))$`                      |
| Evaluate stored    | `$py(ReplaceThis(name()))$`                         |
| Show = result      | `$py(ReplaceAll(str(name) + ' = ' + str(name())))$` |
| Define with params | `$\frac{param(a)}{param(b)} py(f = THIS)$`          |
| Bind params        | `$py(ReplaceThis(str(f.bind(a=1, b=2))))$`          |
| Bind & evaluate    | `$py(ReplaceThis(f(a=1, b=2)))$`                    |
