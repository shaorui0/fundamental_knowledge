
print("写道字符串处理热热身")


# 好蠢！是可以进行预处理的！分层次解决问题，不要想着将一个过程整合到一个函数里面，那样，会很麻烦！

# 过程一：去重，去掉首尾多余的字符&/=

def delete_repeat_substring(s):
    # 去掉头部
    # 边界检查 todo
    a_list = list(s)
    i = 0
    k = 0
    while i < len(s) and s[i] in ['=', '&']:
        i += 1
    # 此时i指向第一个字母
    while i < len(a_list):
        if a_list[i].isalpha():
            a_list[k] = a_list[i]
            k += 1
            i += 1
        elif a_list[i] in ['&', '=']:
            if i != 0 and a_list[i] != a_list[i - 1]:
                # 第一个字符，继续赋值
                a_list[k] = a_list[i]
                k += 1
                i += 1
            else:
                i += 1
    # 去掉尾部的？有没有必要？
    result = ''.join(a_list[:k])
    return result
    # pass
    index = len(result) - 1
    while result[index] in ['&', '=']:
        index -= 1
    
    return ''.join(a_list[:index+1])
s = "&ag=cd=sv&&da=&dc&&&&dav=dwq&&"
print(delete_repeat_substring(s))


# 过程二：在判断，就不需要while只需要if了
def parse_str(s):
    print("parse_str", s)
    # 边界检查 TODO
    i, j = 0, 0
    cur_list = list()
    while i < len(s) and j < len(s):
        #print('>>> ', s[j], j)
        while s[j].isalpha():
            j += 1
        # 此时不是字母
        if s[j] == '=':
            substr = s[i:j]
            cur_list.append(substr)
            j += 1
            i = j
        elif s[j] == '&':
            substr = s[i:j]
            cur_list.append(substr)
            # 处理list
            if "" in cur_list or len(cur_list) != 2:
                print("error", cur_list)
            else:
                print(cur_list)
            j += 1
            i = j
            cur_list = list()
parse_str(delete_repeat_substring(s))

# 以上是腾讯后台实习的一个算法题，这种字符串题如何思考不清楚，实现起来会很复杂。
# 对于程序设计而言，层次化的思考是很重要的思考方式。**每个函数只做一件事**不是说说而已。
# 对于这道题，如果一开始同时处理『重复运算符』和『映射子串』的问题，代码会写的很麻烦，还容易写错。边界条件太多，心智负担过大。

