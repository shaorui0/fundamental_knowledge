# 关于树上DFS

## 最近公共祖先
0. 分为两种情况，这没话说
    - 一种是自己本身就是祖先
    - 一种是两者有共同的祖先
1. 怎么想到的这个数学表达式？
    - 递归的本质是什么？
        - 数学归纳法
    - 树的递归查找本质还是查找
    - 首先我得理解输入，三个指针，root、first、second
    - 我至少得找到这两个节点，然后将信息向上传递吧？
        - 传递什么样的信息？是否找到？
            - 两个儿子都找到了
        - 怎么理解这个向上传递的含义？
            - 如果找到一个儿子，就return
            - 或者cur_root本身就是其中一个
            return left_son || right_son || (pleft.value == root.value || pright.value == root.value)
            left_son 是传过来的信息，首先肯定是一个递归接口
            `left_son = dfs(root.left, first, second)`

2. 本质在考什么？DFS是什么东西？
    - 找祖先这回事，本质是找parent...
        - 要么，通过递归向上传递，要么，通过指向parent的指针进行迭代（如果没有，可以预先进行一次递归）

##  path sum
https://leetcode-cn.com/problems/path-sum-ii/description/

> 找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。

找到所有满足和的结果

能想到什么方法？

递归找， 传递当前和的信息，继续向下，看能不能走，能走就保存，不能走就算了。其实思路还是很清晰的

1. 考虑前中后序
2. 考虑抽象过程

def dfs(root, sum):
    result = []
    def foo(root, sum, temp_sum, temp_list):
        # temp_list保存了以当前root为叶子的通往真root的路
        cur_list = temp_list[:]
        cur_list.append(root.value)
        # 如果当前为叶子节点
            # 判断temp sum 与 sum
                # 如果等于，加入到result，
                
                # 如果不等于
        # 如果当前不为叶子节点
            # 判断temp sum 是否小于 sum，if 小于，继续往下
                return foo(root.left, sum, temp_sum-root.value, cur_list)
                return foo(root.left, sum, temp_sum-root.value, cur_list)
            # 如果大于等于
                # return 

整理一下逻辑，看看是否需要修改？