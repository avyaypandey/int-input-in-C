# int-input-in-C
A small, robust C program that reads and validates integer input from the user without using scanf().
It demonstrates safe buffer handling, input sanitization, and clear error reporting — a minimalist example of writing secure and maintainable C code.

✳️ Overview

This program:

Uses fgets() instead of scanf() to safely read user input.

Validates every character to ensure the input is a valid integer.

Handles edge cases such as:

Empty input

Non-numeric characters

Input longer than the buffer

I/O errors or end-of-file conditions

Cleans the input buffer when needed.

Once a valid integer is entered, it prints a simple multiplication table (1 to 10) for that number.
