
方案一：变量携带 record_list，无需pop，但多了很多次的 copy
```py
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: List[List[int]]
        """
        result = []
        def dfs(head, cur_sum, target, record_list):
            if not head:
                return
            total = cur_sum + head.val
            record_list.append(head.val)
            if head.left is None and head.right is None and total == target:
                print(record_list)
                result.append(record_list[:])


            dfs(head.left, total, target, record_list[:])
            #record_list = record_list[:-1]

            dfs(head.right, total, target, record_list[:])
            #record_list = record_list[:-1] # 什么情况pop？
            #record_list.pop() # 为什么pop，不pop会怎么样

        dfs(root, 0, sum, [])
        return result
```

方案二：全局的 record_list，需要对每次push的节点进行pop，符合直觉
```py
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    # push/pop用于配合全局record_list的更新
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: List[List[int]]
        """
        result = []
        record_list = []
        def dfs(head, cur_sum, target):
            print(record_list) # 打印一下，很容易看出来dfs是怎么工作的，push/pop用于配合全局record_list的更新
            if not head:
                return
            total = cur_sum + head.val
            record_list.append(head.val)
            
            if head.left is None and head.right is None and total == target:
                #print(record_list)
                result.append(record_list[:])


            dfs(head.left, total, target)
            dfs(head.right, total, target)
            
            record_list.pop()

        dfs(root, 0, sum)
        return result
```

注意事项：

1. 内部有一个返回点与其到叶子节点判断，不如到叶子节点的下一层`None`判断，这个可以无脑返回。

2. 如果是外层的`record_list`，则需要管理 push 和 pop，如果是逐渐向内传递 `part_record_list`，则不需要pop，但潜在的会有**复制**过程带来的效率损失。

3. 其他的分支（比如，还没到叶子，但是和已经超过 target），是可以『剪枝』的，但是一般为了减小代码的复杂度，初始阶段不用。）