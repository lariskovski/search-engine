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

def add_page_to_index(index: list, url: str, content: str) -> list:
    words = content.split()
    for word in words:
        is_word_in_keywords = False
        for entry in index:
            if word == entry[0]:
                entry[1].append(url)
                is_word_in_keywords = True
        if not is_word_in_keywords:
            index.append([word, [url]])
    return index


add_page_to_index(index, 'fake.test', 'This is a test')
add_page_to_index(index, 'real.test', 'This is not a test')

def lookup(index:list,keyword:str) -> list:
    for entry in index:
        # entry[0] = index[0] = dog
        if entry[0] == keyword:
            return entry[1]
    return []

print(lookup(index, 'dog'))
print(lookup(index, 'giraffe'))
print(lookup(index, 'This'))