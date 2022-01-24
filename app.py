from flask import Flask, redirect
import toml
import base64
import random


import logging


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
        return collections
    else:
        return []

def get_collection_metadata(user, collection):
    user = get_user(user)
    thiscollection = {}
    if user != {}:
        thiscollection = [item for item in user if item['collection'] == collection][0]
        if thiscollection:
            return thiscollection
    return thiscollection


def get_collection(user, collection):
    thiscollection = get_collection_metadata(user, collection)
    if thiscollection != {}:
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
    if item:
        item['uid'] = base64.urlsafe_b64encode(item['item'].encode('utf-8')).decode('ascii')
    return item


def get_specific_item(user, collection, url):
    data = get_collection(user, collection)
    thisitem = None
    matches = [item for item in data if item['item'] == url]
    if len(matches) > 0:
        thisitem = matches[0]
    if not thisitem:
        thisitem = None
    return thisitem


def get_first_item(user, collection):
    return get_item(user, collection, mode='first')


def get_item_by_base64_string(user,collection,base64_string):
    collection_config = get_collection_metadata(user,collection)
    url = None
    if base64_string:
        try:
            base64_string = base64_string.encode('ascii')
            url = base64.urlsafe_b64decode(base64_string).decode('utf-8')
        except:
            url = None
    if url:
        item = get_specific_item(user, collection, url)
    return item, collection_config, url


def record_viewed(item, collection_config):
    if item:
        data = steinProvider(collection_config).update('daily',item)
    else:
        data = None
    return data


def collect_items_for(user):
    user_collections = get_user(user)
    items = {}
    for collection in user_collections:
        thiscollection = collection['collection']
        items[thiscollection] = {}
        if collection['mode'] == 'first':
            items[thiscollection] = get_first_item(user, thiscollection)
        else:
            items[thiscollection] = get_item(user, thiscollection)
        items[thiscollection]['collection'] = thiscollection
    return items, user_collections



@app.route("/")
def home_handler():
    return {'users':get_users()}


@app.route("/users/<string:user>")
def user_handler(user):
    user_items, user_collections = collect_items_for(user)
    return user_items

@app.route("/users/<string:user>/collections/<string:collection>")
def user_collection_handler(user,collection):
    return {'user':user,'collection':get_collection(user, collection)}


@app.route("/users/<string:user>/collections/<string:collection>/random")
def user_collection_random_handler(user,collection):
    item = get_item(user, collection)
    return item


@app.route("/users/<string:user>/collections/<string:collection>/first")
def user_collection_first_handler(user,collection):
    item = get_first_item(user, collection)
    return item


@app.route("/users/<string:user>/collections/<string:collection>/redirect/<string:base64_string>")
def user_collection_redirect_handler(user,collection,base64_string):
    item, collection_config, url = get_item_by_base64_string(user,collection,base64_string)
    if url and item:
        data = record_viewed(item, collection_config)
    else:
        data = None
    if data and url:
        return redirect(url, code=302)
    else:
        return {'message':'Oops, problem'}