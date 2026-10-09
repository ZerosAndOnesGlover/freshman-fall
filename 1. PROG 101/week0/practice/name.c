#include <stdio.h>
int main(void) {
    char name[10];
    int age;
    printf("Name: ");
    scanf("%s", name);
    printf("Age: ");
    scanf("%d", &age);
    printf("%s is %d\n", name, age);
    return 0;
}
