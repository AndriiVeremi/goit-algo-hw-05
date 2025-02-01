def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            upper_bound = arr[mid]
            return (iterations, upper_bound)
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid] if upper_bound is None else min(upper_bound, arr[mid])
            right = mid - 1

    if left < len(arr) and (upper_bound is None or arr[left] < upper_bound):
        upper_bound = arr[left]

    return (iterations, upper_bound)


arr = [1.1, 2.3, 3.5, 4.8, 6.0, 7.2, 8.9]
target = 5.0
result = binary_search(arr, target)
print(result)  