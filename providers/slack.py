import json
import logging

from .http import httpProvider



class slackProvider():

    webhook = None

    def __init__(self, webhook):
        self.webhook = webhook


    def put(self, message):
        response = httpProvider().post(self.webhook, message, 'txt')
        return response


