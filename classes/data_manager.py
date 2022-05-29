import json
#from pprint import pprint as pp
from classes.exceptions import DataSourceBrokenException

class DataManager:

    def __init__(self, path):
        self.path = path
        pass

    def _load_data(self):
        """загрузка из файла для дальнйшего использования"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise DataSourceBrokenException("Файл с данными повржден")
        return data


    def _save_data(self, data):
        """перезапись данных в файл с данными"""

        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


    def get_all(self):
        """передает данные"""
        data = self._load_data()
        return data

    def search(self, substring):
        """передает посты, которые содержат подстроку"""

        posts = self._load_data()
        substring = substring.lower()
        matching_posts = [post for post in posts if substring in post["content"].lower()]

        return matching_posts

    def add(self, post):
        """"добавляет пост"""

        if type(post) != dict:
            raise TypeError("Dict expected for adding post")

        posts = self._load_data()
        posts.append(post)
        self._save_data(posts)
