
def find_non_repeat_left_index(a_list, left, right, hash_table):
    repeat_value = a_list[right]
    i = left
    for i in range(left, right):
        hash_table.remove(a_list[i])
        if a_list[i] == repeat_value:
            break
    return i+1, hash_table

def lengthOfLongestSubstring(a_list):
    # 边界检查
    hash_table = set()
    # 如果right指针所指与left不同，right向右走
    left = 0
    right = 1
    max_len = 1
    result = ""
    hash_table.add(a_list[left])
    while left < len(a_list) and right < len(a_list):
        if a_list[right] not in hash_table:
            hash_table.add(a_list[right])
            right += 1
            if max_len < (right - left):
                max_len = right - left
                result = a_list[left: right]
        # 注意记录最大长度
        # 注意更新 hash table
        else:
            left, hash_table = find_non_repeat_left_index(a_list, left, right, hash_table)
    # 如果相同，left right 找到第一个不同的left
    return max_len, result
a_list = "abcdbabcde"
print(lengthOfLongestSubstring(a_list))