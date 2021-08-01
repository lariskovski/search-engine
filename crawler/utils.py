import logging


def timer(origin_func):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = origin_func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        logging.info(f"{origin_func.__name__} ran in {total_time}")
        return result
    
    return wrapper
