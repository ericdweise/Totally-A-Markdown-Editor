#!/usr/bin/env python3

import functools
import os
import pprint
import pypandoc
import subprocess
import sys


SKIP_DIRS = (
		'.bak',
		'.git',
		'assets',
		'htbin')


def get_title(path):
	with open(path, 'r') as f:
		title = f.readline().strip()

	if len(title):
		while title[0] in ('#', ' '):
			if len(title) > 1:
				title = title[1:]
			else:
				break

	if not len(title):
		title = 'Unknown'

	return title


def recurse(root, depth, string):
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
		string += '\n'
		string += '\t'*depth
		string += f'<details><summary>{directory}</summary>'
		string = recurse(os.path.join(root, directory), depth+1, string)
		string += '\n'
		string += '\t'*depth
		string += '<hr>'
		string += '\n'
		string += '\t'*depth
		string += '</details>'

	if len(files):
		string += '\n'
		string += '\t'*depth
		string += '<ul>'

	for f in files:
		path = os.path.join(root, f)
		title = get_title(path)
		l = path.split(os.sep)
		url = '/' + '/'.join(l[-1*depth-1:])
		url = url.replace('.md', '.html')
		string += '\n'
		string += '\t'*(depth+1)
		string += f'<li><a href="{url}">{title}</a></li>'

	if len(files):
		string += '\n'
		string += '\t'*depth
		string += '</ul>'

	return string


site_root = os.path.realpath(__file__)
site_root = os.path.split(site_root)[0]
site_root = os.path.split(site_root)[0]
SITE_DIR = recurse(f'{site_root}', 0, '')


def make_html(title, contents, site_directory):
	return f'''<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>&#x1F989; - {title}</title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="/assets/stylesheets/main.css">
		<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
		<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
		<script src="/assets/javascript/editor.js"></script>
		<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
	</head>
	<body>
		<div id="header">
			<p class="site-title">{title}</p>
		</div> <!-- header -->
		<div id="container" class="clearfix">
			<div id="contents">
				<div id="view-menu">
					<button id="edit">Edit Markdown</button>
					<button id="file">New Note</button>
				</div> <!-- id="view-menu" -->
				<div id="edit-menu" class="hidden">
					<button id="save">Save</button>
					<button id="abort">Abort</button>
				</div> <!-- id="edit-menu" -->
				<div id="viewer">
					{contents}
				</div> <!-- id="viewer" -->
				<div id="editor" contenteditable="true" class="hidden">
				</div> <!-- id="editor" -->
			</div> <!-- id="contents" -->
			<div class="spacer"></div>
			<div id="sidebar">
				<h2>Notes</h2>
				<hr>
				{site_directory}
			</div> <!-- id="sidebar" -->
		</div> <!-- id="container" -->
		<div id="footer">
			<p>This site was made with <em>TAME! (Totally A Markdown Editor)</em></p>
			<p>Handcrafted by &middot; <a href="https://ericdweise.com">Eric D. Weise</a></p>
		</div> <!-- footer -->
	</body>
</html>'''


def make_page(md_file, site_directory):
	assert(md_file.endswith('.md'))

	html_file = md_file.replace('.md', '.html')
	print(f'  {md_file} ---> {html_file}')

	title = get_title(md_file)

	with open(md_file, 'r') as fin:
		_ = fin.readline()
		markdown = fin.read()

	contents = pypandoc.convert_text(
			markdown,
			'html5',
			format='md')

	html = make_html(title, contents, site_directory)

	with open(html_file, 'w') as fp:
		fp.write(html)


def make_all():
	for root, _, files in os.walk('.'):
		for f in files:
			if not (f.endswith('.md') or f.endswith('.MD')):
				continue

			md_file = os.path.join(root, f)
			make_page(md_file, SITE_DIR)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		for path in sys.argv[1:]:
			make_page(path, SITE_DIR)
	else:
		make_all()
