import datetime


def debug_send(send):
    def func_wrapper(*args, **kwargs):
        for arg in args:
            print('Sent: {} at {:%Y-%m-%d %H:%M:%S:%f}'
                  .format(arg, datetime.datetime.now()))
        return send(*args, **kwargs)
    return func_wrapper


def debug_recv(recv):
    def func_wrapper(*args, **kwargs):
        res = recv(*args, **kwargs)
        print('Received: {} at {:%Y-%m-%d %H:%M:%S:%f}'
              .format(res, datetime.datetime.now()))
        return res
    return func_wrapper
