# 如何使用leetcode？

[别再埋头刷LeetCode之：北美算法面试的题目分类，按类型和规律刷题，事半功倍 - 穷码农的文章 - 知乎](https://zhuanlan.zhihu.com/p/89392459)

1. Pattern: Sliding window，滑动窗口类型经典题目：Maximum Sum Subarray of Size K (easy)Smallest Subarray with a given sum (easy)Longest Substring with K Distinct Characters (medium)Fruits into Baskets (medium)No-repeat Substring (hard)Longest Substring with Same Letters after Replacement (hard)Longest Subarray with Ones after Replacement (hard)
    - 通常是前后两个指针在不同条件下进行向右移动，right_index快。
    - 经典题目是『最长不重复子串』。
    - 典型的框架是：
    ```
    for left_index in [0, n-1]:
        if xxx:
            do something
        
        while yyy:
            do something else
            
            right_index++
        update final result
    ```

2. Pattern: two points, 双指针类型经典题目：Pair with Target Sum (easy)Remove Duplicates (easy)Squaring a Sorted Array (easy)Triplet Sum to Zero (medium)Triplet Sum Close to Target (medium)Triplets with Smaller Sum (medium)Subarrays with Product Less than a Target (medium)Dutch National Flag Problem (medium)
    - 滑动窗口的一种。主要包括：同向移动、交叉向内移动（一般是 **ordered** list）
    - 经典题目是：Remove Duplicates

3. Pattern: Fast & Slow pointers, 快慢指针类型经典题目：LinkedList Cycle (easy)Start of LinkedList Cycle (medium)Happy Number (medium)Middle of the LinkedList (easy)
    - 经典题目：判断循环链表以及进一步的找到循环链表循环点
    ```
    1. 判断循环，会在圈内某个点相遇
    2. 重置一个指针，同速向前，会在某个时间一起到达圈的起点（这块可能需要一个证明）
    ```

4. Pattern: Merge Intervals，区间合并类型经典题目：Merge Intervals (medium)Insert Interval (medium)Intervals Intersection (medium)Conflicting Appointments (medium)
    - 经典题目：一些交叉的一维范围进行一些合并：[1,3] + [2,4] => [1, 4]

5. Pattern: Cyclic Sort，循环排序经典题目：Cyclic Sort (easy)Find the Missing Number (easy)Find all Missing Numbers (easy)Find the Duplicate Number (easy)Find all Duplicate Numbers (easy)
    - 448. Find All Numbers Disappeared in an Array
    - 典型的思路（trick）是**原地置负进行标记，在不丢失原来的信息的情况下增加新的信息**
    - **经典的解法**是通过不断迭代数组，直到全部放到正确的位置
    ```py
    def cyclic_sort(input_list):
        idx = 0;
        while idx < len(input_list):
            if input_list[idx] != input_list[input_list[idx] - 1]:
                # Swap, notice must change "input_list[input_list[idx] - 1]" first
                tmp = input_list[input_list[idx] - 1]
                input_list[input_list[idx] - 1] = input_list[idx] 
                input_list[idx]  = tmp
            else:
                idx += 1
        # check result list
    ```
6. Pattern: In-place Reversal of a LinkedList，链表翻转经典题目：Reverse a LinkedList (easy)Reverse a Sub-list (medium)Reverse every K-element Sub-list (medium)
    - 典型链表翻转注意手动尝试中间的过程，`HEAD->2->1->3->4->null`
7. Pattern: Tree Breadth First Search，树上的BFS经典题目：Binary Tree Level Order Traversal (easy)Reverse Level Order Traversal (easy)Zigzag Traversal (medium)Level Averages in a Binary Tree (easy)Minimum Depth of a Binary Tree (easy)Level Order Successor (easy)Connect Level Order Siblings (medium)
    - Queue
8. Pattern: Tree Depth First Search，树上的DFS经典题目：Binary Tree Path Sum (easy)All Paths for a Sum (medium)Sum of Path Numbers (medium)Path With Given Sequence (medium)Count Paths for a Sum (medium)
    - 本质和**permutations**类似（dfs，分支if left/if right 和 for i in list）
    - 主要理解dfs怎么工作
    - 最关键的，是否需要push/pop，何时push/pop。
9. Pattern: Two Heaps，双堆类型经典题目：Find the Median of a Number Stream (medium)Sliding Window Median (hard)Maximize Capital (hard)
    - 双堆一般是维护一大一小，这样**两个堆的堆顶**是**中间的两个数**，一般**动态**找index/2的树

10. Pattern: Subsets，子集类型，一般都是使用多重DFS经典题 目：Subsets (easy)Subsets With Duplicates (easy)Permutations (medium)String Permutations by changing case (medium)Balanced Parentheses (hard)Unique Generalized Abbreviations (hard)
    - 理解多重DFS
    - 可迭代 + push/pop，也可以分支多次dfs（无需push/pop）
    - 使用index控制当前处理的下标
    - 保持要记录的数据，持续更新。通常是 `part_list`, `current_sum`, `total_sum`

11. Pattern: Modified Binary Search，改造过的二分经典题目：Order-agnostic Binary Search (easy)Ceiling of a Number (medium)Next Letter (medium)Number Range (medium)Search in a Sorted Infinite Array (medium)Minimum Difference Element (medium)Bitonic Array Maximum (easy)
    - 经典题型是**多次方程函数求解**，思路是**逼近误差值**，和开方（不一定是二次方，三次方同样是二分，**二分的本质是每次排除一半不可能的情况使得复杂度降低到log(n）** 思路一致。
12. Pattern: Top ‘K’ Elements，前K个系列经典题目：Top ‘K’ Numbers (easy)Kth Smallest Number (easy)‘K’ Closest Points to the Origin (easy)Connect Ropes (easy)Top ‘K’ Frequent Numbers (medium)Frequency Sort (medium)Kth Largest Number in a Stream (medium)‘K’ Closest Numbers (medium)Maximum Distinct Elements (medium)Sum of Elements (medium)Rearrange String (hard)
    - heap / quick sort
        - 快排思想本质是每次找到的pivot的左右两部分处于它们应该在的位置，然后**分治**处理
13. Pattern: K-way merge，多路归并经典题目：Merge K Sorted Lists (medium)Kth Smallest Number in M Sorted Lists (Medium)Kth Smallest Number in a Sorted Matrix (Hard)Smallest Number Range (Hard)
    - 思路直观，编程不难，主要是要有并发的思维。
14. Pattern: 0/1 Knapsack (Dynamic Programming)，0/1背包类型经典题目：0/1 Knapsack (medium)Equal Subset Sum Partition (medium)Subset Sum (medium)Minimum Subset Sum Difference (hard)
    - DP的核心是空间换时间 + **状态转移**
    - 具体到**背包问题**的核心是，对『选与不选』某个物品，传递下一层级的状态
    - 比较**耗空间**的方式是**二维数组**，某些问题可以优化到一维。思路是观察二维数组的实现，行状态（i）的转移，只与上一行有关（i-1），那这里是可以省略行信息的。
    - **初始状态**肯定是所有的都不选和为0的情况是一定会出现的（True），以及确定第一个dp[0][nums[0]] = True
        - 同时，优化成一维以后，注意**从大到小**计算。因为dp[j]的状态依赖dp[j - cur_num]，但是从小到大的话，dp[j - cur_num]不再是上一行的状态，而是这一行的状态（**内层循环非外层循环**）。
15. Pattern: Topological Sort (Graph)，拓扑排序类型经典题目：Topological Sort (medium)Tasks Scheduling (medium)Tasks Scheduling Order (medium)All Tasks Scheduling Orders (hard)Alien Dictionary (hard)
拓扑排序是说输入一些依赖关系，输出一棵或多棵树（Airflow DAG）
    - 回忆一下图的性质，同时规定了有向
    - 输入：图的两种表达是二维列表 or 二维链表
    - 输出：一般是排序后的结果, [1, [2,3], 4]
    - 具体的操作过程，就是：
        - 从无输入的点开始（入度=0），得到它的所有下一级
        - 下一级的入度都-1
        - 将所有的0导入到0度列表（栈 or 队列）
        - 选取下一个0度节点, again
        ```
        func topologic_sort(graph):
            init stack
            for node in graph:
                if indegree of node is 0:
                    push to stack
            while stack is not empty:
                pop item in stack
                visit the item
                for next_node in item.total_next_nodes:
                    reduce 1 on next_node
                    if current indegree of next_node is 0:
                        push current node to stack
            if all of node have visited:
                return True
            else:
                return False
        ```