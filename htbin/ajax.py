#!/usr/bin/env python3

import cgi
import os
import pathlib
import pypandoc
import sys

from build import make_all
from build import make_page
from build import make_sitemap
from build import get_title


MD_DIR = 'markdown'
SKIP_DIRS = (
		'.bak',
		'.git',
		'assets',
		'htbin')


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


def sitedir(root, string):
	dirs = []
	files = []
	for i in os.listdir(root):
		if os.path.isdir(os.path.join(root, i)):
			dirs.append(i)
		elif os.path.isfile(os.path.join(root, i)):
			if not i.endswith('.md'):
				continue
			files.append(i)

	dirs.sort()
	files.sort()

	for directory in dirs:
		if directory.startswith('.') or directory.startswith('_') or directory in SKIP_DIRS:
			continue
		string += f'\n<details><summary>{directory}</summary>'
		string = sitedir(os.path.join(root, directory), string)
		string += '\n<hr>\n</details>'

	if len(files):
		string += '\n<ul>'

	for f in files:
		path = os.path.join(root, f)
		title = get_title(path)
		string += f'\n<li><a onclick="$.fn.loadNote(\'{path}\')">{title}</a></li>'

	if len(files):
		string += '\n</ul>'

	return string


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

	elif action == 'site-directory':
		print("Content-Type: text/html")
		print()
		print(sitedir(MD_DIR, ''))

	elif action == 'load-note':
		note_path = form.getvalue('note-path')
		with open(note_path, 'r') as fp:
			mdstuff = fp.read()

		print("Content-Type: text/html")
		print()
		print(pypandoc.convert_text(
			mdstuff,
			'html5',
			format='md'))

	else:
		raise(Exception(f'Invalid action: "{action}"'))
