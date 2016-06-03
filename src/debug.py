import datetime
import logging

# Set by init_debug, retains what the MPI process' rank is.
process_rank = -1


def init_debug(rank):
    """Given a rank creates a log file.

    Args:
    rank: The MPI rank of a process.
    """
    global process_rank
    process_rank = rank
    logging.basicConfig(filename='logs/' + str(rank), level=logging.DEBUG)


def debug_send(send):
    def func_wrapper(*args, **kwargs):
        for arg in args:
            logging.debug('Sent: {} at {:%Y-%m-%d %H:%M:%S:%f}'
                          .format(arg, datetime.datetime.now()))
        return send(*args, **kwargs)
    return func_wrapper


def debug_recv(recv):
    def func_wrapper(*args, **kwargs):
        res = recv(*args, **kwargs)
        logging.debug('Received: {} at {:%Y-%m-%d %H:%M:%S:%f}'
                      .format(res, datetime.datetime.now()))
        return res
    return func_wrapper
