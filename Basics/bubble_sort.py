def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                # Swap if the element is greater than the next one
                arr[i], arr[j] = arr[j], arr[i]

                #another syntax
                # temp = arr[i]
                # arr[i] = arr[j]
                # arr[j] = temp

arr = [5, 1, 4, 2, 8]
bubble_sort(arr)
print("Sorted array:", arr)
