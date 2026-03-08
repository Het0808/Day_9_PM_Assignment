# 💼 Interview Answers — Tuples, Sets & Python Internals

---

## Q1 — Tuple Immutability Trap

### The Code
```python
t = ([1, 2], [3, 4])
t[0][0] = 99
```

### Does it work?
**Yes — it works without raising any error.**

After execution, `t` becomes `([99, 2], [3, 4])`.

---

### Why it works (and what it reveals)

A tuple is immutable, but **immutability in Python means the tuple's
*references* cannot be changed — not the objects those references point to.**

Internally, `t` stores two memory addresses (pointers):

```
t[0]  →  points to list object  [1, 2]
t[1]  →  points to list object  [3, 4]
```

`t[0][0] = 99` does **not** touch the tuple at all.
It navigates *through* the tuple's first reference to the list it points
to, and mutates *that list* in-place. The tuple's own pointers never change.

What **would** raise a `TypeError` is:
```python
t[0] = [99, 2]   # ❌ TypeError: 'tuple' object does not support item assignment
```
Because now you're trying to swap the pointer stored inside the tuple itself.

---

### The Core Insight

> **Tuple immutability is *shallow*, not deep.**
> The tuple protects its own structure (which slots point where),
> but has no control over what the objects at those addresses do internally.

This is a fundamental Python interview trap. The lesson generalises:
- A `tuple` of lists is **not** safely immutable for use as a dict key or set element
- Only a `tuple` of fully hashable, truly immutable objects (ints, strings, other tuples) can be hashed
- `hash(([1,2], [3,4]))` raises `TypeError` for exactly this reason

---

## Q2 — Duplicate Detection (O(n), set operations only)

### Function

```python
def find_duplicates(lst: list) -> set:
    """
    Return a set of elements that appear more than once in lst.
    Uses only set operations — no Counter, no nested loops.
    Time complexity: O(n)  |  Space complexity: O(n)
    """
    seen    = set()   # elements encountered at least once
    dupes   = set()   # elements encountered more than once

    for item in lst:
        if item in seen:      # O(1) average — hash lookup
            dupes.add(item)
        else:
            seen.add(item)

    return dupes
```

### How it achieves O(n)

- Single pass through the list → **O(n)** iterations
- Both `in` (membership test) and `.add()` on a set are **O(1)** average
- Total: **O(n)** time, **O(n)** space for the two sets

### Tests

```python
print(find_duplicates([1, 2, 3, 2, 4, 1]))   # → {1, 2}
print(find_duplicates(["a", "b", "a", "c"]))  # → {'a'}
print(find_duplicates([1, 2, 3]))             # → set()  (no duplicates)
print(find_duplicates([]))                    # → set()  (empty list)
print(find_duplicates([5, 5, 5, 5]))          # → {5}
```

---

## Q3 — Debug Problem

### Buggy Code
```python
def unique_to_each(a, b):
    result = set(a) - set(b)
    return list(result)
```

### Test
```python
unique_to_each([1, 2, 3], [3, 4, 5])
```

| | Expected | Actual (buggy) |
|---|---|---|
| Result | `[1, 2, 4, 5]` | `[1, 2]` |

---

### Why the Bug Occurs

`set(a) - set(b)` computes the **left difference only** —
elements in `a` that are not in `b`.

```
{1, 2, 3} - {3, 4, 5}  =  {1, 2}   ← only items from 'a' missing in 'b'
```

It completely **ignores elements that are in `b` but not in `a`** (i.e., `4` and `5`).

The correct operation is the **symmetric difference** (`^`), which returns
elements that are in *either* set but **not in both**.

```
{1, 2, 3} ^ {3, 4, 5}  =  {1, 2, 4, 5}   ✅
```

---

### Fixed Function

```python
def unique_to_each(a: list, b: list) -> list:
    """
    Returns elements that are unique to each list —
    i.e., appear in one list but not the other.
    Uses symmetric difference (^).
    """
    return list(set(a) ^ set(b))
```

### Verification

```python
print(unique_to_each([1, 2, 3], [3, 4, 5]))   # → [1, 2, 4, 5]  ✅
print(unique_to_each([1, 2], [1, 2]))           # → []            ✅ (identical lists)
print(unique_to_each([], [1, 2]))               # → [1, 2]        ✅ (one empty)
print(unique_to_each([1, 1, 2], [2, 3]))        # → [1, 3]        ✅ (handles dupes)
```

> **Set operations quick reference:**
> - `A - B`  → Left difference (only what A has that B doesn't)
> - `B - A`  → Right difference (only what B has that A doesn't)
> - `A ^ B`  → Symmetric difference (unique to *either* — equivalent to `(A-B) | (B-A)`)
> - `A & B`  → Intersection (in both)
> - `A | B`  → Union (in either)
