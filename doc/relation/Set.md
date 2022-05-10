# Relation: Set

## Supported Pattern
```yaml
name: Set
```
### Examples

- Set Variable
```python
// test_set_variable.py
x = 1

y: int = 1
t1, t2 = 1, 2

(t3 := 1)

x = 1

y = 2

t1, t2 = 3, 4

```

```yaml
name: Set Global Variable
relation:
  exact: false
  items: 
  - category: Set
    dest: test_set_variable.x
    src: test_set_variable
    r: 
      s: x
      e: .
      d: xUse
      u: .
  - category: Set
    dest: test_set_variable.y
    src: test_set_variable
    r: 
      s: x
      e: .
      d: xUse
      u: .
  - category: Set
    dest: test_set_variable.t1
    src: test_set_variable
    r: 
      s: x
      e: .
      d: xUse
      u: .
  - category: Set
    dest: test_set_variable.t2
    src: test_set_variable
    r: 
      s: x
      e: .
      d: xUse
      u: .
  - category: Set
    dest: test_set_variable.t3
    src: test_set_variable
    r: 
      s: x
      e: x
      d: x
      u: .
```

