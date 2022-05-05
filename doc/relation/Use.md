# Relation: Use

## Supported Pattern
```yaml
name: Use
```
### Examples
- Use Module Level Definition
```python
// test_module_level_use.py
class Base:
    ...

class Inherit(Base):
    ...

def func1():
    return 0

x = []

y: int = 1

t1, t2 = 1, 2

(t3 := 1)
for a, b in x:
    print(a)
    print(b)

print(Base)
print(Inherit)
print(func1)
print(x)
print(y)

print(t1)

print(t2)

print(t3)
```

```yaml
name: UseModuleLevelDefinition
relation:
  exact: false
  items:
  - category: Define
    dest: test_module_level_define.Base
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.Inherit
    src: test_module_level_define
  - category: Inherit
    dest: test_module_level_define.Base
    src: test_module_level_define.Inherit
  - category: Define
    dest: test_module_level_define.func1
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.x
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.y
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.t1
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.t2
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.t3
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.a
    src: test_module_level_define
  - category: Define
    dest: test_module_level_define.b
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.a
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.b
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.Base
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.Inherit
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.func1
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.x
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.y
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.t1
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.t2
    src: test_module_level_define
  - category: Use
    dest: test_module_level_define.t3
    src: test_module_level_define

```


- Use Local Definition

```python
// test_local_use.py
def func():

    def inner():

        def inner_inner():
            print(func)

        print(func)
        print(inner_inner)

    print(inner)

def func2():

    x = 1

    y: int = 1

    t1, t2 = 1, 2

    (t3 := 1)

    for a, b in x:
        print(a)
        print(b)

    print(x)

    print(y)
    print(t1)

    print(t2)
    print(t3)

```

```yaml
name: UseLocalDefinition
relation:
  exact: false
  items:
  - category: Use
    dest: test_local_use.func
    src: test_local_use.func.inner_inner
  - category: Use
    dest: test_local_use.func
    src: test_local_use.func.inner
  - category: Use
    dest: test_local_use.func.inner_inner
    src: test_local_use.func.inner
  - category: Use
    dest: test_local_use.func.inner
    src: test_local_use.func
  - category: Use
    dest: test_local_use.func2.a
    src: test_local_use.func2
  - category: Use
    dest: test_local_use.func2.b
    src: test_local_use.func2
  - category: Use
    dest: test_local_use.func2.x
    src: test_local_use.func2
  - category: Use
    dest: test_local_use.func2.y
    src: test_local_use.func2
  - category: Use
    dest: test_local_use.func2.t1
    src: test_local_use.func2
  - category: Use
    dest: test_local_use.func2.t2
    src: test_local_use.func2
  - category: Use
    dest: test_local_use.func2.t3
    src: test_local_use.func2

```

