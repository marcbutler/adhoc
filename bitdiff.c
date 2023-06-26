/*
 * Calculate the difference in bits between binary files.
 * Files are assumed to be of the same length.
 * 
 * Usage: bindiff file1 file2
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    FILE *in1, *in2;
    int b1, b2, d;
    long diffcount, bitcount;
    float diffpct;

    in1 = fopen(argv[1], "rb");
    in2 = fopen(argv[2], "rb");
    for (diffcount = 0, bitcount = 0;; bitcount += 8) {
        b1 = fgetc(in1);
        b2 = fgetc(in2);
        if (b1 == EOF || b2 == EOF) break;
        if (b1 != b2) {
            d = b1 ^ b2;
            while (d != 0) {
                diffcount++;
                d = d & (d - 1);
            }
        }
    }
    assert(b1 == EOF && b2 == EOF);

    diffpct = diffcount / (float)bitcount;
    printf("%s %s\n", argv[1], argv[2]);
    printf("bit difference %li bits of %li bits (%f)\n", diffcount, bitcount, diffpct);
    exit(EXIT_SUCCESS);
}