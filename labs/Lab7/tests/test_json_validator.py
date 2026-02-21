"""
Tests for JSON Structure Validator — Lab 7.
Do not modify this file.

Run from the labs/Lab7 directory:
    pytest -v
"""

import os
import sys

# Add src/ to the path so we can import the validator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from json_validator import validate, validate_file

# ── Path to test data files ──────────────────────────────────────
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


def data_path(filename):
    return os.path.join(TEST_DATA_DIR, filename)


# ═══════════════════════════════════════════════════════════════════
# Task 1 Tests: Basic Nesting
# ═══════════════════════════════════════════════════════════════════


class TestBasicValid:
    """Tests for correctly nested JSON (no string tricks)."""

    def test_easy_correct_file(self):
        is_valid, errors = validate_file(data_path("easy_correct.json"))
        assert is_valid is True
        assert errors == []

    def test_empty_object(self):
        is_valid, errors = validate("{}")
        assert is_valid is True

    def test_empty_array(self):
        is_valid, errors = validate("[]")
        assert is_valid is True

    def test_nested_objects(self):
        is_valid, errors = validate('{"a": {"b": {"c": 1}}}')
        assert is_valid is True

    def test_nested_arrays(self):
        is_valid, errors = validate("[[1, 2], [3, 4]]")
        assert is_valid is True

    def test_mixed_nesting(self):
        is_valid, errors = validate('{"list": [1, {"key": [2, 3]}]}')
        assert is_valid is True


class TestBasicBroken:
    """Tests for structurally broken JSON (no string tricks)."""

    def test_easy_broken_file(self):
        is_valid, errors = validate_file(data_path("easy_broken.json"))
        assert is_valid is False
        assert len(errors) > 0

    def test_missing_closing_brace(self):
        is_valid, errors = validate('{"key": "value"')
        assert is_valid is False
        assert len(errors) > 0

    def test_missing_closing_bracket(self):
        is_valid, errors = validate("[1, 2, 3")
        assert is_valid is False
        assert len(errors) > 0

    def test_mismatched_brace_bracket(self):
        is_valid, errors = validate('{"key": [1, 2}')
        assert is_valid is False
        assert len(errors) > 0

    def test_extra_closing_brace(self):
        is_valid, errors = validate('{"key": 1}}')
        assert is_valid is False
        assert len(errors) > 0

    def test_extra_closing_bracket(self):
        is_valid, errors = validate("[1, 2]]")
        assert is_valid is False
        assert len(errors) > 0

    def test_unexpected_closer_on_empty_stack(self):
        is_valid, errors = validate("}")
        assert is_valid is False
        assert len(errors) > 0


# ═══════════════════════════════════════════════════════════════════
# Task 2 Tests: String Awareness
# ═══════════════════════════════════════════════════════════════════


class TestStringAwareness:
    """Tests that structural chars inside strings are ignored."""

    def test_medium_correct_file(self):
        is_valid, errors = validate_file(data_path("medium_correct.json"))
        assert is_valid is True
        assert errors == []

    def test_medium_broken_file(self):
        is_valid, errors = validate_file(data_path("medium_broken.json"))
        assert is_valid is False
        assert len(errors) > 0

    def test_braces_inside_string(self):
        is_valid, errors = validate('{"key": "value with {braces}"}')
        assert is_valid is True

    def test_brackets_inside_string(self):
        is_valid, errors = validate('{"key": "value with [brackets]"}')
        assert is_valid is True

    def test_mixed_structural_in_string(self):
        is_valid, errors = validate('{"msg": "use {id} and [0]"}')
        assert is_valid is True

    def test_escaped_quote_in_string(self):
        is_valid, errors = validate('{"key": "say \\"hello\\""}')
        assert is_valid is True

    def test_escaped_quote_does_not_end_string(self):
        # The escaped quote should NOT close the string,
        # so the { inside should be treated as string content.
        is_valid, errors = validate('{"key": "a\\"b{c"}')
        assert is_valid is True

    def test_unterminated_string(self):
        is_valid, errors = validate('{"key": "no closing quote}')
        assert is_valid is False
        assert len(errors) > 0


# ═══════════════════════════════════════════════════════════════════
# Task 3 Tests: Error Reporting Quality
# ═══════════════════════════════════════════════════════════════════


class TestErrorReporting:
    """Tests that error messages include useful location info."""

    def test_mismatch_includes_line_col(self):
        json_str = '{\n  "a": [\n    1\n  }\n}'
        is_valid, errors = validate(json_str)
        assert is_valid is False
        # Error should mention both the closer location and the opener location
        error_msg = errors[0].lower()
        assert "line" in error_msg
        assert "col" in error_msg

    def test_unclosed_opener_includes_location(self):
        json_str = '{\n  "a": [\n    1\n'
        is_valid, errors = validate(json_str)
        assert is_valid is False
        # Should report at least one unclosed opener with location
        assert len(errors) >= 1
        error_msg = errors[0].lower()
        assert "line" in error_msg

    def test_unexpected_closer_includes_location(self):
        json_str = '  ]\n'
        is_valid, errors = validate(json_str)
        assert is_valid is False
        error_msg = errors[0].lower()
        assert "line" in error_msg
        assert "col" in error_msg

    def test_multiple_unclosed_reports_all(self):
        json_str = '{['
        is_valid, errors = validate(json_str)
        assert is_valid is False
        # Should report both unclosed openers
        assert len(errors) == 2
