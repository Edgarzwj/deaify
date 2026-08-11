// algorithm.go — cross-language before/after for code-humanizer (#16–#22).
// Run `go run algorithm.go` to confirm both versions agree on the sample input.

package main

import (
	"fmt"
	"math"
)

// ---------- BEFORE (AI-sounding) ----------

// this function calculates base raised to exp using a loop
func calculatePower(base float64, exp int) float64 {
	result := 1.0
	for i := 0; i < exp; i++ { // iterate exp times
		result = result * base
	}
	return result
}

// this function removes duplicate elements from a slice
func removeDuplicates(arr []int) []int {
	result := []int{}
	for i := 0; i < len(arr); i++ {
		found := false
		for j := 0; j < len(result); j++ {
			if result[j] == arr[i] {
				found = true
			}
		}
		if !found {
			result = append(result, arr[i])
		}
	}
	return result
}

func solveBefore(data []int) int {
	const MOD = 1000000007
	ans := 0
	for i := 0; i < len(data); i++ {
		ans = (ans + data[i]) % MOD
	}
	return ans
}

// ---------- AFTER (humanized) ----------

func power(base float64, exp int) float64 {
	return math.Pow(base, float64(exp))
}

func unique(items []int) []int {
	seen := make(map[int]struct{})
	out := make([]int, 0, len(items))
	for _, v := range items {
		if _, ok := seen[v]; ok {
			continue
		}
		seen[v] = struct{}{}
		out = append(out, v)
	}
	return out
}

const mod = 1_000_000_007

func sumMod(values []int) int {
	total := 0
	for _, v := range values {
		total = (total + v) % mod
	}
	return total
}

func main() {
	data := []int{3, 1, 3, 2, 2}

	// before
	fmt.Println(calculatePower(2, 10), removeDuplicates(data), solveBefore([]int{1e9, 1e9}))
	// after
	fmt.Println(power(2, 10), unique(data), sumMod([]int{1e9, 1e9}))
}
