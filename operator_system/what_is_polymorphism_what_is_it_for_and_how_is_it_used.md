# what_is_polymorphism_what_is_it_for_and_how_is_it_used

就是不同类型使用同一套上层接口，但底层实现不同。

最初的整数和浮点数其实就有类似的概念在里面。（知乎，为什么会有类型？Ivony）
整数和浮点数都有 `+`/`-`/`*`/`/`的操作，但底层的实现上会有不同
在C++里面，不同类型的`+`操作，都会调用`operator+()`的类函数。

当然，经常用的一个例子就是`Shape`派生出来的square, circle, dodecahedron, irregular polygon, splat。

如果没有多态`square.draw()`可能会变成`drawSquare()`, `drawCircle()`。

https://stackoverflow.com/questions/1031273/what-is-polymorphism-what-is-it-for-and-how-is-it-used