# -*- coding: utf-8 -*-
import time, functools
import time
import functools

'''
def metric(fn):#并没有做到真正的获取运行时间
    print('%s executed in %s ms' % (fn.__name__, 10.24))
    return fn
'''
def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kw):
        start=time.time()
        res=fn(*args,**kw)
    
        end=time.time()
        s=end-start
        print('%s executed in %s ms' % (fn.__name__,s))
        return res
    return wrapper
#之前直接在两次获取时间之间直接调用fn，一直不知道该怎么写参数
#网上看到这个写的是又定义了一个函数参数为(*args,**kw)
#返回时不一定返回函数，也可以是相应的值
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;

@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
#print(f)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')
else :
    print('测试成功！')
