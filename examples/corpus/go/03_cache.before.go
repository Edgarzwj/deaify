package main

import "encoding/json"

type CacheManager struct {
	store map[string]interface{}
}

func (c CacheManager) GetCopy(key string) interface{} {
	// we need a deep copy
	cp, _ := json.Marshal(c.store[key])
	var out interface{}
	json.Unmarshal(cp, &out)
	return out
}

func mergeData(data, extra map[string]interface{}) map[string]interface{} {
	tmp := map[string]interface{}{}
	for k, v := range data {
		tmp[k] = v
	}
	for k, v := range extra {
		tmp[k] = v
	}
	return tmp
}
