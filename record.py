#!/usr/bin/env python

import os
import sys
import httplib
import urlparse
import cloudfiles
import urllib
import urllib2
import sys
import pytz

authurl='http://ip/auth'

def application(environ, start_response):
                from datetime import datetime
                our = pytz.timezone('Asia/Novosibirsk')
                i = datetime.now(our)
                _data = urlparse.parse_qs(environ["QUERY_STRING"])

                username = urlparse.parse_qs(environ["QUERY_STRING"])['ceph_api_user'][0]
                api_key = urlparse.parse_qs(environ["QUERY_STRING"])['ceph_api_key'][0]
                api_key = urllib.unquote(api_key).decode('utf8')
                
                container_name = "records" 

                record =  urlparse.parse_qs(environ["QUERY_STRING"])['recording'][0]
                record =  record [1:]
                record = i.strftime('%Y%m%d-%H%M%S') +"_" +record

                conn = cloudfiles.get_connection(
                        username=username,
                        api_key=api_key,
                        authurl=authurl,
                )
                
                length = int(environ["CONTENT_LENGTH"])
                body="Hello world"

                buf = environ['wsgi.input'].read(length)

                testuser = conn.create_container(container_name)
                obj = testuser.create_object(record)
                obj.write(buf)

                start_response("200 Ok",
                 [("Content-Type", "text/html"),
                  ("Content-Length", str(len(body)))])

                return [body]
                

