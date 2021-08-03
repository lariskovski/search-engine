
def str_to_list(string):
    string = string.replace('[', '').replace(']', '').replace("'", '')
    return string.split(',')
