# FAQ

**Why can't I write `x = 5`?**
Typy requires a name to be declared before it is assigned: `int x = 5` (or
`dyn x = 5` for anything-goes). After that, `x = 6` is fine.

**How do I write a method? `self` has no type.**
Every parameter needs one; use `dyn self` (or `dyn cls`).

**Can I still call Python's `any()`?**
Yes. Reserved words cannot be *defined*, but they can be referenced.

**Can I use `_` as a throwaway name?**
Yes. Only `__` (two underscores) is reserved, because `repeat` uses it.

**Why is `bool` not accepted where I declared `int`?**
Typy's types are exact. `True` is a `bool`, and `bool` is not `int` here, even
though Python considers it a subclass.

**Does `int x = some_function()` get checked?**
Not at compile time: Typy never guesses what an arbitrary expression returns.
With `--enforce` it is checked when the program runs.

**My standalone build can't open its data files.**
Inside a `.pyz` archive files are not on disk. Read them with
`importlib.resources` or `pkgutil.get_data`.

**Optional chaining inside an f-string fails.**
That needs Python 3.12 or newer, where f-string contents are tokenized as code.

**Where do the usage stats live? Can I move them?**
In `Typy/stats/`. Set `TYPY_STATS_DIR` to put them elsewhere; `typy stats
--reset` zeroes the counters.

**Can a Python 3.12 `type X = ...` alias be used?**
No: `TYPE name = value` is a typed declaration in Typy, so `type X = int`
declares a variable `X` of type `type`, which is what it looks like.
