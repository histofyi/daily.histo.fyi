from .http import httpProvider

import logging

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