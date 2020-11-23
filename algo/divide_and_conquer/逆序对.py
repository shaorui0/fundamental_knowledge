
# 逆序对

本质是分治
先算两半的逆序对，再算跨区域的逆序对
```
left_part = foo(0, mid, nums, tmp)
right_part = foo(...)
total = left_part + right_part

while l <= mid and j <= r:
    if nums_i < nums_j:
        ...
    else:
        ...
    pos

# 剩下的，可能是i没到头，可能是j没到头

for k in range(i, mid+1):

for k in range(j, r+1)

# 最后还要注意将有序数组保存到原数组上面
```


