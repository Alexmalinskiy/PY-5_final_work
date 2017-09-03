# coding=utf-8

import requests
import time


Version_param = '5.68'
# Token_param = '9be8082c9be8082c9be8082c7c9bb5599e99be89be8082cc2839dce323a6864fcf75015'
Token_param = 'ed1d0df13558b8aa91b157cef3fe8334e832bbd29dbdeb95235c0ba2d05ac970e5382598f009c15f2652b'


def main_function():
    while True:
            print('\nВведите id пользователя, за которым шпионим или введите q - для выхода')
            inp = input().lower()
            if inp == 'q':
                print('Работа программы завершена')
                break
            else:
                if inp.isdigit():
                    friends_list = get_me_and_friends_id(inp)
                else:
                    friends_list = get_me_and_friends_id(get_user_id(inp))
                print(intersect_groups(friends_list))


def get_me_and_friends_id(id_user):
    params = {
        'user_id': id_user,
        'access_token': Token_param,
        'order': 'name',
        'fields': 'screen_name',
        'v': Version_param
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    print('.')
    list_of_id = [user_id['id'] for user_id in response.json()['response']['items']]
    return list_of_id


def get_user_id(id_user):
    params = {
        'user_ids': id_user,
        'access_token': Token_param,
        'fields': 'screen_name',
        'v': Version_param
    }
    response = requests.get('https://api.vk.com/method/users.get', params)
    print('.')
    return response.json()['response'][0]['id']


def get_groups_info(id_user):
    params = {
        'user_id': id_user,
        'access_token': Token_param,
        'extended': '0',
        'v': Version_param
     }
    response = requests.get('https://api.vk.com/method/groups.get', params)
    if 'error' in response.json().keys():
        if response.json()['error']['error_code'] == 18 or response.json()['error']['error_code'] == 7:
            return None
    print('.')
    groups = response.json()['response']['items']
    return groups


def intersect_groups(list_of_users):
    for i, friend in enumerate(list_of_users):
        # print(friend)
        someone_groups = get_groups_info(friend)
        if someone_groups is None:
            continue
        if i == 0:
            common_groups = set(someone_groups)
        common_groups = common_groups.union(set(someone_groups))
        time.sleep(0.3)
    return common_groups


if __name__ == '__main__':
    main_function()
