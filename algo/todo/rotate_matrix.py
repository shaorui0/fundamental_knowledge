def rotate(matrix, left, right, top, bottom):
    n = len(matrix)
    i = top
    for j in range(left, right):
        print(n, i, j)
        matrix[i][j], matrix[n - j - 1][i], matrix[n - i - 1][n - j - 1], matrix[j][n - i - 1] \
            = matrix[n - j - 1][i], matrix[n - i - 1][n - j - 1], matrix[j][n - i - 1], matrix[i][j]
    return matrix

a_list_of_list = [
    [1,3,4,5],
    [11,33,44,55],
    [111,333,444,555],
    [1111,3333,4444,5555],
]
print(rotate(a_list_of_list, 1, 2, 1, 2))

# 还可以考虑成“块”状旋转，leetcode
# https://leetcode-cn.com/problems/rotate-matrix-lcci/solution/xuan-zhuan-ju-zhen-by-leetcode-solution/

# 上面是一种层次思维，其实可以取巧，有点类似前半部分翻转一次，后半部分翻转一次，整体再翻转一次。
# 水平翻转 + 对角线翻转


# ------------------
print("https://leetcode-cn.com/problems/shun-shi-zhen-da-yin-ju-zhen-lcof/, 顺时针打印数组")