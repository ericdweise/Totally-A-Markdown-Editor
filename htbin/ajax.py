#!/usr/bin/env python3

import cgi
import os
import pathlib
import sys

from build import make_all
from build import make_page
from build import make_sitemap
from build import SITE_ROOT


def target_to_path(target):
	NOT_ALLOWED = ('..', '~', '$')

	for pattern in NOT_ALLOWED:
		if pattern in target:
			raise Exception('Path contains "..".')

	assert(target.endswith('.md') or target.endswith('.MD'))

	while target[0] == '/':
		target = target[1:]

	return target


def save_note(target, data):
	assert(target is not None)
	path = target_to_path(target)
	# assert(os.path.isfile(path))

	if not data.endswith('\n'):
		data += '\n'

	if path:
		with open(path,'w') as fp:
			fp.write(data)

	make_page(path)
	make_sitemap()


def new_note(target):
	path = target_to_path(target)
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
