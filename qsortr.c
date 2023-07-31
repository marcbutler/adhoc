#include <stdlib.h>
#include <stdio.h>
#include <thread.h>

typedef int (*ext_cmp_fn)(const void *, const void *, void *);

static _Thread_local ext_cmp_fn cmp_fn;
static _Thread_local void *cmp_ctx = NULL;

static int 
qsort_compat_cmp(const void *a, const void *b)
{
	return cmp_fn(a, b, cmp_ctx);
}

void
ext_qsort(void *base, size_t cnt, size_t sz, ext_cmp_fn fn, void *ctx)
{
	cmp_fn = fn;
	cmp_ctx = ctx;
	qsort(base, cnt, sz, qsort_compat_cmp);
	cmp_fn = NULL;
	cmp_ctx = NULL;
}

int 
test_cmp_fn(const void *a, const void *b, void *ctx)
{
	printf("cmp(%d, %d) %p %d\n", *(int*)a, *(int*)b, ctx, *(int*)ctx);
	usleep(500);
	return *(int *)a < *(int *)b;
}

int main(void)
{
	int ary[] = { 3, 4, 56, 11, 778, 309, 10, 2 };
	int ctx[] = { 1, 2, 3, 4, 5 };
	
	ext_qsort(ary, sizeof(ary)/sizeof(ary[0]), sizeof(ary[0]), test_cmp_fn, &ctx[i]);
	return 0;
}
