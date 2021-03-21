# 输入是什么

# 一些重量
# 一些价值

# 重量只能装到最大为止
# 价值尽可能的大
# 输出是：可能装的最大价值

# volume = [1,2,3,4]
# worth = [2,4,4,5]
# max_volume = 5
worth = [60, 100, 120] 
volume = [10, 20, 30] 
max_volume = 50
# # 初始化一个二维DB
# # 选0，不选0
dp = []
for i in range(len(volume)):
    dp.append([0 for i in range(max_volume)])
# 如何初始化一个二维数组？指定大小？
# print(dp)
# dp[0][0] = 0
# dp[0][volume[0]] = worth[0]
# print(dp)
# 怎么算？怎么推？
for i in range(len(volume)):
    for v in range(max_volume): # 这里相当于最大只能是49（但是我只管能不能装进去啊）
        if v >= volume[i]:
            print(dp[i-1][v - volume[i]] + worth[i], dp[i-1][v])
            dp[i][v] = max(dp[i-1][v - volume[i]] + worth[i], dp[i-1][v]) # 选与不选
        else:
            dp[i][v] = dp[i-1][v] 

print(dp)

# 理解dp数组的含义
# TODO 优化成一维呢？
# 首先要知道是如何更新的

# def knapSack(W, wt, val, n): 
#     K = [[0 for x in range(W + 1)] for x in range(n + 1)] 
  
#     # Build table K[][] in bottom up manner 
#     for i in range(n + 1): 
#         for w in range(W + 1): 
#             if i == 0 or w == 0: 
#                 K[i][w] = 0
#             elif wt[i-1] <= w: 
#                 K[i][w] = max(val[i-1]  
# + K[i-1][w-wt[i-1]],  K[i-1][w]) 
#             else: 
#                 K[i][w] = K[i-1][w] 
  
#     return K
  
# # Driver program to test above function 
# val = [60, 100, 120] 
# wt = [10, 20, 30] 
# W = 50
# n = len(val) 
# print(knapSack(W, wt, val, n)) 

