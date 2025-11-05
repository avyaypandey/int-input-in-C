Rust-C Integer Input Integration

This project demonstrates a safe way to read integer input in C using a Rust backend for input validation. The C side handles the table printing logic, while Rust ensures input is sanitized, preventing buffer overflows, invalid characters, or excessive numbers.

Features

Safe integer input via Rust, callable from C.

Validates numeric characters only.

Prevents empty input or overly large integers.

C handles arithmetic and printing.

Cross-language integration via FFI.

Integration tests for valid and invalid inputs.

Project Structure
table_project/
│
├─ rust_input/                # Rust side
│   ├─ src/
│   │   └─ lib.rs             # Rust input validation
│   ├─ Cargo.toml             # Rust project config
│   └─ target/                # Build outputs (auto-generated)
│
├─ c_logic/                   # C side
│   ├─ main.c                 # C code for multiplication table
│   └─ Makefile               # Build both Rust and C
│
└─ integration_tests.py       # Python tests for integration

Build Instructions

Make sure you have installed:

Rust (rustup)

GCC

Make

Then from c_logic:

make        # builds Rust library and links with C
make test   # runs Python integration tests

Usage
./table


Prompts for an integer input.

Prints the multiplication table from 1 to 10 for the entered number.

Notes for Developers

Rust exposes the read_int_into_buffer function via FFI.

Unsafe blocks exist in Rust to allow C to provide a mutable buffer.

All input validation (length, digits, empty input) occurs in Rust; C assumes the buffer is safe.

Memory is managed by C; Rust does not allocate for return strings.

Testing

integration_tests.py tests valid inputs, invalid inputs (letters, signs, overflows), and edge cases like INT_MAX.

Python integration tests simulate user input and verify C table output.
