#!/usr/bin/env python3

import functools
import os
import pathlib
import pprint
import pypandoc
import subprocess
import sys


SITE_DIR = 'site'
MD_DIR = 'markdown'
SITEMAP_PATH = 'assets/sitemap.html'
SKIP_DIRS = (
		'.bak',
		'.git',
		'assets',
		'htbin')

def path_to_url(path, depth=None):
	if not path.endswith('.md'):
		raise(Exception(f'Bad Extension: "{path}"'))

	l = path.split(os.sep)
	if depth:
		l = l[-1*depth:]

	if l[0] != MD_DIR:
		raise(Exception(f'Bad path: "{path}"'))

	l[0] = SITE_DIR
	l[-1] = l[-1][:-3] + '.html'
	return '/'.join(l)


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
		string += f'\n<details><summary>{directory}</summary>'
		string = recurse(os.path.join(root, directory), depth+1, string)
		string += '\n<hr>\n</details>'

	if len(files):
		string += '\n<ul>'

	for f in files:
		path = os.path.join(root, f)
		title = get_title(path)
		url = path_to_url(path, depth)
		string += f'\n<li><a href="{url}">{title}</a></li>'

	if len(files):
		string += '\n</ul>'

	return string


def gen_html(title, contents):
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
			</div> <!-- id="sidebar" -->
		</div> <!-- id="container" -->
		<div id="footer">
			<p>This site is <a href="https://github.com/ericdweise/Totally-A-Markdown-Editor"><em>TAME! (Totally A Markdown Editor)</em></a></p>
			<p>Handcrafted by &middot; <a href="https://ericdweise.com">Eric D. Weise</a></p>
		</div> <!-- footer -->
	</body>
</html>'''


def make_sitemap(site_root=MD_DIR, sitemap_path=SITEMAP_PATH):
	sitemap = recurse(site_root, 2, '<h2>Notes</h2>\n<hr>')
	with open(sitemap_path, 'w') as fp:
		fp.write(sitemap)


def make_page(md_path):
	assert(md_path.endswith('.md'))
	html_path = path_to_url(md_path)
	print(f'  {md_path} ---> {html_path}')

	title = get_title(md_path)

	with open(md_path, 'r') as fin:
		_ = fin.readline()
		markdown = fin.read()

	contents = pypandoc.convert_text(
			markdown,
			'html5',
			format='md')
	html = gen_html(title, contents)

	directory, _ = os.path.split(html_path)
	if not os.path.isdir(directory):
		os.makedirs(directory)

	with open(html_path, 'w') as fp:
		fp.write(html)

def make_home():
	title = get_title('README.md')

	with open('README.md', 'r') as fp:
		_ = fp.readline()
		markdown = fp.read()

	contents = pypandoc.convert_text(
			markdown,
			'html5',
			format='md')
	html = gen_html(title, contents)

	with open('index.html', 'w') as fp:
		fp.write(html)


def make_all(site_root=MD_DIR):
	if not os.path.isdir(site_root):
		os.makedirs(site_root)

	make_sitemap(site_root)
	make_home()

	for root, _, files in os.walk(site_root):
		for f in files:
			if not (f.endswith('.md') or f.endswith('.MD')):
				continue

			md_path = os.path.join(root, f)
			make_page(md_path)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		for path in sys.argv[1:]:
			make_page(path, SITE_DIR)
	else:
		make_all(MD_DIR)
