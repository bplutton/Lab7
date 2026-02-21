# Lab 8: Build Your Own Hash Table

## Overview

In this lab, you'll implement a hash table from scratch. Python's `dict` is a hash table under the hood — by building one yourself, you'll understand **how** it works, not just **that** it works. This is one of the most commonly asked topics in technical interviews.

**Time:** ~30 minutes
**File to edit:** `hash_table.py`
**Test command:** `pytest -v`

## Background

A **hash table** stores key-value pairs and provides fast (average O(1)) lookups. It works in three steps:

1. **Hash** the key → produces a number
2. **Modulo** that number by the table size → gives a bucket index
3. **Store** the key-value pair in that bucket

### What about collisions?

Two different keys can hash to the same bucket. This is called a **collision**. We handle it with **separate chaining** — each bucket is a list that can hold multiple pairs.

```
Bucket 0: [ ["apple", 5] ]
Bucket 1: [ ["banana", 3], ["grape", 8] ]    ← collision! two pairs in one bucket
Bucket 2: [ ]
Bucket 3: [ ["cherry", 2] ]
```

When we look up `"grape"`, we hash it → bucket 1 → then search the list for a matching key.

## Setup

```bash
# Clone / pull the cs417 repo
cd labs/Lab8
pytest -v       # All tests should FAIL initially
```

## Tasks

Open `hash_table.py` and complete the four `TODO` methods.

### Task 1: `_hash(self, key)` — The Hash Function

This is the foundation. Use Python's built-in `hash()` function and modulo `%` to convert any key into a valid bucket index.

**Hint:** You need exactly one line: combine `hash()`, `%`, and `self.size`.

**Test it:** `pytest -v -k "TestHashFunction"`

### Task 2: `put(self, key, value)` — Insert / Update

Steps:
1. Use `_hash()` to find the right bucket
2. Loop through the bucket to check if the key already exists
   - If it does → update the value
   - If it doesn't → append a new `[key, value]` pair
3. Only increment `self.count` when adding a **new** key (not updating)

**Think about:** Why do we check for existing keys? What would happen if we just always appended?

**Test it:** `pytest -v -k "TestPutAndGet"`

### Task 3: `get(self, key)` — Look Up a Value

Steps:
1. Use `_hash()` to find the right bucket
2. Loop through the bucket to find the matching key
3. Return the value if found
4. Raise `KeyError(key)` if not found

**Pattern:** This is very similar to `put` — find the bucket, search for the key.

**Test it:** `pytest -v -k "TestPutAndGet"`

### Task 4: `delete(self, key)` — Remove a Pair

Steps:
1. Use `_hash()` to find the right bucket
2. Loop through the bucket with `enumerate()` to get the index
3. If you find the key, use `del` or `.pop()` to remove it, then decrement `self.count`
4. If the key isn't found, raise `KeyError(key)`

**Hint:** `enumerate()` gives you both the position and the pair: `for i, pair in enumerate(bucket):`

**Test it:** `pytest -v -k "TestDelete"`

## Checking Your Work

Run all tests:
```bash
pytest -v
```

You should see all tests pass. The test file also checks:
- That collisions are handled correctly (tiny 2-bucket table)
- That `in` works (`"key" in hash_table`)
- That `load_factor()` computes correctly (it uses your `put` and `count`)

## Key Concepts to Take Away

| Concept | What it means |
|---------|--------------|
| **Hash function** | Converts a key into a bucket index |
| **Collision** | Two keys mapping to the same bucket |
| **Separate chaining** | Each bucket holds a list of pairs |
| **Load factor** | `items / buckets` — higher means more collisions |
| **Average O(1)** | Lookups are constant time *on average*, but O(n) worst case if everything collides |

## Submission

Push your completed code to your GitHub repo and submit the repo URL.

```bash
git add -A
git commit -m "Lab 8: Hash Table implementation"
git push
```
