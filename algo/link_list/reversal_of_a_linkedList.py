
print("In-place Reversal of a LinkedList")

def print_link_list(head_node):
    tmp = head_node
    while tmp is not None:
        print(tmp, tmp.data)
        tmp = tmp.next # 链表要注意更新
print_link_list(head)
def reverse_link_list(head_node):
    # 边界
    if head_node is None:
        return None
    # 以 head-2-1-3-4-null进行测试（不要以太特殊的情况进行测试）
    get_next_pointer = head_node.next
    while get_next_pointer.next is not None:
        tmp_pointer = get_next_pointer.next
        head_next = head_node.next

        head_node.next = tmp_pointer
        get_next_pointer.next = tmp_pointer.next
        tmp_pointer.next = head_next
        print_link_list(head_node) # for test
    return head_node

print_link_list(reverse_link_list(head))
