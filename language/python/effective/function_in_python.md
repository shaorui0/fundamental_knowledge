# ___call___

函数是一等公民
直接作为closure使用
类也可以作为函数使用，通过`__call__`
```py
class Foo:
    def __call__(self):
        pass
Foo()
```