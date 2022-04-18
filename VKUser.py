import requests
import datetime

class VKPhoto:

    url = 'https://api.vk.com/method/'
    def __init__(self, token, version, user_id, user_count):
        self.params = {
            'access_token': token,
            'v': version
        }
        self.user_id = user_id
        self.user_count = user_count
        self.json, self.export_dict = self._sort_info()

    def _get_photo(self):
        # блок получения id в виде цифрового кода, если пользователь вводит screen name
        get_user_url = self.url + 'users.get'
        get_user_params = {'user_ids': self.user_id}
        id = requests.get(get_user_url, params={**self.params, **get_user_params}).json()['response'][0]['id']

        get_photo_url = self.url + 'photos.get'
        get_photo_params = {
              'owner_id': id,
              'album_id': 'profile',
              'photo_sizes': 0,
              'extended': 1,
              'count': self.user_count,
        }
        req = requests.get(get_photo_url, params={**self.params, **get_photo_params}).json()['response']

        photo_count = req['count']
        photo_items = req['items']

        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            max_size = 0
            for j in range(len(photo_items[i]['sizes'])):
                file_size = photo_items[i]['sizes'][j].get('width') * photo_items[i]['sizes'][j].get('height')
                if file_size > max_size:
                    max_size = file_size

            url_download, picture_size = photo_items[i]['sizes'][j].get('url'), photo_items[i]['sizes'][j].get('type')

            date_standart = datetime.datetime.fromtimestamp(photo_items[i]['date'])
            date = date_standart.strftime('%Y-%m-%d')

            new_value = result.get(likes_count, [])
            new_value.append({'add_name': date,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_photo()
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{elem}.jpeg'
                else:
                    file_name = f'{elem} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                sorted_dict[file_name] = picture_dict[elem][0]['url_picture']

        return json_list, sorted_dict



