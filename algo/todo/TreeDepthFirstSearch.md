# 8. Tree Depth First Search

## 公共父节点
https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/solution/
输入：
1. root
2. first_node, second_node


输出

3. parent

怎么找？肯定是递归了，但是递归式怎么写？

- 深度可能不一样
- 你肯定是不能向上找
- 


找模式，能够找到什么样的模式？
无非就是几种遍历方法，前中后序

抽象成数学方法

1. 你的问题是什么？
2. 迭代的本质是什么？或者说为什么要有一个树这种数据结构？为了查找效率更高
    一切的一切归根结底都是（更好的）读、写

理解迭代

1. 找到节点，返回一些信息给递归上层
    - 典型的，比如我找到了
    - 递归的本质，看起来是从上到下，但本质还是从下往上 --- 栈（先处理谁后处理谁？）


所以，抽象出来，这题是要干什么？
    1. 要么左右各找到了结果，处理两个结果的返回值


1. 首先：两种情况，一个节点自身为parent。两个节点分别在parent 的两边
    - 抽象成数学表达式就是：f(left) && f(right)
    - (f(left) || f(right)) && (x == left || x == right)

2. 写出简单的伪代码
输出是一个parent节点，如何保存？用闭包

def driver()
    parent = None
    dfs(root, first, second):
        # 边界检查
        判断 root 与 first/second 的对比，是否为同一节点
        is_left_parent = 
        is_right_parent = 
        found_in_left = dfs(root.left, first, second)
        found_in_right = dfs(root.left, first, second)
        对比结果：
        if (found_in_left && found_in_right) || (...):
            parent = root
        
        return 是否找到了某个节点？或者就是root 本身？
https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/solution/er-cha-shu-de-zui-jin-gong-gong-zu-xian-by-leetc-2/


TODO 如何想到这个解法的？

## 方案二

1. 通过栈的性质，
保存一直向上走的过程
获取len
长的先走，短的再走。。。这就是过程了

或者再加一个空间换时间，比如 一个hash记录visited


1. 迭代遍历，记录所有节点的父节点，相当于增加一个向上的指针
    - 如何增加一个向上的指针？每访问一个节点，将他的left/right 指向它即可
2. 增加之后，就可以从该节点往上走了
    - 往上走的过程再进行 visited 记录


TODO 如何想到这个解法的？、、、、

1. 逆序对

分析题目

问题是什么？
找到数组中所有的逆序对，
    - 逆序也是有序
    - 典型的暴力解法是On2
    - 能不能减少到nlogn？
    如果前后两个数组有序了，那么结果会不会变？
- 归根结底是什么？归并排序？左右两个

https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/solution/shu-zu-zhong-de-ni-xu-dui-by-leetcode-solution/

贡献，怎么会 想到这个方法的？逻辑链