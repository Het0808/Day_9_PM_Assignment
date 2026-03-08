# 🤖 AI-Augmented Task — Jaccard Similarity

---

## 1️⃣ Exact Prompt Used

> *"Write a Python function that calculates the Jaccard similarity between
> two sets of strings. Explain what Jaccard similarity is and where it is
> used in industry."*

---

## 2️⃣ AI Output (Claude)

**What is Jaccard Similarity?**

Jaccard similarity measures the overlap between two sets.
It is defined as the size of the *intersection* divided by the size of the *union*:

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

The result is a float in the range **[0.0, 1.0]**:
- `1.0` → the sets are identical
- `0.0` → the sets share no elements
- Values in between represent partial overlap

**Python Function (AI-generated)**

```python
def jaccard_similarity(set_a: set, set_b: set) -> float:
    """
    Calculate Jaccard similarity between two sets of strings.

    Formula: |A ∩ B| / |A ∪ B|

    Returns 0.0 if both sets are empty (avoids ZeroDivisionError).
    """
    if not set_a and not set_b:
        return 0.0                        # edge case: both empty

    intersection = set_a & set_b         # set intersection
    union        = set_a | set_b         # set union

    return len(intersection) / len(union)
```

---

## 3️⃣ Testing the AI Output

```python
set_a = {'python', 'java', 'sql'}
set_b = {'python', 'sql', 'docker', 'aws'}

score = jaccard_similarity(set_a, set_b)
print(f"Jaccard similarity: {score:.4f}")
```

**Manual verification:**
```
Intersection: {'python', 'sql'}          → |A ∩ B| = 2
Union:        {'python','java','sql','docker','aws'}  → |A ∪ B| = 5

J = 2 / 5 = 0.4000  ✅
```

**Output:**
```
Jaccard similarity: 0.4000
```

---

## ✅ Formula Validation

| Check | Result |
|---|---|
| Formula matches definition `\|A∩B\| / \|A∪B\|` | ✅ Correct |
| Uses Python set operators `&` and `\|` | ✅ Correct |
| Returns float in [0, 1] | ✅ Correct |
| Handles both sets empty → returns 0.0 (not ZeroDivisionError) | ✅ Handled |
| One set empty, other non-empty → returns 0.0 (union = other set, intersection = ∅) | ✅ Correct (no special case needed) |
| Identical sets → returns 1.0 | ✅ Correct |
| Completely disjoint sets → returns 0.0 | ✅ Correct |

**Verdict:** The AI output is mathematically correct and handles all critical
edge cases. The only improvement worth adding for production use would be
type hints and input validation for non-set types.

---

## 🔬 Edge Case Test Results

```python
# Both empty
print(jaccard_similarity(set(), set()))           # → 0.0  ✅

# One empty
print(jaccard_similarity({'a'}, set()))            # → 0.0  ✅

# Identical sets
print(jaccard_similarity({'x','y'}, {'x','y'}))   # → 1.0  ✅

# No overlap
print(jaccard_similarity({'a','b'}, {'c','d'}))   # → 0.0  ✅

# Subset
print(jaccard_similarity({'a'}, {'a','b','c'}))   # → 0.333  ✅
```

---

## 🏭 Industry Applications of Jaccard Similarity

**Recommendation Systems:** Streaming platforms like Netflix and Spotify use
Jaccard similarity to compare users' watched or liked item sets, finding
"users like you" for collaborative filtering. A high Jaccard score between
two users' histories means their tastes overlap and their unseen items can be
cross-recommended.

**NLP & Document Similarity:** In natural language processing, documents are
converted to sets of n-grams or token shingles, then Jaccard is used to
detect near-duplicate web pages, measure sentence similarity, and power
search result deduplication — this underpins MinHash and LSH (Locality
Sensitive Hashing), which allow Jaccard comparisons at web scale.

**Plagiarism Detection:** Tools like Turnitin represent student submissions
as sets of word shingles and compute Jaccard similarity against a corpus of
known documents; a score above a threshold flags potential plagiarism for
human review.

**Bioinformatics & Data Deduplication:** Jaccard is widely used to compare
gene sets between biological samples, measure species overlap in ecological
studies, and deduplicate customer records or product listings in data
pipelines where exact-match is too strict.
