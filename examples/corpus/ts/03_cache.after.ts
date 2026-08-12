class Cache {
  private store: Record<string, any> = {};
  get(key: string): any {
    return this.store[key];
  }
  set(key: string, value: any): void {
    this.store[key] = value;
  }
}

function merge(base: Record<string, any>, other: Record<string, any>): Record<string, any> {
  return { ...base, ...other };
}
