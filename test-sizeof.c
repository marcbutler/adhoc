#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

struct S1 {
	uint32_t	f1;
	uint16_t	f2;
	uint8_t		f3;
	uint8_t		f4[];
};

void fn1(struct S1 *ps1)
{
	struct S1 *ps2;
	printf("fn1 ps1==%p\n", ps1);
	printf("sizeof(*ps1) == %zu\n", sizeof(*ps1));
	printf("sizeof(*ps2) == %zu\n", sizeof(*ps2));
}

int main()
{
	struct S1 s1;
	struct S1 *ps1 = &s1;
	printf("sizeof(struct S1) == %zu\n", sizeof(struct S1));
	printf("sizeof(s1) == %zu\n", sizeof(s1));
	printf("sizeof(*ps1) == %zu\n", sizeof(*ps1));
	printf("offsetof(f4) == %zu\n", offsetof(struct S1, f4));
	fn1(NULL);
	fn1(&s1);
	fn1(ps1);
	return EXIT_SUCCESS;
}
