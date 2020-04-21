from functools import wraps
from time import time

# decorator for send_image function to print_time
def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func: %r took: %2.4f sec' % (f.__name__, te-ts))
        return result
    return wrap
