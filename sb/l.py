from app.models import math_timel


@math_timel  # 装饰器的使用
def sbb(x,y):
    s = x+y
    print(s)


sbb(8,2)
