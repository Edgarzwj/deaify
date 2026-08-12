function calculatePower(base: number, exponent: number): number {
  let result = 1;
  for (let i = 0; i < exponent; i++) { // iterate exponent times
    result = result * base;
  }
  return result;
}

class MathUtility {
  compute(x: number): number {
    return x * x;
  }
}

const MOD = 1000000007;

function processData(data: number[]): number {
  try {
    let ans = 0;
    for (let i = 0; i < data.length; i++) {
      ans = (ans + data[i]) % MOD;
    }
    return ans;
  } catch (e) {
    console.log("An error occurred");
    return -1;
  }
}
