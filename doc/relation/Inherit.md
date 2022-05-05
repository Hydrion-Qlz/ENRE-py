# Relation: Inherit

## Supported Pattern
```yaml
name: Inherit
```
### Examples

- Class Inherit
```python
// test_inherit.py
class Base:
    ...
class Inherit(Base):
    ...
class Base2:
    ...

class Inherit1(Base, Base2):
    ...

def func():
    class LocalInherit(Base):
        ...

    class LocalInherit2(Base, Base2):
        ...
```

```yaml
name: ClassInherit
relation:
  exact: false
  items:
  - category: Inherit
    dest: test_inherit.Base
    src: test_inherit.Inherit
    r:
      e: .
      u: .
      d: .
  - category: Inherit
    dest: test_inherit.Base
    src: test_inherit.Inherit1
    r:
      e: .
      u: .
      d: .
  - category: Inherit
    dest: test_inherit.Base2
    src: test_inherit.Inherit1
    r:
      e: .
      u: .
      d: .
  - category: Inherit
    dest: test_inherit.Base
    src: test_inherit.func.LocalInherit
    r:
      e: .
      u: .
      d: .
  - category: Inherit
    dest: test_inherit.Base
    src: test_inherit.func.LocalInherit2
    r:
      e: .
      u: .
      d: .
  - category: Inherit
    dest: test_inherit.Base2
    src: test_inherit.func.LocalInherit2
    r:
      e: .
      u: .
      d: .

```
- VariableInherit
```python
// test_variable_inherit.py
def mixin(c, d):
    class Mixed(c, d):
        ...
```

```yaml
name: VariableInherit
relation:
  exact: false
  items:
  - category: Inherit
    dest: test_variable_inherit.Mixed.c
    src: test_variable_inherit.mixin.Mixed
    r:
      e: .
      u: x
      d: x

  - category: Inherit
    dest: test_variable_inherit.Mixed.d
    src: test_variable_inherit.mixin.Mixed
    r:
      e: .
      u: x
      d: x

```