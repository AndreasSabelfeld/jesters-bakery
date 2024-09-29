import sys

PATH = sys.path[0]

if "\\_MEI" in PATH:
    path_string = sys.executable
    spl_word = 'an_gine'
    result = path_string.partition(spl_word)[0]
    PATH = result + spl_word
    print(PATH)
