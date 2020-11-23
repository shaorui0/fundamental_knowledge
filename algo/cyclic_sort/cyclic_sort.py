print("448. Find All Numbers Disappeared in an Array")
a_list = [4,3,2,7,8,2,3,1]
def cyclic_sort(a_list):
    idx = 0;
    while idx < len(a_list):
        print(idx, a_list)
        if a_list[idx] != a_list[a_list[idx] - 1]:
            # 迭代直到所有的数字到位，才进行下一轮
            # 注意这里的交换问题，可能产生死循环。a_list[a_list[idx] - 1]依赖a_list[idx]的值。
            tmp = a_list[a_list[idx] - 1]
            a_list[a_list[idx] - 1] = a_list[idx] 
            a_list[idx]  = tmp
        else:
            idx += 1

    for i, x in enumerate(a_list):
        print(i, x)
        if i != a_list[i]-1:
            print(x)

cyclic_sort(a_list)