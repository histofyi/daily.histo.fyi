from .http import httpProvider

import logging
import json
import datetime

class steinProvider():

    config = None


    def __init__(self, config):
        self.config = config


    def get(self, table):
        url = self.config['url'] + '/' + table
        data = httpProvider().get(url, 'json', auth=self.config)
        if data:
            return data
        else:
            return None


    def update(self, table, item):
        url = self.config['url'] + '/' + table
        viewed_date = datetime.datetime.now().isoformat()
        payload = {
            'condition':{
                'item':item['item']
            },
            'set':{
                'viewed':'yes',
                'viewed_date':viewed_date
            }
        }
        data = httpProvider().put(url, json.dumps(payload), 'json', auth=self.config)

        if data:
            logging.warn(data)
        else:
            data = {}
        return data