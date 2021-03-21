# 进制转换


## 先写个快速幂

### 递归

# 1. 注意尾递归优化
# 尾递归


# 1. 静态语言一般是编译器优化了
# 2. 主要思想是通过系数传递替代底层递归结果依赖
# 3. 同时由于参数直接记录了结果而不是依赖递归过程，节省了很多栈空间（时间效率没什么变化）

# https://stackoverflow.com/questions/33923/what-is-tail-recursion
# https://www.zhihu.com/question/20761771/answer/20672305

def pow(a, b):
    # 递归出口
    if b == 0:
        return 1
    if b == 1:
        return a

    # 递归式
    if b % 2 == 1:
        return pow(a*a, b//2) * a
    else:
        return pow(a*a, b//2)

print(pow(2, 11))


# 15进制 转为 7 进制转换

# 第一阶段，往十进制转
def tran_to_ten(base, nums):
    # 边界检查
    sum = 0
    for i in range(len(nums)):
        power = len(nums) - i - 1
        x = nums[i]
        cur = x * pow(base, power)
        sum += cur
    return sum
print(tran_to_ten(15, [13, 12, 0, 5]))

# 第二阶段从十转
def tran_from_ten(base, num):
    a_list = []
    cur = num
    while cur != 0:
        x = cur % base
        a_list.append(x)
        cur = cur // base
    result = []
    for _ in range(len(a_list)):
        result.append(a_list.pop()) # python 没有现成数据结构，只有一个pop()函数
    return result

print(trans_num_to_list(7, tran_to_ten(15, [13, 12, 0, 5])))
