# coding=utf-8

import requests
import time
import json


Version_param = '5.68'
# Token_param = '9be8082c9be8082c9be8082c7c9bb5599e99be89be8082cc2839dce323a6864fcf75015'
# Token_param = 'ed1d0df13558b8aa91b157cef3fe8334e832bbd29dbdeb95235c0ba2d05ac970e5382598f009c15f2652b'
Token_param = '99417014f01682d80dba993686a61ce214380698ff5ba42709a6211e244c744eb97a809329d707c11fef3'
field = 'screen_name'


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
                sec_groups = intersect_groups(inp, friends_list)
                save_to_file(sec_groups)


def get_me_and_friends_id(id_user):
    params = {
        'user_id': id_user,
        'access_token': Token_param,
        'order': 'name',
        'fields': field,
        'v': Version_param
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    print('.')
    # print(response.json())
    list_of_id = [user_id['id'] for user_id in response.json()['response']['items']]
    return list_of_id


def get_user_id(id_user):
    params = {
        'user_ids': id_user,
        'access_token': Token_param,
        'fields': field,
        'v': Version_param
    }
    response = requests.get('https://api.vk.com/method/users.get', params)
    print('.')
    return response.json()['response'][0]['id']


def get_groups_info(id_user):
    params = {
        'user_id': id_user,
        'access_token': Token_param,
        'extended': '1',
        'v': Version_param
     }
    response = requests.get('https://api.vk.com/method/groups.get', params)
    if 'error' in response.json().keys():
        if response.json()['error']['error_code'] == 18 or response.json()['error']['error_code'] == 7:
            return None
    print('.')
    # print(response.json())
    groups = response.json()['response']['items']
    # print(groups)
    return groups


def intersect_groups(id_user, list_of_users):
    for i, friend in enumerate(list_of_users):
        # print(friend)
        someone_groups = get_groups_info(friend)
        if someone_groups is None:
            continue
        if i == 0:
            common_groups = set([group['id'] for group in someone_groups])
            continue
        common_groups = common_groups.union(set([group['id'] for group in someone_groups]))
        time.sleep(0.3)
    user_groups = get_groups_info(id_user)
    secret_groups = [group for group in user_groups if group['id'] not in common_groups]
    # not_secret_groups = [group for group in user_groups if group in common_groups]
    # print(len(secret_groups))
    # print(len(not_secret_groups))
    # print(len(user_groups))
    print(secret_groups)
    return secret_groups


def save_to_file(groups):
    dict_gr = dict()
    list_gr = []
    dict_gr["count"] = len(groups)
    for i in range(0, len(groups)):
        dict_one_gr = dict()
        dict_one_gr[groups[i]['id']] = groups[i]['name']
        list_gr.append(dict_one_gr)
    dict_gr["secret_groups"] = list_gr
    with open("secret vk groups.json", "w", encoding="utf8") as file:
        json.dump(dict_gr, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main_function()
