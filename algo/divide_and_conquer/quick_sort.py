
print('>>> quick sort')

def partition(a_list, start, end):
    """外层进行前置条件的检查，这里就不检查了
    """
    low = start + 1
    high = end
    pivot = a_list[start]

    while True:
        while low <= high and a_list[high] >= pivot:
            high -= 1
        while low <= high and a_list[low] <= pivot:
            low += 1

        if low <= high:
            a_list[low], a_list[high] = a_list[high], a_list[low]
        else:
            break
    a_list[start], a_list[high] = a_list[high], a_list[start]
    return high # high最终就是pivot的位置，high与start交换前，属于较小的那个，与start交换后，属于中间那个

def quick_sort(array, start, end):
    """https://stackabuse.com/quicksort-in-python/
    """
    if start >= end:
        return

    p = partition(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)

array = [29,99,27,41,66,28,44,78,87,19,31,76,58,88,83,97,12,21,44]

quick_sort(array, 0, len(array) - 1)
print(array)


print(">>> 找到最小的k个数")
# 改写一下上面的算法，目的是对每次quick_sort做出一个选择


def quick_find_k(array, start, end, k):
    """https://stackabuse.com/quicksort-in-python/
    """
    if start >= end:
        return

    p = partition(array, start, end)
    if p == k:
        return array[: k]
    elif p < k:
        quick_find_k(array, start, p-1, k)
    else:
        quick_find_k(array, p+1, end, k)

array = [29,99,27,41,66,28,44,78,87,19,31,76,58,88,83,97,12,21,44]


print(quick_find_k(array, 0, len(array) - 1, 5))

print(">>> 利用heap找到最小的k个数")

# 小根堆，大小固定，不断的pop进去数字，最后打印heap
import heapq

a_heapq = []
for item in array:
    heapq.heappush(a_heapq, item)
print(a_heapq[: 5])

print(">>> 寻找出现次数超过一半")
#很典型就是找到 len / 2就好了
#前面一半，中间，后面一半

