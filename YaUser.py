import requests
from tqdm import tqdm
import time
import json

class YaUploader:
    def __init__(self, token_ya, folder_name):
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': token_ya}
        self.folder = self._create_folder(folder_name)

    def _create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {folder_name} создана в корневом каталоге Яндекс.Диска!\n')
        else:
            print(f'\nПапка {folder_name} уже существует. Файлы с одинаковыми именами не будут скопированы!\n')
        return folder_name

    def _in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        return in_folder_list

    def _create_copy(self, dict_files):
        files_in_folder = self._in_folder(self.folder)
        added_files_num = 0
        for key in tqdm(dict_files.keys()):
            time.sleep(1)
            if key not in files_in_folder:
                params = {'path': f'{self.folder}/{key}',
                          'url': dict_files[key],
                          'overwrite': 'false'}
                requests.post(self.url, headers=self.headers, params=params)
                added_files_num += 1
            else:
                print(f'Копирование отменено, Файл {key} уже существует!')
        print(f'\nЗагрузка завершена, добавлено {added_files_num} файлов!')

    def _json_file(self, logs_list):
        with open(f'json.txt', 'a') as f:
            json.dump(logs_list, f, indent=2)
