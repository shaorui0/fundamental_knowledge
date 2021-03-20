# 13. K-way merge
https://leetcode-cn.com/problems/merge-k-sorted-lists/solution/he-bing-kge-pai-xu-lian-biao-by-leetcode-solutio-2/

k 路归并

def merge_two(first, second):
    if second_link is None:
        # 奇数个link list
        return first
    
    # 合并两个



def merge_all(a_list_of_link_list_header):
    """
    每次对list里面的链表迭代一次，返回一系列合并后的链表
    """
    results = []

    # 边界检查
    i = 0
    # 这只迭代了一次
    while i < len(a_list_of_link_list_header):
        first_link = a_list_of_link_list_header[i]
        second_link = a_list_of_link_list_header[i+1] if i+1 < len(a_list_of_link_list_header) else None
        result_link = merge_two(first_link, second_link)
        i += 2
        results.append(result_link)

    return results

def merge_k_sorted_list(a_list_of_link_list_header):
    cur_list = a_list_of_link_list_header
    while True:
        results = merge_all(cur_list)

        if len(results) == 1:
            break
        cur_list = results
    
    return results[0]

## 还有一种方法，heap sort
本质就是n个元素，逐个排序出来

这种迭代的方式总是觉得写代码太麻烦？


### 关于递归与迭代的问题

1. 递归写起来代码比较简单，迭代则是思路与人脑同步

1. 本质是分治，所以可以用递归
merge2(merge(), merge()) # 

两个函数交替递归，你能理解其中的含义吗？感觉设计还是十分精巧的
怎么思考迭代？

画图理解递归，两个函数交替递归，如何理解这个过程。
递归还是画图比较简单


1. 如何发起？
2. 具体的过程是什么？
 

典型的分治：

分：merge
治：mergeTwo

TODO picture

驱动程序，merge(xxx, left, right)
if left == right:   return 具体的list（栈的底部）


爆栈问题，怎么解决？（完全可以写上去）

画一个图吧

# 迭代的话，通过index管理比较好 
不需要额外的复制或者创建空间
https://leetcode-cn.com/problems/merge-k-sorted-lists/solution/4-chong-fang-fa-xiang-jie-bi-xu-miao-dong-by-sweet/


接口：

def merge_k_sorted_list(a_list_of_link_list_header):
    # 边界检查

    n = len(a_list_of_link_list_header)
    return merge(a_list_of_link_list_header, 0, n-1)


def merge(a_list_of_link_list_header, left, right):
    # 递归出口
    if left == right:
        return a_list_of_link_list_header[list]
    if left > right:
        return None

    # 递归式
    mid = (left + right) // 2
    return merge_2_list(merge(a_list_of_link_list_header, left, mid), merge(a_list_of_link_list_header, mid+1, right))

def merge_2_list(link_list_1, link_list_2):
    # 处理一下 None 的边界
    if None:
        reutnr link_list_1
    dummy = Node()
    first_index = 
    second_index = 
    while first and second:
        first_value
        second_value
        if first_value:
            dummy.next = first_index
            first_index = first_index.next
        else:
            ...
    
    # 处理一下剩余的
    if first_index:
        pass

    if second_index:
        pass

# 优先队列

1. 固定大小的heap（其实通过每次push + pop 维持固定大小，直到某个list会走到最后）
    2. 所有的first push 进去

2. 每次找一个top，pop + push(top.next)

典型的k路归并没什么说的，关键是如何能够想到优先队列的？
这是个什么场景？ 排序的场景
之前的两个链表合并只需要对比两个数，那么k个链表呢？对比k个数典型的太麻烦，本质上我需要的是什么？我并不需要把这k个node完全排序，而只需要找到最大的一个数就可以了！一次找一个！
所以，本质是一个简单问题的复杂化， 但是思想还是不变。
之前的两个链表对比并不是比出个完全大小，而是只要找到“最值”！


