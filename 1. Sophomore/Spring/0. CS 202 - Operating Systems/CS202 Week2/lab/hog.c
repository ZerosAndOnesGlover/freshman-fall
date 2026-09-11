/* hog.c: use the CPU and nothing else, forever. CS 202 Lab 2. */
int main(void)
{
    volatile unsigned long x = 0;
    for (;;)
        x++;
}
