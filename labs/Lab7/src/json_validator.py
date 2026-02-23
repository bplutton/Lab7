"""
JSON Structure Validator — Lab 7

Validates the structural nesting of a JSON string using a Stack.
Reports the location (line, column) of any errors found.
"""

from inspect import stack

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
    Extend your validator to handle quoted strings:

    Track whether the scanner is currently inside a double-quoted string.
    While inside a string, ignore all structural characters ({, }, [, ]).
    Handle the escape sequence \" so that an escaped quote does not toggle the flag.
    This is what prevents a value like "ports: [80, 443]" from being misinterpreted as containing a real array.

    Run your validator against medium_correct.json and medium_broken.json.
        

        

        

    # ── AFTER ALL CHARACTERS ─────────────────────────────────────

    # If we reached the end while still inside a string, the last
    # opening quote was never closed.
    IF in_string is TRUE:
        REPORT error: unterminated string
        RETURN failure

    """
    stack = Stack() # Stack to track openers and their positions
    line = 1 # Initialize line and column counters
    col = 0
    errors = [] # List to collect error messages

    # ── STATE FLAG ───────────────────────────────────────────────
    # in_string tracks whether we are currently inside a "quoted
    # string". While True, structural characters like { and [ are
    # just text content — they must be ignored by the validator.
    # This is the key insight that separates a real validator from
    # a naive parentheses checker.
    in_string = False
    escaped = False # Tracks if the previous character was a backslash

    for character in json_string:
        
        col += 1 # Increment column for each character

        if character == '\n':
            line += 1
            col = 0 # Reset column to 0 when newline is encountered
        
        # ── STRING MODE ──────────────────────────────────────────
        # If we are inside a quoted string, the only characters
        # that matter are:
        #   backslash  → the next char is escaped, skip it
        #   double-quote → this ends the string
        # Everything else is just string content — skip it.

        if in_string:
            if escaped:
                escaped = False
                continue                   # skip this character, it is escaped
            elif character == "\\":
                escaped = True
                continue                   # it is escaped (e.g., \")
            elif character == "\"":
                in_string = False          # we are leaving the string
            continue                       # either way, move on

        # ── NORMAL MODE ──────────────────────────────────────────
        # We are outside any string. Structural characters matter.

        # Encountering a double-quote means we are entering a string.
        # From this point until the matching closing quote, we must
        # ignore all braces and brackets.
        
        if character == "\"":
            in_string = True
            continue
        
        # Opening brace/bracket: push it onto the stack along with
        # its location. We store the location so that if this opener
        # is never closed, we can tell the user WHERE it was opened.
        if character == '{' or character == '[':
            stack.push((character, line, col))
            continue
    
        # Closing brace/bracket: this is the core stack operation.
        # Pop the most recent opener and verify it matches this
        # closer. { must match }, [ must match ].
        elif character == '}' or character == ']':
            if stack.is_empty():
                # Nothing to match against — this closer is unexpected.
                # REPORT error: unexpected closer at (line, col)
                errors.append(f"ERROR: Unexpected '{character}' at Line {line}, Col {col}")
                continue

            else:
                open_char, open_line, open_col = stack.pop()
                if MATCHING[character] != open_char:
                    # The opener and closer don't pair up.
                    errors.append(f"ERROR: Expected '{MATCHING[character]}' at git Line {open_line}, Col {open_col} but found '{character}' at Line {line}, Col {col}")
                    continue
            
    # If the stack still has items, those openers were never closed.
    # Report each one with the location where it was opened.
    while not stack.is_empty():
        open_char, open_line, open_col = stack.pop()
        errors.append(f"ERROR: Unclosed '{open_char}' at Line {open_line}, Col {open_col}")

    if len(errors) == 0:
        return True, errors
    else:
        return False, errors


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