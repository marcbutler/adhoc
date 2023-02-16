#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void usage()
{
    puts("\nUsage: snooze milliseconds\n");
}

int main(int argc, char **argv)
{
    long ms;
    char *strend;
    if (argc != 2) {
        fprintf(stderr, "\nERROR: Invalid usage.\n");
        usage();
        exit(EXIT_FAILURE);
    }
    ms = strtol(argv[1], &strend, 10);
    if (*strend != 0) {
        fprintf(stderr, "\nERROR: Invalid time value - not an integer.\n");
        exit(EXIT_FAILURE);
    }
    Sleep(ms);
    return 0;
}
