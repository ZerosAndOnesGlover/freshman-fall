# Error Log for Problem 4

The original program had 10 deliberate errors. These are the fixes that were made:

1. Missing closing angle bracket in `#include <stdio.h`.
   - Fixed by changing it to `#include <stdio.h>`.

2. The function prototype used the wrong parameter type.
   - `int compute_sum(int arr, int n);` was changed to `int compute_sum(int *arr, int n);`.

3. A semicolon was missing after the `compute_sum` call.
   - `int total = compute_sum(numbers, 5)` became `int total = compute_sum(numbers, 5);`.

4. The `printf` call for the sum was missing a comma.
   - `printf("Sum: %d\n" total);` was corrected to `printf("Sum: %d\n", total);`.

5. The `double` value `pi` was printed with the wrong format specifier.
   - `printf("Pi: %d\n", pi);` was changed to `printf("Pi: %f\n", pi);`.

6. The `SQUARE` macro did not protect its argument with parentheses.
   - `#define SQUARE(x) x * x` became `#define SQUARE(x) ((x) * (x))`.

7. The allocated memory was freed twice.
   - One of the `free(ptr);` calls was removed.

8. `main` returned without a value.
   - `return;` was changed to `return 0;`.

9. A semicolon was missing after the initialization of `sum`.
   - `int sum = 0` became `int sum = 0;`.

10. The loop condition used `<=` instead of `<`.
    - `for (int i = 0; i <= n; i++)` was changed to `for (int i = 0; i < n; i++)`.
