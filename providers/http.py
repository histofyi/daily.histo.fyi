import requests
import json


import logging


class httpProvider():

    def get(self, url, format, params=None, auth=None):
        if auth:
            r = requests.get(url, auth=(auth['username'], auth['password']))
        else:
            r = requests.get(url)
        if r.status_code == 200:
            if format == 'txt':
                content = r.text
            elif format == 'json':
                content = r.json()
            return content
        else:
            return None


    def post(self, url, payload, format, auth=None):
        if auth:
            r = requests.post(url, data=payload, auth=(auth['username'], auth['password']))
        else:
            r = requests.post(url, data=payload)
        if r.status_code == 200:
            if format == 'json':
                content = r.json()
            else:
                content = r.text
            return content
        else:
            logging.warn(r.status_code)
            logging.warn(r.text)
            return None


    def put(self, url, payload, format, auth=None):
        if auth:
            r = requests.put(url, data=payload, auth=(auth['username'], auth['password']))
        else:
            r = requests.put(url, data=payload)
        if r.status_code == 200:
            if format == 'json':
                content = r.json()
            else:
                content = r.text
            return content
        else:
            logging.warn(r.status_code)
            logging.warn(r.text)
            return None

