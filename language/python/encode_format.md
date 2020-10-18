# ENCODE: ascii unicode utf-8

1. ascii各国自己标准
2. unicode完全一致（**映射关系**）
3. utf-8等编码方式是unicode的一种实现，

```py
unicode_str = u'邵瑞'
utf8_str = unicode_str.encode('utf8')
unicode_str_2 = utf8_str.decode('utf8')

>>> str = '邵瑞'
>>> str.decode('utf8')
u'\u90b5\u745e'
>>> str.decode('gbk')
u'\u95ad\u7535\u61ba'

type(str.decode('utf8'))

```

utf-8是一种**编码方式**，**文件**中要有编码格式，这样IDE打开文档时，才能显示正确的文字。
unicode则是**内存**中的格式，独一无二。不同国家的不同文字，都有唯一的unicode，但是**太长**了，浪费内存。这里就需要各种编码方式。utf-8...缩减长度
