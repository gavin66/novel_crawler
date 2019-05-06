# -*- coding: UTF-8 -*-
from urllib import parse as urlparse

url = 'http://www.b5200.net/97_97046/154425054.html'

str = urlparse.urlsplit(url).path
# urlparse.urlencode(urlparse.urlsplit(link_doc[0]).path)
print(urlparse.urlencode(str))