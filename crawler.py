# page = contents of a web page
page = ('<div id="top_bin"><div id="top_content" class="width960">'
'<div class="udacity float-left"><a href="http://udacity.com">')

def get_next_target(page: str) -> tuple:
    start_link = page.find('<a href=')

    # if the link tag sequence is not found, find returns a -1
    if start_link == -1:
        # return the error codes of None, 0 now and skip the rest!
        return None, 0

    # Get url start and end index inside double quotes after href tag
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    return url, end_quote


def print_all_links(page: str) -> None:
    while True:
        url, endpos = get_next_target(page)
        if url != None:
            print(url)
            page = page[endpos:]
        else:
            break

print_all_links(page)

# ============
# Web Search Index
# ============
index = [
        ['dog' , ['https://petshop.com', 'https://doglovers', 'https://dogsarethebest.us']],
        ['cat', ['https://catsthemovie.com']],
        ['ducks', ['https://honk.io']]
        ]


def add_to_index(index: list, keyword: str, url: str):
    for entry in index:
        # entry[0] = index[0] = dog
        if entry[0] == keyword:
            entry[1].append(url)
            return

    index.append([keyword,[url]])

add_to_index(index, 'dog', 'https://thewhaledogs.co')
add_to_index(index, 'whale', 'https://japanwhales.jp')
# print(index)



def lookup(index:list,keyword:str) -> list:
    for entry in index:
        # entry[0] = index[0] = dog
        if entry[0] == keyword:
            return entry[1]
        else:
            return []

print(lookup(index, 'dog'))
print(lookup(index, 'giraffe'))