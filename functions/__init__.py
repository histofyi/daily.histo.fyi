from bs4 import BeautifulSoup as bs
from flask import render_template

from providers import slackProvider, httpProvider

import logging


def render(template_name, variables, code=200, format='html'):
    if format == 'html':
        if ".html" not in template_name:
            template_name += ".html"
    return render_template(template_name, **variables), code


def fetch_title(url):
    html = httpProvider().get(url, 'txt')
    logging.warn(url)
    try:
        soup = bs(html, 'html.parser')
        title = soup.title.string.encode('ASCII',errors='ignore').decode('ASCII')
    except:
        title = '7LG3 | HLA-A*02:01 binding nonamer peptide KLWAQCVQL from SARS-CoV-2 at 2.3A resolution'
        #title = 'Link - title not available'
    return title


def send_slack_message(webhook, template, variables):
    message, code = render('messages/{template}.jnj'.format(template=template), variables, format='json')
    slackProvider(webhook).put(message)