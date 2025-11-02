#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define SIZE_BUFFER 64

const char *read_int(const char* prompt) {
	char buffer[SIZE_BUFFER];

	printf("%s", prompt);

	if (!fgets(buffer, SIZE_BUFFER, stdin)) {
		int ch;
		while ((ch = getchar()) != '\n' && ch != EOF);

		return "I/O error";
	}

	if ((buffer[0]) == '\n') return "Empty input";

	for (int i = 0; buffer[i] != '\0'; i++) {
		if ((buffer[i]) == '\n') {
			static char safe_input[SIZE_BUFFER];
			strncpy(safe_input, buffer, i);
			safe_input[i] = '\0';

			return safe_input;
		}

		if (!isdigit((unsigned char)buffer[i])) return "Not a number";
	}

	int ch;
	while ((ch = getchar()) != '\n' && ch != EOF);

	return "Probably input is too long";
}

int main() {
    const int max_value = 10;
    int number = 0;
    const char *num_or_fail = read_int("Enter a number: ");
    
    if (!isdigit((unsigned char)num_or_fail[0])) {
	    printf("Error: %s\n", num_or_fail);
	    return 1;
    }

    number = atoi(num_or_fail);
    
    for (int i = 1; i <= max_value; i++) {
        printf("%d times %d is: %d\n", number, i, number*i);
    }

    return 0;
}
