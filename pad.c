/*
 * == SUGGESTION #1 ==
 *
 * Padding field names contain a trailing underscore to indicate
 * they are NOT for use.
 * 
 * Note: some conventions like Google C++ style use var_ for class
 * members.
 */
#if 0
struct S {
    uint8_t pad0_;
    uint8_t pad0_[7];
    uint8_t pad1_
    uint8_t pad3_[2];

    /* OR "unused" name */
    uint8_t unused0_;
    uint8_t unused0_[7];
    uint8_t unused1_;
    uint8_t unused3_[2];
};
#endif

/*
 * == SUGGESTION #2 ==
 *
 * The following macro would enforce uniformity of padding data type and naming. 
 * Yes the padding name would change as file changes: but the name should not
 * matter! And if for some reason such a field crops in debugging the embedded 
 * line number is unambiguous.
 * 
 * Additionally we could drop the training suffix in pad so that the naming
 * looks like:
 * 
 * uint8_t pad_1234[3];
 */

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>

/* Declare explicit padding within a structure. */
/* ie WT_PAD_STRUCT(3) => uint8_t pad137_[3] */
#define WT_PAD_STRUCT(size) uint8_t pad##__LINE__##_[(size)]

#define WT_PAD_STRUCT_INIT {0}

struct S {
    WT_PAD_STRUCT(2);
    uint16_t f1;
};

int main(void)
{
    struct S s;
    struct S s2;
    
    assert(offsetof(struct S, f1) == 2);

    s2 = (struct S){ WT_PAD_STRUCT_INIT, .f1 = 7u};
    assert(s2.f1 == 7u);
    return 0;
}

/* 
 * FOR COMPLETENESS ONLY -- * NOT* BEING SUGGESTED
 *
 * Discarded after office hours feedback: [[maybe_unused]] while it IS a C23 pragma
 * is confusing in this context as this is really should NOT be used.
 */
#if 0
struct S {
    /* [[maybe_unused]] */ uint8_t pad0_;
    /* [[maybe_unused]] */ uint8_t pad0_[7];
};
#endif
