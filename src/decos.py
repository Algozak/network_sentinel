from typing import Callable
import time
def timer_deco(func: Callable):
    def wrapper(*args,**kwargs):
        start = time.time()
        res = func(*args,**kwargs)
        end = time.time()
        print(f"процесс выполнился за {round(end - start,2)} сек.")
        return res
    return wrapper
