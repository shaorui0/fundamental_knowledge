# python数据结构的底层实现


## dict

[implement a dict](https://www.jianshu.com/p/68db5cff4872)

无序k-v对，典型的hash table（c++还分ordered和unordered）

### bucket如何指定？

- offset，hash(hashable)%k
- 通过二进制的hash值进行取bucket，从右向左`110`, `000`, etc.

```py
>>>dic['name'] = '张三'
>>>bin(hash('name'))
'0b101011100000110111101000101010100010011010110010100101001000110'
```

### 键必须是可hash的

当存在场景想使用list做key时，可以用tuple代替。
只有固定长度类型才能做key


### 动态扩容

迭代dict时注意不要进行update和del，当然list也不行。


## list

https://stackoverflow.com/questions/3917574/how-is-pythons-list-implemented

```cpp
typedef struct {
    PyObject_HEAD
    Py_ssize_t ob_size;

    /* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
    PyObject **ob_item;

    /* ob_item contains space for 'allocated' elements.  The number
     * currently in use is ob_size.
     * Invariants:
     *     0 <= ob_size <= allocated
     *     len(list) == ob_size
     *     ob_item == NULL implies ob_size == allocated == 0
     */
    Py_ssize_t allocated;
} PyListObject;
```

CPython uses an array of pointers
