function fib(n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
const n = process.argv[2] ? parseInt(process.argv[2]) : 30;
const t0 = process.hrtime.bigint();
const r = fib(n);
const s = Number(process.hrtime.bigint() - t0) / 1e9;
console.log(`  ${'JS (node)'.padEnd(12)} fib(${n}) = ${String(r).padEnd(10)} ${s.toFixed(3).padStart(8)} s`);
