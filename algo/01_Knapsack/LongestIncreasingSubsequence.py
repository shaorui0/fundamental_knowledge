# 最长上升子序列

# 简单的动态规划就可以做，典型的使用
# dp 数组中保存什么东西？当前数字为尾的最长子序列是多少？同时还要满足 f(right) = max(f(left)) + 1 and a_right > a_left
nums [2,3,1 .. 4]
dp   [1,2,1 .. 3]

init dp[all] = 1
for i in [0, n-1]:
    for j in [0, i]:
        dp[j] = max(dp[i], dp[j]+1); nums[i] > nums[j]

有点暴力求解的意思
# 思路，长度为i的末尾最小值

# 贪心，定一个数组，d[i]表示长度为i的最大上升子序列的末尾元素的最小值
# 值要尽可能的小，同时又要尽可能的长

d = [0 for i in range(len_nums + 1)]
for x in nums:
    if x > d[-1]:
        d.append(x)
    else:
        # 二分查找找到x应该插入的地方
        left, right = 0, len_nums - 1
        loc = right
        while left <= right:
            mid = (left + right) // 2
            if d[mid] >= x: # 当前数可以插入d[]中，需要被更新
                loc = mid # 分别论证，当前数如果==d_mid，可以放入；当前数如果 < d_mid，也可以放入（相当于更新了）
                right = mid - 1
            else:
                left = mid + 1
        d[loc] = x # 插到应该保存的地方

return # 从后向前找到第一个不为0 的数