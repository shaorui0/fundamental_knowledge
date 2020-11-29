# Item 21: Enforce Clarity with Keyword-Only Arguments

```py
# TODO exec
def foo(a, b, c, d):
    print(a,b,c,d)

foo(1, 2, 3, 4)
foo(1, 2, c=3, d=4)


def foo(a, b, *, c=1, d=2):
    print(a,b,c,d)

foo(1, 2, 3, 4)
foo(1, 2, c=3, d=4)
```