/*
 * Construct binary file from text file of bytes described as space separated hex values
 * output from gdb.
 * 
 * Usage: hex2bin input
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BIN_EXT ".bin"

#define LINE_MAX 200
char hexline[LINE_MAX];

int main(int argc, char **argv)
{
    FILE *hexin, *binout;
    char *outname;
    char *instr, *hex;
    unsigned char b;
    int lcount, bcount;

    if (argc != 2) {
        puts("Usage: hex2bin hexfile");
        exit(EXIT_FAILURE);
    }

    hexin = fopen(argv[1], "rb");
    assert(hexin != NULL);

    outname = malloc(strlen(argv[1]) + strlen(BIN_EXT) + 1);
    strcpy(outname, argv[1]);
    strcat(outname, BIN_EXT);
    binout = fopen(outname, "wb");
    assert(binout != NULL);

    lcount = bcount = 0;
    while (fgets(hexline, sizeof(hexline), hexin) != NULL) {
        lcount++;
        instr = &hexline[0];
        while ((hex = strsep(&instr, " \t")) != NULL) {
            sscanf(hex, "0x%2hhx", &b);
            bcount += fwrite(&b, sizeof(b), 1, binout);
        }        
    }
    printf("line count = %d,  byte count = %d\n", lcount - 1, bcount);
    assert(feof(hexin));
    fclose(hexin);
    fclose(binout);
    return 0;
}