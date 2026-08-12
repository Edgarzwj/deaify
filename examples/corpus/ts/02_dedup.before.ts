function removeDuplicates(arr: number[]): number[] {
  const result: number[] = [];
  for (let i = 0; i < arr.length; i++) { // remove duplicate elements
    if (result.indexOf(arr[i]) === -1) {
      result.push(arr[i]);
    }
  }
  return result;
}

function getFirst(arr: number[]): number {
  const tmp = arr[0];
  return tmp;
}
