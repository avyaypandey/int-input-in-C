# 🛠 Rust-C Integer Input Integration

A demonstration of **safe integer input in C** using **Rust** for validation. C handles the multiplication table, while Rust ensures input safety.

---

## 🔹 Features

| Feature           | Description                                       |
| ----------------- | ------------------------------------------------- |
| Safe input        | Rust validates integers and rejects invalid input |
| Buffer safety     | Prevents overflow and empty input                 |
| Cross-language    | C calls Rust via FFI                              |
| Integration tests | Python scripts validate both C and Rust logic     |

---

## 📂 Project Structure

```
table_project/
│
├─ rust_input/                # Rust backend
│   ├─ src/lib.rs             # Rust input logic
│   ├─ Cargo.toml             # Rust config
│   └─ target/                # Build artifacts (auto-generated)
│
├─ c_logic/                   # C frontend
│   ├─ main.c                 # Multiplication table logic
│   └─ Makefile               # Build Rust + C
│
└─ integration_tests.py       # Python tests
```

---

## ⚡ Build Instructions

Install required tools:

* Rust (`rustup`)
* GCC
* Make

Then run:

```bash
cd c_logic
make        # Build Rust library + C binary
make test   # Run Python integration tests
```

---

## 💻 Usage

```bash
./table
```

* Prompts for an integer.
* Prints the multiplication table from 1 to 10.

Example:

```
Enter a number: 5
5 times 1 is 5
5 times 2 is 10
...
5 times 10 is 50
```

---

## 📝 Developer Notes

* Rust function `read_int_into_buffer` is exposed via `extern "C"` FFI.
* Unsafe blocks in Rust are required for mutable buffer access from C.
* Rust validates input fully; C assumes safe buffer contents.
* C manages memory; Rust does **not** allocate return strings.
* Invalid input in Rust prints an error and returns `1` to C.

---

## 🧪 Testing

Python integration tests cover:

* Valid inputs (random integers)
* Invalid inputs (letters, signs, empty, overly long numbers)
* Edge cases like `INT_MAX`
* Buffer overflow attempts

Run tests:

```bash
make test
```

---
Python integration tests simulate user input and verify C table output.

