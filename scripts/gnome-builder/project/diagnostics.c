#include <stdio.h>

__attribute__((deprecated)) static int
old_square (int value)
{
  return value * value;
}

static void
warnings (void)
{
  int unused_value = 3;                  /* unused variable */

  printf ("%d\n", "text");               /* warning: format mismatch */
  printf ("%d\n", old_square (2));       /* deprecated call */
}

int
main (void)
{
  undefined_call (1);                    /* error: implicit declaration */
  printf ("%d\n", missing_variable);     /* error: undeclared identifier */
  warnings ();
  return 0;
}
