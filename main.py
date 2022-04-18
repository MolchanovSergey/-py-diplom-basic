from VKUser import VKPhoto
from YaUser import YaUploader


with open('token.txt', 'r') as file_object:  #  чтение токена для vk из файла
    token_vk = file_object.read().strip()
with open('token_ya.txt', 'r') as file_object: #  чтение токена для ЯндексДиска из файла
    token_ya = file_object.read().strip()


if __name__ == '__main__':
    my_VK = VKPhoto(token_vk, '5.131', 'molchanof', 10)
    my_yandex = YaUploader(token_ya, 'Фото VK')
    my_yandex._create_copy(my_VK.export_dict)
    my_yandex._json_file(my_VK.json)

