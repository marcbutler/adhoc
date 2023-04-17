#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

/* +src/include/misc.h */

/* Check if a string matches a prefix. */
#define WT_PREFIX_MATCH(str, pfx) \
    (((const char *)(str))[0] == ((const char *)(pfx))[0] && strncmp(str, pfx, strlen(pfx)) == 0)

/* Check if a string matches a suffix. */
#define WT_SUFFIX_MATCH(str, sfx) \
    (strlen(str) >= strlen(sfx) && strcmp(&str[strlen(str) - strlen(sfx)], sfx) == 0)

/* -src/include/misc.h */

bool str_has_prefix(const char * str, const char * prefix)
{
    while (*str && *prefix && (*str++ == *prefix++));
    return *prefix == 0;
}

bool str_has_suffix(const char * str, const char * suffix)
{
    const char * restrict s;
    for (s = suffix; *str; str++)
        if (*s == *str) s++;
        else s = suffix;
    return *s == *str;
}

#define MIN(a, b) (((a) < (b)) ? (a) : (b))

#define ZERO_T(x) (((x) == 0) ? "TRUE" : "FALSE")

#define NON_ZERO_T(x) (((x) != 0) ? "TRUE" : "FALSE")

#define SHOW(fn, str, fix, truth) \
    printf("%-15s  str='%s'  fix='%s' = %s\n", #fn, str, fix, truth(fn(str, fix)))

#define SHOW_N(fn, str, fix, truth) \
    printf("%-15s  str='%s'  fix='%s' = %s\n", #fn, str, fix, truth(fn(str, fix, MIN(strlen(str), strlen(fix)))))

int main()
{
    SHOW(WT_PREFIX_MATCH, "", "", NON_ZERO_T);
    SHOW(WT_PREFIX_MATCH, "A", "", NON_ZERO_T);
    SHOW(WT_PREFIX_MATCH, "", "A", NON_ZERO_T);
    puts("");
    SHOW(WT_SUFFIX_MATCH, "", "", NON_ZERO_T);
    SHOW(WT_SUFFIX_MATCH, "A", "", NON_ZERO_T);
    SHOW(WT_SUFFIX_MATCH, "", "A", NON_ZERO_T);
    puts("");
    SHOW_N(strncmp, "", "", ZERO_T);
    SHOW_N(strncmp, "A", "", ZERO_T);
    SHOW_N(strncmp, "", "A", ZERO_T);
    puts("");
    SHOW(str_has_prefix, "", "", NON_ZERO_T);
    SHOW(str_has_prefix, "A", "", NON_ZERO_T);
    SHOW(str_has_prefix, "", "A", NON_ZERO_T);
    puts("");
    SHOW(str_has_suffix, "", "", NON_ZERO_T);
    SHOW(str_has_suffix, "A", "", NON_ZERO_T);
    SHOW(str_has_suffix, "", "A", NON_ZERO_T);
    return 0;
}
