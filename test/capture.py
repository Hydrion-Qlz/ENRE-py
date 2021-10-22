free_var = 1

def fun():
    print(free_var)

    free_var = 2
    global free_var

fun()