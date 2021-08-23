#!/usr/bin/env python3

import cgi
import os
import pathlib
import sys

from build import make_all
from build import make_page
from build import make_sitemap


def url_to_path(url):
	NOT_ALLOWED = ('..', '~', '$', '//')

	for pattern in NOT_ALLOWED:
		if pattern in url:
			raise Exception(f'Illegal "{pattern}" in "{url}.')

	assert(url.endswith('.html'))
	url = url[:-5] + '.md'

	while url[0] == '/':
		url = url[1:]

	l = url.split('/')
	if not l[0] == 'site':
		raise(Exception(f'URL bad start: "{url}"'))

	l[0] = 'markdown'

	return os.sep.join(l)


def save_note(target, data):
	assert(target is not None)
	path = url_to_path(target)
	# assert(os.path.isfile(path))

	if not data.endswith('\n'):
		data += '\n'

	if path:
		with open(path,'w') as fp:
			fp.write(data)

	make_page(path)
	make_sitemap()


def new_note(url):
	path = url_to_path(url)
	assert(not os.path.exists(path))
	assert(path.endswith('.md') or path.endswith('.MD'))

	root, _ = os.path.split(path)
	if (root) and (not os.path.exists(root)):
		os.makedirs(root)

	contents = 'New Note\n\n# Welcome\nAdd your thoughts here.\n'
	with open(path, 'w') as fp:
		fp.write(contents)

	make_page(path)
	make_sitemap()


if __name__ == '__main__':
	form = cgi.FieldStorage()
	action = form.getvalue('action', None)

	if action == 'save':
		target = form.getvalue('target', None)
		data = form.getvalue('data', None).replace('\r\n', '\n')
		save_note(target, data)

	elif action == 'new-note':
		target = form.getvalue('target', None)
		new_note(target)

	else:
		raise(Exception(f'Invalid action: "{action}"'))
