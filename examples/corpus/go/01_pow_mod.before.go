package main

import "fmt"

func calculatePower(base, exp int) int {
	result := 1
	for i := 0; i < exp; i++ { // iterate exp times
		result *= base
	}
	return result
}

type MathUtility struct{}

func (m MathUtility) Compute(x int) int {
	return x * x
}

const MOD = 1000000007

func processData(data []int) int {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("An error occurred")
		}
	}()
	ans := 0
	for i := 0; i < len(data); i++ {
		ans = (ans + data[i]) % MOD
	}
	return ans
}
