#!/usr/bin/env python3
# integration_tests.py
# Run from project root. Expects binary at ./c_logic/table

import subprocess
import random
import string
import re
import sys

TABLE_BINARY = "./table"

def run_table(input_str, timeout=3):
    """Run the table program with given input and capture output."""
    proc = subprocess.run(
        [TABLE_BINARY],
        input=input_str,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    return proc.returncode, proc.stdout, proc.stderr

def assert_not_crashed(ret, out, err, case_desc=""):
    """Ensure process did not die from a signal (ret < 0)."""
    if ret < 0:
        raise AssertionError(f"Process crashed (signal {-ret}) on case: {case_desc}\nstdout:\n{out}\nstderr:\n{err}")

def looks_like_table_output(out, n):
    """Check if output contains at least one expected table line for n."""
    # e.g. "5 times 1 is 5"
    pattern = rf"{n}\s+times\s+1\s+is\s+{n}"
    return re.search(pattern, out) is not None

def test_valid_input_random():
    n = random.randint(0, 1000)
    ret, out, err = run_table(f"{n}\n")
    assert_not_crashed(ret, out, err, f"valid:{n}")
    assert ret == 0, f"Expected success for valid input {n}, got ret={ret}, stderr={err}"
    # verify all lines exist
    for i in range(1, 11):
        expected = f"{n} times {i} is {n*i}"
        if expected not in out:
            raise AssertionError(f"Missing expected line for {n}: '{expected}'\nstdout:\n{out}")
    print(f"[OK] valid input {n}")

def test_invalid_inputs():
    invalid_cases = [
        "",                # empty
        "abc",             # letters
        "+5",              # plus sign
        "-5",              # minus sign
        "999999999999999", # very large
        "12abc34",         # mixed digits + letters
        " " * 5,           # spaces only
    ]
    # add a few random letters
    for _ in range(5):
        invalid_cases.append("".join(random.choices(string.ascii_letters, k=5)))

    for case in invalid_cases:
        ret, out, err = run_table(f"{case}\n")
        assert_not_crashed(ret, out, err, f"invalid:{case!r}")
        # We expect non-zero exit or at minimum an error printed by Rust to stderr.
        if ret == 0:
            # if program succeeded unexpectedly, ensure output isn't nonsense
            # (that's OK, but warn)
            print(f"[WARN] program accepted invalid input '{case}' (returned 0). stdout:\n{out}")
        else:
            # good: program rejected input
            print(f"[OK] invalid input correctly rejected: {case!r} (ret={ret})")

def test_buffer_overflow():
    # Create very long numeric string (longer than C buffer 64)
    long_num = "1" * 2000
    ret, out, err = run_table(long_num + "\n")
    assert_not_crashed(ret, out, err, "long_numeric")
    # Accept either success or clean failure; but must not crash.
    if ret == 0:
        # if it succeeded, at least one valid table line should appear
        if not re.search(r"1\s+times\s+1\s+is\s+\d+", out):
            raise AssertionError(f"Long numeric input returned 0 but output doesn't look like table.\nstdout:\n{out}\nstderr:\n{err}")
        print("[OK] long numeric input handled (truncated or accepted) without crash")
    else:
        print(f"[OK] long numeric input rejected cleanly (ret={ret})")

    # Very long non-numeric string
    long_alpha = "".join(random.choices(string.ascii_letters + string.digits, k=5000))
    ret, out, err = run_table(long_alpha + "\n")
    assert_not_crashed(ret, out, err, "long_mixed")
    if ret == 0:
        print("[WARN] very long mixed input accepted unexpectedly (ret=0).")
    else:
        print("[OK] very long mixed input rejected (ret != 0)")

def test_int_max_and_overflow():
    # Test INT_MAX for 32-bit signed int
    INT_MAX = 2**31 - 1
    ret, out, err = run_table(f"{INT_MAX}\n")
    assert_not_crashed(ret, out, err, f"int_max:{INT_MAX}")
    if ret == 0:
        # check at least the first line is present
        if not looks_like_table_output(out, INT_MAX):
            print(f"[WARN] INT_MAX accepted but output may be odd. stdout first 200 chars:\n{out[:200]}")
        else:
            print("[OK] INT_MAX accepted and produced table (beware overflow in arithmetic)")
    else:
        print(f"[OK] INT_MAX rejected (ret={ret})")

    # Now a number larger than 32-bit max
    big = 2**40
    ret, out, err = run_table(f"{big}\n")
    assert_not_crashed(ret, out, err, f"big:{big}")
    if ret == 0:
        print("[WARN] very large integer accepted (may be truncated).")
    else:
        print("[OK] very large integer rejected")

def main():
    print("Running integration tests...")
    test_valid_input_random()
    test_invalid_inputs()
    test_buffer_overflow()
    test_int_max_and_overflow()
    print("All integration tests completed.")

if __name__ == "__main__":
    main()

