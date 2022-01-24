from flask import render_template

from providers import slackProvider


def render(template_name, variables, code=200, format='html'):
    if format == 'html':
        if ".html" not in template_name:
            template_name += ".html"
    return render_template(template_name, **variables), code




def send_slack_message(webhook, template, variables):
    message, code = render('messages/{template}.jnj'.format(template=template), variables, format='json')
    slackProvider(webhook).put(message)