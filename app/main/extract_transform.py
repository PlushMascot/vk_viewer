"""
Поиск информации о постах вконтакте в группе
"""

import requests
import json
import csv
import vk_api
from time import sleep
from datetime import datetime
from.credentials import APP_ID, CLIENT_SECRET

# URL, который использоются при получении code на первом этапе авторизации и получении access_token


# def get_groups_info(auth_code: str) -> [str]:
#     """
#     :param auth_code:
#     :return: list of ids for each of user's groups
#     """
#
#     vk_session = vk_api.VkApi(app_id=APP_ID, client_secret=CLIENT_SECRET)
#     try:
#         vk_session.code_auth(auth_code, redirect_uri)
#     except vk_api.AuthError as error_msg:
#         print(error_msg)
#         return
#     vk = vk_session.get_api()
#     print(vk_session.token['user_id'])
#     print(vk_session.token['access_token'])
#     groups = vk.groups.get()
#     if groups.get('count', 0) > 0:
#         groups_ids = groups['items']
#     else:
#         return
#
#     groups_info = vk.groups.getById(group_ids=groups_ids)
#     groups_info = groups_info['response']['items']
#
#     return groups_info


def write_json(data, filename):
    with open(filename + '.json', 'w') as file:
        json.dump(data, file)


def write_csv(data):
    with open('posts_data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['id'],
                         data['likes'],
                         data['reposts']
                         ))


def get_data(post):
    # получения информации о посте
    try:
        post_id = post['id']
    except:
        return

    try:
        likes = post['likes']['count']
    except:
        return

    try:
        reposts = post['reposts']['count']
    except:
        return

    data = {
        'id': post_id,
        'likes': likes,
        'reposts': reposts,
    }

    return data


if __name__ == "__main__":
    start = datetime.now()

    # заря
    # group_id = -66639910

    # d_u_ra
    # group_id = -26945644

    offset = 0
    ACCESS_TOKEN = '1b646275d5c1b7d058a44f667100421273d435fbd17da19cbc208383fd952c24c818b60c61ea7248c907c'
    number_of_posts = 100
    date_x = 1543698000  # 1 Dec 2018
    all_posts = []

    while offset < number_of_posts:
        sleep(1)
        r = requests.get('https://api.vk.com/method/wall.get', params={'owner_id': group_id,
                                                                       'count': 100,
                                                                       'offset': offset,
                                                                       'access_token': ACCESS_TOKEN,
                                                                       'v': 5.92})
        try:
            posts = r.json()['response']['items']
        except KeyError as e:
            print("KeyError")
            print(str(r.json()))
            break
        all_posts.extend(posts)
        offset += 100
        print(offset)
        oldest_date = posts[-1]['date']
        if oldest_date < date_x:
            break

    write_json(all_posts, 'all_posts')
    data_posts = []

    for post in all_posts:
        if get_data(post):
            post_data = get_data(post)
        else:
            continue
        write_csv(post_data)

    end = datetime.now()
    total = end - start
    print(total)
