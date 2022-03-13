import requests
import datetime
from tqdm import tqdm
import time
from pprint import pprint

with open('token.txt', 'r') as file_object:  #  чтение токена для vk из файла
    token_vk = file_object.read().strip()
with open('token_ya.txt', 'r') as file_object: #  чтение токена для ЯндексДиска из файла
    token_ya = file_object.read().strip()
with open('user_id.txt', 'r') as file_object: #  чтение id пользователя из файла
    user_id = file_object.read().strip()

# Вспомогательные функции:

# 1. Функция поиска элемента с максимльным произведением значений c ключами 'width' и 'height'
#         и возврат его значений с ключами 'url' и 'type'
def find_max_size(dict_in_search):
    max_size = 0
    for j in range(len(dict_in_search)):
        file_size = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_size > max_size:
            max_size = file_size
    return dict_in_search[j].get('url'), dict_in_search[j].get('type')

# 2. Функция получает дату из стандартного представления даты и времение в vk и превращает в строку
def date_convert(date_vk):
    date_standart = datetime.datetime.fromtimestamp(date_vk)
    str_date = date_standart.strftime('%Y-%m-%d')
    return str_date

class VkUser:

    def __init__(self, token_vk, version):
        self.user_id = user_id
        self.start_params = {'access_token': token_vk, 'v': version}
        self.json, self.export_dict = self.sort_info()

    def get_photos_method(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.user_id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1}
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']

        photo_count = photo_info['count']
        photo_items = photo_info['items']

        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = find_max_size(photo_items[i]['sizes'])
            date = date_convert(photo_items[i]['date'])

            new_value = result.get(likes_count, [])
            new_value.append({'add_name': date,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self.get_photos_method()
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{elem}.jpeg'
                else:
                    file_name = f'{elem} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict


class YaUploader:
    def __init__(self, token_ya, folder_name):
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': token_ya}
        self.folder = self.create_folder(folder_name)

    def create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {folder_name} создана в корневом каталоге Яндекс.Диска!\n')
        else:
            print(f'\nПапка {folder_name} уже существует. Файлы с одинаковыми именами не будут скопированы!\n')
        return folder_name

    def in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        return in_folder_list

    def create_copy(self, dict_files):
        files_in_folder = self.in_folder(self.folder)
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
        print(f'\nЗагрузка завершена, добавлено {added_files_num} фалов!')

my_VK = VkUser(token_vk, '5.131')
pprint(my_VK.json)

my_yandex = YaUploader(token_ya, 'Фото VK')
my_yandex.create_copy(my_VK.export_dict)
