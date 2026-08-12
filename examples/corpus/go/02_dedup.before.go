package main

func removeDuplicates(arr []int) []int {
	result := []int{}
	for i := 0; i < len(arr); i++ { // remove duplicate elements
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
