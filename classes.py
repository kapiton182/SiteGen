import os
import func
from glob import glob
import re


class WorkWithGenerator:
    def __init__(self, lst):
        self.lst = lst
        self.generator = func.get_generator_from_lst(lst)

    def get_item(self):
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = func.get_generator_from_lst(self.lst)
            return next(self.generator)


class PathsToContent:
    def __init__(self, name_dir: str):
        self.name_site = name_dir
        self.path_to_dir_to_dorgen = os.getcwd()


class Text:
    def __init__(self, paths: PathsToContent):
        self.path_dir = os.path.normpath(paths.path_to_dir_to_dorgen + '/texts/' + paths.name_site)
        self.list_paths_file = os.listdir(self.path_dir)
        self._generator_paths = WorkWithGenerator(self.list_paths_file)

    def get_article(self):
        with open(self.path_dir+'\\'+self._generator_paths.get_item(), 'r') as f:
            return f.read()


class Images:
    def __init__(self, paths: PathsToContent):
        self.path_dir = os.path.normpath(paths.path_to_dir_to_dorgen + '/images/' + paths.name_site)
        self.list_paths_file = os.listdir(self.path_dir)
        self._generator_paths = WorkWithGenerator(self.list_paths_file)

    def get_image(self):
        return self._generator_paths.get_item()


class Keywords:
    def __init__(self, paths: PathsToContent):
        self.path_dir = os.path.normpath(paths.path_to_dir_to_dorgen + '/keywords/' + paths.name_site)
        self.list_paths_file = os.listdir(self.path_dir)
        self._generator_paths = WorkWithGenerator(self.list_paths_file)
        self._lst_keywords = self._get_lst_keywords()
        self._keywords = WorkWithGenerator(self._lst_keywords)

    def _get_lst_keywords(self):
        with open(self.path_dir+'\\'+self._generator_paths.get_item()) as f:
            return [i.strip() for i in f.readlines()]

    def get_keyword(self):
        return self._keywords.get_item()


class Macros:
    def __init__(self, text, img, keys):
        self.texts = text
        self.images = img
        self.keywords = keys

    def text(self):
        return self.texts.get_article()

    def img(self):
        return self.images.get_image()

    def keyword(self):
        return self.keywords.get_keyword()


class Template:
    def __init__(self, path, macroses):
        self.path_dir = os.path.normpath(path.path_to_dir_to_dorgen + '/templates/' + path.name_site)
        self.list_paths_files_for_pages = glob(self.path_dir+'**/*.html', recursive=True)
        self._templates = WorkWithGenerator(self._get_lst_text_from_templates())
        self.macros = macroses

    def _get_lst_text_from_templates(self):
        lst_text = []
        for i in self.list_paths_files_for_pages:
            with open(i, 'r') as f:
                lst_text.append(' '.join([s.strip() for s in f.readlines()]))
        return lst_text

    def get_item_from_generator(self):
        return self._templates.get_item()

    def generated_page(self):
        templ = self.get_item_from_generator()
        for _ in range(len(re.findall(r'(\[\w+\])', templ))):
            name_macro = func.get_name_macros(templ)
            content_macro = getattr(self.macros, name_macro)()
            templ = re.sub(r'(\[\w+\])', content_macro, templ, count=1)
        return templ


def main():
    paths = PathsToContent('site.com')
    text = Text(paths)
    images = Images(paths)
    keywords = Keywords(paths)
    macros = Macros(text, images, keywords)
    template = Template(paths, macros)
    print(template.generated_page())


if __name__ == '__main__':
    main()
