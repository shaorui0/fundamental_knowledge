# 如果不排序，必须用hash

# 2sum，直接hash，实践效率更高，不然就是排序+二分
# 3sum，排序 + 剩余2sum

# https://leetcode.com/problems/3sum-closest/discuss/7871/Python-O(N2)-solution

# 注意，排序则直接可以使用双指针，简单直接
# 可能2sum还不需要，但是3sum，我感觉是必要的了