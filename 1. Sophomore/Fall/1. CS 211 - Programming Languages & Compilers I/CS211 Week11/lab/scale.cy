fn scale(a: [int], n: int, k: int) -> int {
    let s = 0;
    let i = 0;
    while i < n {
        let f = k * 2 + 1;
        s = s + a[i] * f;
        i = i + 1;
    }
    return s;
}
