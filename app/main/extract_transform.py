"""
Dealing with response json
"""

import json
import csv
import vk_api
from datetime import datetime


def wall_binary_search(vk, query):
    pass


def wall_linear_search(vk, query):
    """
    Search posts that match query from latest to earliest.
    Iteratively requesting more posts if query conditions are not met.
    :param vk:
    :param query:
    :return: List[Dict]
    """

    all_posts = []
    offset = 0
    wall_search_finished = False
    while not wall_search_finished:
        try:
            posts = vk.wall.get(owner_id=f"-{query.get('id')}", count=100, offset=offset)
            items = posts['items']
        except vk_api.exceptions.ApiError:
            # TO-DO: add logging
            raise vk_api.exceptions.ApiError
        except KeyError:
            raise vk_api.exceptions.ApiError

        # items are sorted in descending order by time (unless it has changed)
        min_date = datetime.utcfromtimestamp(items[-1]['date']).strftime('%Y-%m-%d')

        try:
            all_posts.extend(process_batch(items, query))
        except Exception as e:
            print(e.args)
            return []

        if min_date <= query['start']:
            wall_search_finished = True

    # fit range
    all_posts = [post for post in all_posts if query['start'] <= post['date'] <= query['end']]

    # sort by chosen order
    sorting_key = query['order']
    all_posts = sorted(all_posts, key=lambda x: x[sorting_key], reverse=True)
    return all_posts


def process_batch(items, query):
    # TO-DO: better attachments
    posts_data = []
    for item in items:
        post_data = {key: item[key] for key in ['id', 'from_id']}

        post_data['text'] = "\n".join(item['text'].split("\n")[:7]) + \
                            ("\n..." if len(item['text'].split("\n")) > 7 else "")
        post_data['attachments'] = item.get('attachments', {})
        post_data['date'] = datetime.utcfromtimestamp(item['date']).strftime('%Y-%m-%d')
        post_data['url'] = f"https://vk.com/{query['screen_name']}?w=wall{item['owner_id']}_{item['id']}"
        post_data['likes'] = int(item.get('likes', 0).get('count', 0))
        post_data['comments'] = int(item.get('comments', 0).get('count', 0))
        post_data['views'] = int(item.get('views', 0).get('count', 0))
        post_data['reposts'] = int(item.get('reposts', 0).get('count', 0))
        posts_data.append(post_data)

    return posts_data


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
