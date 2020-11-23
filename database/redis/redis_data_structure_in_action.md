
# redis数据结构及其使用场景


## list

lpush
rpush

### 使用场景

- Lpush + lpop = stack
- Lpush + rpop = queue
- Lpush + ltrim = capped collection [what is ltrim?](https://redis.io/topics/data-types-intro)
- Lpush + brpop = message queue (blocking queue)

可以剪枝，只保存前多少个，后面的都去掉（一次性/事务性删掉多个）

1. 典型的就是消息队列，用于阻塞，空的时候无法获取，那会阻塞？
2. 典型的还是airticle list，有多少个文章，无需排序，仅仅是通过index去索引

## set

不重复，无序
那么典型的什    么场景

### 使用场景

1. tag
用户标签，对某些东西感兴趣，实现应该是一棵树？

那zset呢？有序无序之间的区别？

### 底层是什么？

## zset

- element不能重复
- 通过score进行排序
有点类似学生id和学生分数

这个分数是个什么性质，比如说我想按时间排序，能做到吗？

### 使用场景呢？

主要是和list的一个对比：

0. set家族当然就是不可重复了
1. find，zset更快
2. edge work，list更快，lpop、lpush
3. 排序，根据某种分数和权重，分数改变了，顺序也会改变
    - 是可以自己指定权重方式？

> The sorted set ensure that the key is unique. If you want to do something complex. For example, every time a user login, you add the userid to a sorted set. And there is a backend service read the sorted set and update the user's information and action habbit. It can save a lot of work if you are using sorted set.
一些复杂的功能，比如每次登陆，都更新一下，按照登陆频率排序。

> What's more, if the user is a premium paid member, you can set the score of his or her id higher, and refresh this user's habbit match earlier.

高级会员，放在redis set前面，这样取这个id更快

总结起来，就是你需要动态排序，然后取一些顶点值的时候。如果是list，你可能要用代码实现，取top_k，但是zset就可以直接按照权重去获取。

https://stackoverflow.com/questions/48630763/why-use-sorted-set-instead-of-list-redis

https://stackoverflow.com/questions/64020570/why-redis-zset-means-sorted-set

https://redis.io/topics/data-types-intro

https://developpaper.com/redis-5-big-data-structure/

### 怎么实现的？

k-v的部分是通过hash，O(1)，排序的部分呢？
