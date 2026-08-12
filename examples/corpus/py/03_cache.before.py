import copy

class CacheManager:
    def __init__(self):
        self.store = {}
    def get_copy(self, key):
        return copy.deepcopy(self.store.get(key))

def merge_data(data, extra):
    tmp = dict(data)
    tmp.update(extra)
    return tmp
