#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

#define BUFFER_SIZE 64

/**
 * @brief Reads an integer from the user using a Rust function.
 * 
 * This function wraps the Rust function `read_int_into_buffer`.
 * 
 * @note The Rust implementation contains two `unsafe` blocks internally:
 *       1. Converting the `prompt` C string to Rust &str
 *       2. Writing into the caller-provided buffer
 * 
 *       It is the caller's responsibility to ensure that:
 *       - `number_buf` is valid and has at least BUFFER_SIZE bytes.
 *       - The buffer pointer is not NULL.
 * 
 * @return 0 on success (number_buf contains a valid integer string),
 *         1 on error (invalid input, I/O error, etc.).
 */

extern int read_int_into_buffer(const char* prompt, char* buf, size_t buf_len);

/**
 * @brief Entry point: prints the multiplication table of a user-provided number.
 * 
 * The input is obtained via `read_int_into_buffer`. Rust handles all validation.
 * C only converts the string to an integer and prints the table.
 */

int main() {
	char number_buf[BUFFER_SIZE];
	if (read_int_into_buffer("Enter a number: ", number_buf, sizeof(number_buf))) {
		return 1; //Assumes rust aldready printed the error
	}
	int number = atoi(number_buf); // Assumes rust makes sure it is valid

	for (int i = 1; i <= 10; i++) {
		printf("%d times %d is %d\n", number, i, number*i);
	}

	return 0;
}
