"""
JSON Structure Validator — Lab 7

Validates the structural nesting of a JSON string using a Stack.
Reports the location (line, column) of any errors found.
"""

from stack import Stack


# Maps each closing character to its expected opening character.
MATCHING = {
    "}": "{",
    "]": "[",
}


def validate(json_string):
    """
    Validate the structural nesting of a JSON string.

    Checks that every { has a matching }, every [ has a matching ],
    and that quoted strings are properly closed.

    Args:
        json_string (str): The JSON text to validate.

    Returns:
        tuple: (is_valid, errors)
            - is_valid (bool): True if the structure is valid.
            - errors (list[str]): List of error message strings.
              Empty if valid.
    """
    """
    Implement the validate function in src/json_validator.py following the pseudocode above. For this first task, you may ignore string awareness (skip the in_string logic). Focus on:

    Pushing { and [ with their positions onto the stack.
    Popping and matching on } and ].
    Returning a clear result: valid, or a description of the first error found.
    Your function should return a result object or tuple that includes:

    Whether the JSON is valid (True/False).
    If invalid, an error message with the line number and column number.
    Run your validator against easy_correct.json and easy_broken.json.
    """
    """
    CREATE empty stack
    SET line = 1, col = 0

    # ── STATE FLAG ───────────────────────────────────────────────
    # in_string tracks whether we are currently inside a "quoted
    # string". While True, structural characters like { and [ are
    # just text content — they must be ignored by the validator.
    # This is the key insight that separates a real validator from
    # a naive parentheses checker.
    SET in_string = FALSE

    FOR each character in json_string:
        INCREMENT col

        IF character is newline:
            INCREMENT line, RESET col to 0
            CONTINUE                          # move to next character

        # ── STRING MODE ──────────────────────────────────────────
        # If we are inside a quoted string, the only characters
        # that matter are:
        #   backslash  → the next char is escaped, skip it
        #   double-quote → this ends the string
        # Everything else is just string content — skip it.

        IF in_string is TRUE:
            IF character is backslash:
                SKIP the next character        # it is escaped (e.g., \")
            ELSE IF character is double-quote:
                SET in_string = FALSE          # we are leaving the string
            CONTINUE                           # either way, move on

        # ── NORMAL MODE ──────────────────────────────────────────
        # We are outside any string. Structural characters matter.

        # Encountering a double-quote means we are entering a string.
        # From this point until the matching closing quote, we must
        # ignore all braces and brackets.
        IF character is double-quote:
            SET in_string = TRUE
            CONTINUE

        # Opening brace/bracket: push it onto the stack along with
        # its location. We store the location so that if this opener
        # is never closed, we can tell the user WHERE it was opened.
        IF character is '{' or '[':
            PUSH (character, line, col) onto stack

        # Closing brace/bracket: this is the core stack operation.
        # Pop the most recent opener and verify it matches this
        # closer. { must match }, [ must match ].
        ELSE IF character is '}' or ']':
            IF stack is empty:
                # Nothing to match against — this closer is unexpected.
                REPORT error: unexpected closer at (line, col)
                RETURN failure

            POP (open_char, open_line, open_col) from stack
            IF open_char does not match character:
                # The opener and closer don't pair up.
                REPORT error: expected matching closer for open_char
                    (opened at open_line, open_col)
                    but found character at (line, col)
                RETURN failure

    # ── AFTER ALL CHARACTERS ─────────────────────────────────────

    # If we reached the end while still inside a string, the last
    # opening quote was never closed.
    IF in_string is TRUE:
        REPORT error: unterminated string
        RETURN failure

    # If the stack still has items, those openers were never closed.
    # Report each one with the location where it was opened.
    IF stack is not empty:
        FOR each remaining item on stack:
            POP (open_char, open_line, open_col)
            REPORT error: unclosed open_char at (open_line, open_col)
        RETURN failure

    RETURN success                             # all matched correctly
    """
    return True


def validate_file(filepath):
    """
    Validate a JSON file by reading it and calling validate().

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        tuple: (is_valid, errors) — same as validate().
    """
    with open(filepath, "r") as f:
        content = f.read()
    return validate(content)


# ── Main ─────────────────────────────────────────────────────────
# You can use this to test your validator from the command line:
#   python src/json_validator.py tests/test_data/easy_correct.json

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python json_validator.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    is_valid, errors = validate_file(filepath)

    if is_valid:
        print(f"{filepath}: Valid JSON structure")
    else:
        for error in errors:
            print(error)