# hash / b-tree

[reference](https://stackoverflow.com/questions/7306316/b-tree-vs-hash-table)

一开始的索引，就是key-value结构的。但后来，为什么会出现使用b-tree的场景？




##### 从数据结构的角度

> Tree algorithms are usually easier to maintain, grow with data, scale

> The trade off for tree algorithms is small and they are suitable for almost every use case and thus are default.

处理规模化的数据时，hash维护key会显著变慢（冲突处理）
- hash时间复杂度可能落入到O(n)

- b-tree更平衡，平均复杂度为O(log n)





##### 从数据库的角度

> The difference between using a b-tree and a hash table is that the former allows you to use column comparisons in expressions that use the =, >, >=, <, <=, or BETWEEN operators, while the latter is used only for equality comparisons that use the = or <=> operators.

就存取特征而言，hash table是离散的，只能以O(1)的时间复杂度寻找特定值，而不支持range query（**主要原因**）。
