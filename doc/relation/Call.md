# Relation: Call

## Supported Pattern
```yaml
name: Call
```
### Examples

- Global Function Call
```python
// test_global_function_call.py
def func1():
    func1()
    return 0

func1()

```

```yaml
name: GlobalFunctionCall
relation:
  exact: false
  items:
  - category: Define
    dest: test_global_function_call.func1
    src: test_global_function_call
  - category: Call
    dest: test_global_function_call.func1
    src: test_global_function_call.func1
  - category: Call
    dest: test_global_function_call.func1
    src: test_global_function_call
```
- Class Method Call
```python
// test_method_call.py
class ClassA:

    def method(self):
        ...


class ClassB:

    def method(self):
        ...


instance = ClassA()
instance.method()


```
```yaml
relation:
  exact: false
  items:
  - category: Define
    dest: test_method_call.ClassA
    src: test_method_call
  - category: Define
    dest: test_method_call.ClassA.method
    src: test_method_call.ClassA
  - category: Define
    dest: test_method_call.ClassB
    src: test_method_call
  - category: Define
    dest: test_method_call.ClassB.method
    src: test_method_call.ClassB
  - category: Define
    dest: test_method_call.instance
    src: test_method_call
  - category: Call
    dest: test_method_call.ClassA.method
    src: test_method_call

```

- Local Function Call
```python
// test_local_call.py
def func():
    def inner():
        def inner_inner():
            func()

        func()

        inner_inner()

    inner()
```

```yaml
name: LocalFunctionCall
relation:
  exact: false
  items:
  - category: Define
    dest: test_local_call.func
    src: test_local_call
  - category: Define
    dest: test_local_call.func.inner
    src: test_local_call.func
  - category: Define
    dest: test_local_call.func.inner_inner
    src: test_local_call.func
  - category: Call
    dest: test_local_call.func
    src: test_local_call.func.inner_inner
  - category: Call
    dest: test_local_call.func
    src: test_local_call.func.inner
  - category: Call
    dest: test_local_call.func.inner_inner
    src: test_local_call.func.inner
  - category: Call
    dest: test_local_call.func.inner
    src: test_local_call.func
  - category: Define
    dest: test_local_call.func2.x
    src: test_local_call.func2
  - category: Define
    dest: test_local_call.func2.y
    src: test_local_call.func2
  - category: Define
    dest: test_local_call.func2.t1
    src: test_local_call.func2
  - category: Define
    dest: test_local_call.func2.t2
    src: test_local_call.func2
  - category: Define
    dest: test_local_call.func2.t3
    src: test_local_call.func2
```

- First Order Function Call
``` python
// test_first_order_func_call.py
def acceptor(f):
    f()
```

```yaml
name: FirstOrderFunctionCall
relation:
    exact: False
    filter: Call
    items:
    - dest: test_first_order_func_call.f
      src: test_first_order_func_call.acceptor

```
