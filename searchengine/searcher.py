
def lookup(index:list, keyword:str) -> None:
    if keyword in index:
        return index[keyword]
    return None
