function power(base: number, exponent: number): number {
  return base ** exponent;
}

function square(x: number): number {
  return x * x;
}

const MOD = 1_000_000_007;

function sumMod(values: number[]): number {
  return values.reduce((a, b) => a + b, 0) % MOD;
}
