# Dev flags
CC = gcc
CFLAGS = -Wall -Wextra -O2

# rust cargo command
CARGO = cargo

#Project Target
RUST_LIB_NAME = read_input
RUST_LIB_DIR = ../rust_input
C_SRC = main.c
C_BIN = table

#Paths
RUST_TARGET_DIR = $(RUST_LIB_DIR)/target/release
RUST_STATIC_LIB = $(RUST_TARGET_DIR)/lib$(RUST_LIB_NAME).a

#default target
all: $(C_BIN)

# Build Rust static library
$(RUST_STATIC_LIB):
	cd $(RUST_LIB_DIR) && cargo build --release

# Compile C program and link with Rust
$(C_BIN): $(C_SRC) $(RUST_STATIC_LIB)
	$(CC) $(CFLAGS) -I$(RUST_LIB_DIR)/include -L$(RUST_TARGET_DIR) \
	    $(C_SRC) -l$(RUST_LIB_NAME) -o $(C_BIN)

# Clean build artifacts
clean:
	cd $(RUST_LIB_DIR) && cargo clean
	rm -f $(C_BIN)

# Python integration tests
PYTEST = python3
TEST_SCRIPT = ../integration_tests.py  # relative to c_logic directory

.PHONY: test

test: $(C_BIN)
	@echo "Running integration tests..."
	@$(PYTEST) $(TEST_SCRIPT)

