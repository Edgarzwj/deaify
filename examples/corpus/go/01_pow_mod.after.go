package main

import "math"

func power(base, exp int) int {
	return int(math.Pow(float64(base), float64(exp)))
}

func square(x int) int {
	return x * x
}

const MOD = 1_000_000_007

func sumMod(values []int) int {
	total := 0
	for _, v := range values {
		total += v
	}
	return total % MOD
}
