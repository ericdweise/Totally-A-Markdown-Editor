#!/usr/bin/env python3

import cgi
import os
import pathlib
import pypandoc
import re
import sys

from collections import OrderedDict


MD_DIR = 'markdown'
SKIP_DIRS = (
		'.bak',
		'.git',
		'assets',
		'htbin')


def get_title(md_path):
	with open(md_path, 'r') as f:
		title = f.readline().strip()

	if (title is None) or (not len(title)):
		return 'Unknown'

	if len(title):
		while title[0] in ('#', ' '):
			if len(title) > 1:
				title = title[1:]
			else:
				title = 'Unknown'

	return title


def sanitize_path(path):
	NOT_ALLOWED = ('..', '~', '$', '//')
	for pattern in NOT_ALLOWED:
		if pattern in path:
			raise Exception(f'Illegal "{pattern}" in "{path}.')

	while path[0] == '/':
		path = path[1:]

	l = path.split('/')

	return os.sep.join(l)


def save_note(target, data):
	sanitize_path(target)
	assert(target is not None)
	assert(os.path.isfile(target))

	if not data.endswith('\n'):
		data += '\n'

	if target:
		with open(target,'w') as fp:
			fp.write(data)


def new_note(path):
	sanitize_path(path)
	assert(not os.path.exists(path))
	assert(path.endswith('.md') or path.endswith('.MD'))

	root, _ = os.path.split(path)
	if (root) and (not os.path.exists(root)):
		os.makedirs(root)

	contents = 'New Note\n\n# Welcome\nAdd your thoughts here.\n'
	with open(path, 'w') as fp:
		fp.write(contents)


def load_md_with_toc(note_path):
	toc = []
	contents = []
	with open(note_path, 'r') as fp:
		# Discard title line
		_ = fp.readline()

		# Load rest of note
		for line in fp:
			if line.startswith('#'):
				heading = line.strip()
				indent = -1
				while heading.startswith('#'):
					heading = heading[1:]
					indent += 1
				while heading[0] == ' ':
					heading = heading[1:]
				tag = heading.replace(' ', '-')
				tag = re.sub('[^a-zA-Z0-9\-_]', '', tag)
				tag = '#' + tag.lower()
				toc.append('\t'*indent + f'- [{heading}]({tag})')

			contents.append(line)

	if len(contents):
		return '# Contents\n\n' + '\n'.join(toc) + '\n' + ''.join(contents)
	else:
		return ''


def load_markdown(note_path):
	with open(note_path, 'r') as fp:
		# Discard title line
		_ = fp.readline()

		# Load rest of note
		mdstuff = fp.read()

	return mdstuff


def sitedir(root, output):
	dirs = []
	files = {}
	for item in os.listdir(root):
		if os.path.isdir(os.path.join(root, item)):
			dirs.append(item)
		elif os.path.isfile(os.path.join(root, item)):
			if not item.endswith('.md'):
				continue
			filepath = os.path.join(root, item)
			title = get_title(filepath)
			while title in files.keys():
				title += ' [duplicate]'
			files[title] = filepath

	dirs.sort()
	for directory in dirs:
		if directory.startswith('.') or directory.startswith('_') or directory in SKIP_DIRS:
			continue
		output += f'\n<details><summary>{directory}</summary>'
		output = sitedir(os.path.join(root, directory), output)
		output += '\n</details>'

	for item in sorted(files.items()):
	    output += f'\n<p><a href="?path={item[1]}">{item[0]}</a></p>'

	return output


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
		mdstuff = load_md_with_toc(note_path)

		print("Content-Type: text/html")
		print()
		print(pypandoc.convert_text(
			mdstuff,
			'html5',
			format='md'))

	elif action == 'get-title':
		note_path = form.getvalue('note-path')

		print("Content-Type: text/html")
		print()
		print(get_title(note_path))

	else:
		raise(Exception(f'Invalid action: "{action}"'))
