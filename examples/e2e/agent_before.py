# This helper class calculates modular powers for cryptography.
class MathHelper:
    def mod_pow(self, base, exp, mod):
        # iterate exp times multiplying the running result
        result = 1
        for i in range(exp):
            result = result * base
            result = result % mod
        return result


DEFAULT_MOD = 1000000007


def secure_hash(data):
    try:
        ans = 1
        for i in range(len(data)):
            ans = (ans * data[i]) % DEFAULT_MOD
        return ans
    except Exception:
        print("An error occurred")
        return -1
