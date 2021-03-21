# 树上BFS

1。 Zigzag
2. 找到每一层最左边的数

关于换层，能不能有一个比较“简单”的方法？

# 树上BFS

每层


a_queue = queue()

能否记录层数？

如果输入是链表
如果输入书数组

# 边界检查
a_queue.put(root)
while a_queue is not empty:
    cur_node = a_queue.pop()
    # 准备处理这层的数（比如第一层）
    cur_size = len(queue)
    for _ in range(size):
        if left: 
            a_queue.put(left)
        if right
            a_queue.put(right)

```
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        import queue
        result = []
        if root is None:
            return result
        q = queue.Queue()
        q.put(root)
        
        is_left_to_right = True
        while not q.empty():
            cur_size = q.qsize()
            cur_nodes = [None for _ in range(cur_size)]
            for i in range(cur_size):
                cur_node = q.get()
                index = i if is_left_to_right else cur_size - i - 1
                cur_nodes[index] = cur_node.val
                
                if cur_node.left:
                    q.put(cur_node.left)
                if cur_node.right:
                    q.put(cur_node.right)
            is_left_to_right = not is_left_to_right
            result.append(cur_nodes)
        return result
```
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/submissions/

## 注意

1. 我一直想的是怎么能够保存“层”这个概念（之前面试也面到过）
    - 比如再加一个list数据结构保存当前层的所有数，但好像和queue的功能重合了，我明明只用保存size就够了
    - 我的目的就是“精确”知道每一层有多少个数
        - 本质就是内层遍历多少次，有个“界限”的概念在那里

2. 关于zigzag的问题，可以搞个flag，然后初始化一个list，有时候倒序放入有时候正序放入。