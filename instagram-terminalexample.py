"""
Modified version of code to deal with authenticating to Instagram without a server
You'll need to set your redirect URL to localhost:8080 to use this
"""

import urllib, urllib2, webbrowser, json, cgi, logging
from instagram.client import InstagramAPI

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

import BaseHTTPServer, urlparse
from SimpleHTTPServer import SimpleHTTPRequestHandler

class ListenerHandlerClass(SimpleHTTPRequestHandler):
    def do_GET(self):
        resp = "PIN received."
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(resp))
        self.end_headers()
        self.wfile.write(resp)
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)
        try:   
            self.parent.code = queryParsed['code'][0]
        except:
            pass

class Listener():
    def __init__(self):
        self.code = None
        port = 8080
        server_address = ('127.0.0.1', port)
        ListenerHandlerClass.parent = self
        ServerClass  = BaseHTTPServer.HTTPServer
        ListenerHandlerClass.protocol_version = "HTTP/1.0"
        httpd = ServerClass(server_address, ListenerHandlerClass)
        sa = httpd.socket.getsockname()
        print "Serving HTTP on", sa[0], "port", sa[1], "..."
        while not self.hasPin():
            httpd.handle_request()

    def hasPin(self):
        if self.code is not None:
            return True
        else:
            return False

def getAccess():
    params = {
        'client_id': '',
        'client_secret': '',
        'redirect_uri': 'http://localhost:8080', #http://localhost: 
        'response_type': 'code'       
    }
    baseurl = 'https://api.instagram.com/oauth/authorize/?'
    url = baseurl + urllib.urlencode(params)

    webbrowser.open(url)
    tokenListener = Listener()

    while not tokenListener.hasPin():
        ## waits until we have a pin
        pass
    
    ## now that we have the auth code, go get the token
    params = {
        'client_id': 'FILL THIS IN',
        'client_secret': 'FILL THIS IN',
        'grant_type':'authorization_code',
        'code':tokenListener.code,
        'redirect_uri': 'http://localhost:8080', #http://localhost:        
    }
    url = 'https://api.instagram.com/oauth/access_token'
    access_token = json.load(urllib2.urlopen(url,urllib.urlencode(params)))['access_token']
    return access_token

access_token = getAccess()
api = InstagramAPI(access_token=access_token)
media = api.tag_search("snowy",2) 

print media
