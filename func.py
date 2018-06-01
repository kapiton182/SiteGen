import re


def get_generator_from_lst(lst):
    for i in lst:
        yield i


def get_name_macros(template_file):
    return re.search(r'(\[\w+\])', template_file)[1][1:-1].lower()
