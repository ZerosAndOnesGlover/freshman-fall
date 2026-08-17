int scale(int *a, int n, int k) {
    int s = 0;
    int i = 0;
    while (i < n) {
        int f = k * 2 + 1;
        s = s + a[i] * f;
        i = i + 1;
    }
    return s;
}
