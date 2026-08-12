package main

func unique(items []int) []int {
	seen := map[int]bool{}
	out := []int{}
	for _, v := range items {
		if !seen[v] {
			seen[v] = true
			out = append(out, v)
		}
	}
	return out
}
