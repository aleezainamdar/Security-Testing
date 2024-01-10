#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include "include/libxml/tree.h"
#include "include/libxml/parser.h"
#include "include/libxml/xmlregexp.h"

#define SIZE 1000

void harness(char* buffer, ssize_t length) {
	if (length >= 0 && length <= SIZE)
	{
		buffer[length-1] = '\0';
		xmlRegexpPtr regex_compile = xmlRegexpCompile ((const xmlChar *)buffer);
		if (regex_compile != NULL)
		{
			xmlRegFreeRegexp(regex_compile);
		}
	}
}


int main(int argc, char** argv) {
	char input[SIZE];
	while (__AFL_LOOP(1000)) {
		ssize_t length = read(STDIN_FILENO, input, SIZE);
		harness(input, length);
	}
	return 0;
}
