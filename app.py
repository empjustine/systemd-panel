#!/usr/bin/env python

import lib.systemd as systemd
import lib.wsgi as wsgi
import lib.template as template


def systemd_units(_, res):
   
    data = {'units': systemd.units()} 
    res_body = template.render('units.html', data)
    
    res_headers = [
        ('Content-Type', 'text/html; charset="UTF-8"'),
        ('Content-Length', str(len(res_body)))
    ]
    
    res(wsgi.HTTP_STATUS_CODE[200], res_headers)
    
    return [res_body]


CORE_ROUTES = [
    ('/systemd/units', systemd_units),
    ('/static/**', wsgi.serve_static),
  # ('/', route_index),
    ('*', wsgi.not_found),
]

def application(req, res):
    return wsgi.router(CORE_ROUTES, req, res)
    
wsgi.serve(application)
