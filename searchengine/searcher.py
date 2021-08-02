
def lookup(index:list, keyword:str) -> list:
    if keyword in index:
        return index[keyword]
    return None

def lookup_best(index: dict, keyword: str, ranks: dict) -> str:
    urls_for_kw: list = lookup(index, keyword)

    if urls_for_kw:
        # Get set intersection between all possible urls for a given keyword and the ranked dictionary
        url_rank_intersection: set = set(urls_for_kw).intersection(set(ranks.keys()))
        # transforms set into a dict for later sorting
        selected_ranks: dict = {key : ranks[key] for key in url_rank_intersection}
        # sorts values in reverse order. gets most popular page
        sort_selected_rank:list = [k for k, v in sorted(selected_ranks.items(), key=lambda item: item[1], reverse=True)]

        best_url = sort_selected_rank[0]
        
        return best_url
    
    return None
