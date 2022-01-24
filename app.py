from flask import Flask
import toml
import logging
import random


from providers import steinProvider

app = Flask(__name__)
app.config.from_file('config.toml', toml.load)




def get_master_stein_config():
    return {
        'url':app.config['STEIN_CONFIG_URL'],
        'username':app.config['STEIN_CONFIG_USERNAME'],
        'password':app.config['STEIN_CONFIG_PASSWORD']
    }


def get_master_collection():
    data = steinProvider(get_master_stein_config()).get('config')
    return data


def get_users():
    data = get_master_collection()
    if data:
        users = list(set([item['person'] for item in data]))
        return users
    else:
        return []

def get_user(user):
    data = get_master_collection()
    if data:
        collections = [item for item in data if item['person'] == user]
        return {'user':user,'collections':collections}
    else:
        return {}


def get_collection(user, collection):
    user = get_user(user)
    if user != {}:
        thiscollection = [item for item in user['collections'] if item['collection'] == collection][0]
        if thiscollection:
            data = steinProvider(thiscollection).get('daily')
    return data


def get_item(user, collection, mode='random'):
    data = get_collection(user, collection)
    thiscollection = [item for item in data if item['viewed'] is None]
    if mode=='random':
        length = len(thiscollection)
        item_index = random.randint(0, length-1)
        item = thiscollection[item_index]
    else:
        item = thiscollection[0]
    return item


@app.route("/")
def home_handler():
    return {'users':get_users()}


@app.route("/users/<string:user>")
def user_handler(user):
    return get_user(user)


@app.route("/users/<string:user>/collections/<string:collection>")
def user_collection_handler(user,collection):
    return {'user':user,'collection':get_collection(user, collection)}


@app.route("/users/<string:user>/collections/<string:collection>/random")
def user_collection_random_handler(user,collection):
    return get_item(user, collection)


@app.route("/users/<string:user>/collections/<string:collection>/first")
def user_collection_first_handler(user,collection):
    return get_item(user, collection, mode='first')


@app.route("/users/<string:user>/collections/<string:collection>/redirect")
def user_collection_redirect_handler(user,collection):
    return "<p>Hello, person! We're logging your thing</p>"