import logging

def get_page_content(url) -> str:
    try:
        import requests
        return requests.get(url).text
    except:
        logging.warn(f"Couldnt get content from address {url}")
        return ""

def union(p: list, q: list) -> None:
    '''Unites two lists by adding unique elements from the second to the first one.'''
    for item in q:
        if item not in p:
            p.append(item)
    return p


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
