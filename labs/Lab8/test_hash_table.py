"""
Tests for Hash Table — Lab 8.
Do not modify this file.

Run from the labs/Lab8 directory:
    pytest -v
"""

from hash_table import HashTable


# ═══════════════════════════════════════════════════════════════════
# Task 1 Tests: Hash Function
# ═══════════════════════════════════════════════════════════════════


class TestHashFunction:
    """Tests that _hash returns valid bucket indices."""

    def test_returns_int(self):
        ht = HashTable(size=10)
        assert isinstance(ht._hash("hello"), int)

    def test_within_range(self):
        ht = HashTable(size=10)
        for key in ["apple", "banana", "cherry", 42, 99, "z"]:
            idx = ht._hash(key)
            assert 0 <= idx < 10, f"_hash({key!r}) returned {idx}, expected 0-9"

    def test_within_range_small_table(self):
        ht = HashTable(size=3)
        for key in ["a", "b", "c", "d", "e"]:
            idx = ht._hash(key)
            assert 0 <= idx < 3, f"_hash({key!r}) returned {idx}, expected 0-2"

    def test_consistent(self):
        ht = HashTable(size=10)
        assert ht._hash("test") == ht._hash("test")

    def test_different_keys_can_differ(self):
        """Different keys should (usually) hash differently."""
        ht = HashTable(size=100)
        indices = {ht._hash(f"key_{i}") for i in range(20)}
        # With 100 buckets and 20 keys, we expect at least a few different indices
        assert len(indices) > 1


# ═══════════════════════════════════════════════════════════════════
# Task 2 Tests: Put and Get
# ═══════════════════════════════════════════════════════════════════


class TestPutAndGet:
    """Tests for inserting and retrieving key-value pairs."""

    def test_put_and_get_one(self):
        ht = HashTable()
        ht.put("name", "Alice")
        assert ht.get("name") == "Alice"

    def test_put_and_get_multiple(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("b", 2)
        ht.put("c", 3)
        assert ht.get("a") == 1
        assert ht.get("b") == 2
        assert ht.get("c") == 3

    def test_put_updates_existing_key(self):
        ht = HashTable()
        ht.put("color", "red")
        ht.put("color", "blue")
        assert ht.get("color") == "blue"

    def test_get_missing_key_raises(self):
        ht = HashTable()
        ht.put("x", 10)
        try:
            ht.get("y")
            assert False, "Expected KeyError"
        except KeyError:
            pass

    def test_integer_keys(self):
        ht = HashTable()
        ht.put(1, "one")
        ht.put(2, "two")
        assert ht.get(1) == "one"
        assert ht.get(2) == "two"

    def test_count_increases(self):
        ht = HashTable()
        assert len(ht) == 0
        ht.put("a", 1)
        assert len(ht) == 1
        ht.put("b", 2)
        assert len(ht) == 2

    def test_count_no_increase_on_update(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("a", 2)
        assert len(ht) == 1

    def test_collision_handling(self):
        """Force collisions with a tiny table and verify all keys work."""
        ht = HashTable(size=2)  # Only 2 buckets — guaranteed collisions
        ht.put("apple", 1)
        ht.put("banana", 2)
        ht.put("cherry", 3)
        ht.put("date", 4)
        assert ht.get("apple") == 1
        assert ht.get("banana") == 2
        assert ht.get("cherry") == 3
        assert ht.get("date") == 4


# ═══════════════════════════════════════════════════════════════════
# Task 3 Tests: Delete
# ═══════════════════════════════════════════════════════════════════


class TestDelete:
    """Tests for removing key-value pairs."""

    def test_delete_existing(self):
        ht = HashTable()
        ht.put("x", 10)
        ht.delete("x")
        assert "x" not in ht

    def test_delete_decrements_count(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("b", 2)
        assert len(ht) == 2
        ht.delete("a")
        assert len(ht) == 1

    def test_delete_missing_key_raises(self):
        ht = HashTable()
        try:
            ht.delete("ghost")
            assert False, "Expected KeyError"
        except KeyError:
            pass

    def test_delete_does_not_affect_other_keys(self):
        ht = HashTable(size=2)  # Small table to force collisions
        ht.put("a", 1)
        ht.put("b", 2)
        ht.put("c", 3)
        ht.delete("b")
        assert ht.get("a") == 1
        assert ht.get("c") == 3
        assert "b" not in ht

    def test_put_after_delete(self):
        ht = HashTable()
        ht.put("key", "first")
        ht.delete("key")
        ht.put("key", "second")
        assert ht.get("key") == "second"


# ═══════════════════════════════════════════════════════════════════
# Task 4 Tests: Contains and Load Factor
# ═══════════════════════════════════════════════════════════════════


class TestContainsAndLoadFactor:
    """Tests for __contains__ and load_factor (these use your implementations)."""

    def test_contains_true(self):
        ht = HashTable()
        ht.put("hello", "world")
        assert "hello" in ht

    def test_contains_false(self):
        ht = HashTable()
        assert "missing" not in ht

    def test_load_factor_empty(self):
        ht = HashTable(size=10)
        assert ht.load_factor() == 0.0

    def test_load_factor_half(self):
        ht = HashTable(size=10)
        for i in range(5):
            ht.put(f"key_{i}", i)
        assert ht.load_factor() == 0.5

    def test_load_factor_over_one(self):
        """Load factor > 1.0 means more items than buckets (many collisions)."""
        ht = HashTable(size=3)
        for i in range(6):
            ht.put(f"key_{i}", i)
        assert ht.load_factor() == 2.0
