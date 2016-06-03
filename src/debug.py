def debug_send(send):
    def func_wrapper(*args, **kwargs):
        print("Sent:")
        for arg in args:
            print(arg)
        return send(*args, **kwargs)
    return func_wrapper


def debug_recv(recv):
    def func_wrapper(*args, **kwargs):
        print("Received:")
        for arg in args:
            print(arg)
        return recv(*args, **kwargs)
    return func_wrapper
