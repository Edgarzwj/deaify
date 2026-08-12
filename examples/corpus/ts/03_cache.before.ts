class CacheManager {
  private store: Record<string, any> = {};
  getCopy(key: string): any {
    // we need a deep copy to be safe
    return JSON.parse(JSON.stringify(this.store[key]));
  }
}

function mergeData(data: Record<string, any>, extra: Record<string, any>): Record<string, any> {
  const tmp = { ...data };
  Object.assign(tmp, extra);
  return tmp;
}
