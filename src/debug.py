def debug_send(send):
    def func_wrapper(*args, **kwargs):
        print("Sent: ", end='')
        for arg in args:
            print(arg, end='')
        print()
        return send(*args, **kwargs)
    return func_wrapper


def debug_recv(recv):
    def func_wrapper(*args, **kwargs):
        res = recv(*args, **kwargs)
        print("Received:", end='')
        print(res)
        return recv(*args, **kwargs)
    return func_wrapper
