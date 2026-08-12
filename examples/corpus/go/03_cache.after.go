package main

type Cache struct {
	store map[string]interface{}
}

func (c Cache) Get(key string) interface{} {
	return c.store[key]
}

func (c Cache) Set(key string, value interface{}) {
	c.store[key] = value
}

func merge(base, other map[string]interface{}) map[string]interface{} {
	out := map[string]interface{}{}
	for k, v := range base {
		out[k] = v
	}
	for k, v := range other {
		out[k] = v
	}
	return out
}
