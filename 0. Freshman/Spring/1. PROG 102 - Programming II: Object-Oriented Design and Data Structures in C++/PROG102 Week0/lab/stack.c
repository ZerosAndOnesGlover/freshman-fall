/* stack.c - PROG 102 Lab 0: a growable integer stack in C. Do not modify.
 * Build: gcc -std=c11 -Wall -Wextra -pedantic -g stack.c -o stack_c */
#include <stdio.h>
#include <stdlib.h>

struct IntStack { int* data; int count; int cap; };

void stack_init(struct IntStack* s, int cap) {
    s->data = malloc(cap * sizeof *s->data);
    s->count = 0;
    s->cap = cap;
}

void stack_push(struct IntStack* s, int v) {
    if (s->count == s->cap) {                       /* full: double the capacity */
        int* bigger = malloc(2 * s->cap * sizeof *bigger);
        for (int i = 0; i < s->count; i++) bigger[i] = s->data[i];
        free(s->data);
        s->data = bigger;
        s->cap *= 2;
    }
    s->data[s->count++] = v;
}

int  stack_pop(struct IntStack* s)         { return s->data[--s->count]; }
int  stack_size(const struct IntStack* s)  { return s->count; }
int  stack_empty(const struct IntStack* s) { return s->count == 0; }
void stack_free(struct IntStack* s)        { free(s->data); s->data = NULL; s->count = s->cap = 0; }

int main(void) {
    struct IntStack s;
    stack_init(&s, 2);
    for (int i = 1; i <= 5; i++) stack_push(&s, i * i);
    printf("size=%d cap=%d\n", stack_size(&s), s.cap);
    while (!stack_empty(&s)) {
        printf("%d", stack_pop(&s));
        printf(stack_empty(&s) ? "\n" : " ");
    }
    stack_free(&s);
    return 0;
}
