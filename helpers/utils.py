
def get_page_content(url) -> str:
    try:
        import requests
        return requests.get(url).text
    except:
        return ""

def union(p: list, q: list) -> None:
    '''Unites two lists by adding unique elements from the second to the first one.'''
    for item in q:
        if item not in p:
            p.append(item)
    return p
