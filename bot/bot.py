import configparser
import random

import requests

config = configparser.ConfigParser()
config.read(r'config.txt')
number_of_users = int(config.get('Bot Config', 'number_of_users'))
max_posts_per_user = int(config.get('Bot Config', 'max_posts_per_user'))
max_likes_per_user = int(config.get('Bot Config', 'max_likes_per_user'))
HOST = 'http://localhost:8000/'


def get_access_token(user_data):
    response = requests.post(HOST + 'api/token/',
                             data=user_data, )
    json_response = response.json()
    access_token = json_response['access']
    if response.status_code == 200:
        return access_token
    else:
        return None


def create_users(token, number_of_users):
    users = []
    for i in range(number_of_users):
        users.append(
            {'first_name': 'name_{}'.format(i), 'last_name': 'surname_{}'.format(i), 'username': 'user_{}'.format(i),
             'password': 'password_{}'.format(i)})
        response = requests.post(HOST + 'api/users/', data=users[i], headers={'Authorization': 'Bearer {}'.format(
            token)})
        if response.status_code == 201:
            print('user {} created!'.format(users[i]['username']))
        else:
            print('Error')
    return users


def create_posts(user, number_of_post):
    user_data = {'username': user['username'], 'password': user['password']}
    token = get_access_token(user_data)
    posts = []
    for i in range(number_of_post):
        posts.append({'title': 'title_{}'.format(i), 'content': 'content_{}'.format(i)})
        response = requests.post(HOST + 'api/posts/', data=posts[i], headers={'Authorization': 'Bearer {}'.format(
            token)})
        if response.status_code == 201:
            print('Post {} created!'.format(posts[i]['title']))
        else:
            print('Error')
    return posts


def like_post(user, number_of_likes, post_amount):
    user_data = {'username': user['username'], 'password': user['password']}
    token = get_access_token(user_data)
    for i in range(number_of_likes):
        post_id = random.randint(1, post_amount)
        response = requests.put(HOST + 'api/like/{}/'.format(post_id), headers={'Authorization': 'Bearer {}'.format(
            token)})
        if response.status_code == 201:
            print(response.json())
        else:
            print('Error')


def main():
    admin_data = {'username': 'admin', 'password': 'admin'}
    admin_access_token = get_access_token(admin_data)
    users = create_users(admin_access_token, number_of_users)
    users_posts = []
    post_amount = 0
    for user in users:
        num_post = random.randint(1, max_posts_per_user)
        posts = create_posts(user, num_post)
        users_posts.append(posts)
        post_amount += len(posts)

    for user in users:
        like_post(user, max_likes_per_user, post_amount)


main()
