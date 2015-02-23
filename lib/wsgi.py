import wsgiref.simple_server
import cgi

import fnmatch
import os


STATIC_URL_PREFIX = '/static/'
STATIC_FILE_DIR = os.path.realpath('static') + '/'


MIME_TABLE = {
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
}    


HTTP_STATUS_CODE = {
   200: '200 Ok',
   203: '203 Non-Authoritative Information',
   204: '204 No Content',
   400: '400 User Error',
   404: '404 Not Found',
   401: '401 Unauthorized',
   403: '403 Forbidden',
   405: '405 Method Not Allowed',
   406: '406 Not Acceptable',
   409: '409 Conflict',
   410: '410 Gone',
   413: '413 Request Entity Too Large',
   414: '414 Request-URI Too Long',
   418: '418 I\'m a teapot',
   429: '429 Too Many Requests',
   431: '431 Request Header Fields Too Large',
   500: '500 Internal Server Error',
   501: '501 Not Implemented',
   503: '503 Service Unavailable',
   505: '505 HTTP Version Not Supported',
   506: '506 Variant Also Negotiates',
}


HTTPD_HOSTNAME = 'localhost'
HTTPD_PORT = 8080

def content_type(path):
    """Return a guess at the mime type for this path
    based on the file extension"""
    
    name, ext = os.path.splitext(path)
    
    if ext in MIME_TABLE:
        return MIME_TABLE[ext]
    else:
        return "application/octet-stream"


def not_found(req, res):
    res_body = ['%s: %s' % (k, v) for k, v in sorted(req.items())]
    res_body = "\n".join(res_body)
    res_body = (HTTP_STATUS_CODE[404] + "\n\n\n" + res_body).encode('utf-8')
    
    res_status = HTTP_STATUS_CODE[404]
    res_headers = [
        ('Content-Type', 'text/plain; charset="UTF-8"'),
        ('Content-Length', str(len(res_body)))
    ]
    
    res(res_status, res_headers)
    
    return [res_body]


def serve_static(req, res):
    path = req['PATH_INFO']
    path = path.replace(STATIC_URL_PREFIX, STATIC_FILE_DIR)
    path = os.path.normpath(path)
    
    if os.path.exists(path):
        print(path, 'exists')
        if path.startswith(STATIC_FILE_DIR):
            print(path)
        
            with open(path, 'rb') as f:
                content = f.read()
            
            headers = [
                ('Content-Type', content_type(path)),
                ('Content-Length', str(len(content)))
            ]

            res('200 OK', headers)
            return [content]
        else:
            print(path, 'NOT STATIC FILE!!!!!')
            return not_found(req, res)   
    else:
        print(path, 'NOT FILE!!!!!')
        return not_found(req, res)


def router(routes, req, res):
    for path, app in routes:
        if fnmatch.fnmatch(req['PATH_INFO'], path):
            print('wsgi.router', app)
            return app(req, res)
    print('wsgi.router', not_found)
    return not_found(req, res)


# EXAMPLE
def application(env, res):
    
    req_query = env['QUERY_STRING']
    req_query = cgi.parse_qs(req_query)

    try:
        req_lenght = int(env.get('CONTENT_LENGTH', 0))
    except (ValueError):
        req_lenght = 0
    
    req_body = env['wsgi.input'].read(req_lenght)
    req_body = cgi.parse_qs(req_body)
    
    #env['REQUEST_METHOD']


def serve(application):
    print("URL", HTTPD_HOSTNAME, HTTPD_PORT)
    print("STATIC_FILE_DIR", STATIC_FILE_DIR)
    httpd = wsgiref.simple_server.make_server(HTTPD_HOSTNAME, HTTPD_PORT, application)
  # httpd.handle_request()
    httpd.serve_forever()
