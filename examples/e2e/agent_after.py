import math

MOD = 1_000_000_007


def mod_pow(base, exp, mod):
    return pow(base, exp, mod)


def secure_hash(values):
    return math.prod(values) % MOD
