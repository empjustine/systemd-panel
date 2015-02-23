import pystache

TEMPLATE_DIRNAME = 'templates/'

def render(template_basename, data):

    if 'server_address' not in data:
        data['server_address'] = '//localhost:8080'

    template_filename = '{}{}'.format(TEMPLATE_DIRNAME, template_basename)
    template = open(template_filename, 'r').read()

    return pystache.render(template, data).encode('utf-8')
