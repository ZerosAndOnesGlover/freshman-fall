#include "mathutils.h"
#include <stdio.h>

int main (void) {
  int n;
  printf("Enter an integer: ");
  scanf("%i", &n);
  printf("The square of %i is %i\n", n, square(n));
  return 0;
}
  