
print("分割等和子集")
# 背包问题的核心是什么？选与不选，然后会有一个退化状态转移的问题
# dp[i][j] = 
# - 选：dp[i-1][j-nums[i]] 
# - 不选：dp[i-1][j]

# 核心是找到状态转移方程，以及规定好dp数组的含义，i、j，值...
# 条件：j于nums[i]的比较
# - j < nums[i]，没必要选，选不选都不能满足，直接『状态』发生转移

# 边界条件
# len<2, 和为基数，
# dp[i][j]，n * target

# TODO 一维数组

# dp[0][j]什么含义？选第0个能否得到何为j？
# 也就是说初始条件是什么？
# 显然，dp[i][nums[i]] = True, 其他都是False
# 以及，所有的dp[i][0] = True, 表示我不选每一个，都等于0
def canPartition(a_list):
    # 边界
    if a_list is None or a_list == []:
        return False
    length = len(a_list)
    total = 0
    for x in a_list:
        total += x
    if length < 2 or total % 2 != 0:
        return False
    
    target = total // 2 # 找到部分数字和为target即可
    # dp, len * total/2
    dp = [[0] * (target + 1) for _ in range(length)]

    # init
    for i in range(length):
        dp[i][0] = True # 都不选
    
    dp[0][a_list[0]] = True # 起点

    # 迭代判断所有的i，j
    for i in range(1, length):
        cur_num = a_list[i]
        for j in range(1, target+1):
            if j >= cur_num: # 这里的比较出现了错误，要理解下标是在干什么
                dp[i][j] = dp[i - 1][j] | dp[i - 1][j - cur_num] # 状态转移：不选 | 选
            else:
                dp[i][j] = dp[i - 1][j] # 当前值已经超过了target

    # 然后最终结果在dp[i][target] = True的所有i？测一下
    print(dp)
    return dp[length-1][target] # 为什么是最后一个，对所有的数字都做完决策以后，有没有等于target的（最后一行的意思是，给n个数进行选择，有没有可能等于下标？）
canPartition([1,2,3,6])

# 可能时间长了会忘记的点：
# 理解状态转移四个字（dp是什么？）
# 背包问题是一种很典型的题目
# 处理if-else（j >= num）时，注意真实的含义
