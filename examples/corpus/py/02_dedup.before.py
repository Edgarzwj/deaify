def remove_duplicates(arr):
    result = []
    for i in range(len(arr)):
        if arr[i] not in result:  # remove duplicate elements
            result.append(arr[i])
    return result

def get_first(arr):
    tmp = arr[0]
    return tmp
