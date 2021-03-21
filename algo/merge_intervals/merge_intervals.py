
print("Merge Intervals")
#input: [1,3], [2,4], [3,8], [4,6], [9, 10]
#output: [1, 8], [9, 10]
# 思路，迭代对比前后两个list，对list的两端进行对比
# 注意，两个list合并，会有四种情况，但其中两种本质是相同的，只是换了个边。为了避免复杂度，应该先对list[0]进行排序

# current[0] > result[-1][0] >= result[-2][1]
def merge_intervals(intervals):
    # 排序
    intervals.sort(key=lambda x:x[0])
    i = 0
    result = []
    for current_list in intervals:
        # 排序后，只可能与result[-1]的list进行对比，
        #if result is empty or result[-1][1] < current_list[0]:
        print(result)
        if len(result) == 0 or result[-1][1] < current_list[0]:
            result.append(current_list)
            #push current list to result
        else: # 有交集（覆盖或交叉）
            result[-1][1] = max(current_list[1], result[-1][1]) # 右边界扩大，注意可能是包含关系

    return result
print(merge_intervals([[1,3], [2,4], [3,8], [4,6], [9, 10]]))
