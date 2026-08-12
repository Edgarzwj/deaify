def calculate_power(base, exponent):
    result = 1
    for i in range(exponent):  # iterate exponent times
        result = result * base
    return result

class MathUtility:
    def compute(self, x):
        return x * x

MOD = 1000000007

def process(data):
    try:
        ans = 0
        for i in range(len(data)):
            ans = (ans + data[i]) % MOD
        return ans
    except Exception as e:
        print("An error occurred")
        return -1
