/* temperature.c — temperature converter */
#include <stdio.h>

double celsius_to_fahrenheit(double celsius);

int main(void) {
    double c;

    printf("\nEnter temperature in Celsius: ");
    if (scanf("%lf", &c) != 1) {
        fprintf(stderr, "Error: invalid input\n");
        return 1;
    }

    printf("\n\t\t\t %.1f°C = %.1f°F\n", c, celsius_to_fahrenheit(c));
    return 0;
}

double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
