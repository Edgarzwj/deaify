"""
Example: humanizing AI-flavored algorithm code (code-humanizer skill).

BEFORE = what an LLM typically emits.
AFTER  = the humanized version.
Both produce identical outputs on the normal path (verified by the asserts below).
"""

# ---------------- BEFORE (AI-sounding) ----------------
def calculate_power(base, exp):
    result = 1
    for i in range(exp):  # iterate exp times
        result = result * base
    return result

def remove_duplicates(arr):
    result = []
    for i in range(len(arr)):
        if arr[i] not in result:
            result.append(arr[i])
    return result

class SortUtility:
    def __init__(self):
        pass
    def sort_data(self, data):
        return sorted(data)

MOD = 1000000007

def solve(data):
    try:
        ans = 0
        for i in range(len(data)):
            ans = (ans + data[i]) % MOD
        return ans
    except Exception as e:
        print("An error occurred")
        return -1


# ---------------- AFTER (humanized) ----------------
def power(base, exp):
    return base ** exp

def unique(items):
    return list(dict.fromkeys(items))  # order-preserving, same behavior

MOD = 1_000_000_007

def sum_mod(values):
    return sum(values) % MOD


# ---------------- VERIFY (behavior preserved) ----------------
assert calculate_power(2, 10) == power(2, 10) == 1024
assert remove_duplicates([3, 1, 3, 2, 2]) == unique([3, 1, 3, 2, 2]) == [3, 1, 2]
assert solve([1, 2, 3]) == sum_mod([1, 2, 3]) == 6
assert solve([10**9, 10**9]) == sum_mod([10**9, 10**9]) == (2 * 10**9) % MOD
print("PASS: before and after match on all sample inputs")
