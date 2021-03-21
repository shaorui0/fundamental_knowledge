print("448. Find All Numbers Disappeared in an Array")
# 循环排序是不断交换，直到它找到属于它的位置（有一个点已经到了“最终位置”）
a_list = [4,3,2,7,8,2,3,1]
def cyclic_sort(a_list):
    idx = 0;
    while idx < len(a_list):
        print(idx, a_list)
        if a_list[idx] != a_list[a_list[idx] - 1]:
            # 相等说明不能再交换了，数字已经“就位”了
            # 迭代直到所有的数字到位，才进行下一轮
            # 注意这里的交换问题，可能产生死循环。a_list[a_list[idx] - 1]依赖a_list[idx]的值。
            tmp = a_list[a_list[idx] - 1]
            a_list[a_list[idx] - 1] = a_list[idx] 
            a_list[idx]  = tmp
        else:
            idx += 1
    print(a_list)
    for i, x in enumerate(a_list):
        if i != a_list[i]-1:
            print("index =", i, "value =", x)

cyclic_sort(a_list)