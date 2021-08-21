#!/usr/bin/env python3

import cgi
import os
import pathlib
import sys

from build import make_page, SITE_DIR

form = cgi.FieldStorage()
data = form.getvalue('data','None')
path = os.path.join(pathlib.Path(__file__).parent.absolute(), form.getvalue('target','None'))

if '..' in path:
	raise Exception('Path contains "..".')

if '~' in path:
	raise Exception('Path contains "~".')

while path.startswith('/'):
	path = path[1:]

if path:
	with open(path,'w') as fp:
		fp.write(data)

make_page(path, SITE_DIR)
