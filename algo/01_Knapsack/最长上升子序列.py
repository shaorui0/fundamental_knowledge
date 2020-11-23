# 最长上升子序列

# 简单的动态规划就可以做，典型的使用
init dp[all] = 1
for i in [0, n-1]:
    for j in [0, i]:
        dp[j] = max(dp[i], dp[j]+1); nums[i] > nums[j]

# 思路，长度为i的末尾最小值

贪心，顶一个数组，d[i]表示长度为i的最大上升子序列的末尾元素的最小值
值要尽可能的小，同时又要尽可能的长
```
for x in nums:
    if x > d[-1]:
        d.append(x)
    else:
        # 二分查找找到x应该插入的地方
        left, right = 0, len_nums - 1
        loc = right
        while left <= right:
            mid = (left + right) // 2
            if d[mid] >= n:
                loc = mid # 分别论证，当前数如果==d_mid，可以放入；当前数如果 < d_mid，也可以放入（相当于更新了）
                right = mid - 1
            else:
                left = mid + 1
        d[loc] = x
```
