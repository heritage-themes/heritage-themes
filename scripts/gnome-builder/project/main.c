#include <stdio.h>

/* TODO: read the points from a file */
struct point { int x; int y; };

static int
square (int value)
{
  return value * value;
}

static int
sum_of_squares (struct point p)
{
  return square (p.x) + square (p.y);
}

int
main (void)
{
  struct point p = { 3, 4 };

  printf ("%d\n", sum_of_squares (p));
  return 0;
}
