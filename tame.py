#!/usr/bin/env python3

import functools
import os
import pprint
import pypandoc
import subprocess


SKIP_DIRS = (
        '.bak',
        '.git',
        'assets')


def get_title(path):
    with open(path, 'r') as f:
        title = f.readline().strip()

    while title[0] in ('#', ' '):
        title = title[1:]

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
        string += '\n'
        string += '\t'*(depth+1)
        string += f'<li><a href="{path[1:].replace(".md", ".html")}">{title}</a></li>'

    if len(files):
        string += '\n'
        string += '\t'*depth
        string += '</ul>'

    return string


def make_page(title, contents, site_directory):
    return f'''<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>TAME Notes</title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="/assets/stylesheets/main.css">
		<link rel="stylesheet" href="/assets/stylesheets/editor.css">
		<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
		<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
		<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
	</head>
	<body>
		<div id="header">
			<a class="site-title">{title}</a>
		</div> <!-- header -->
		<div id="container" class="clearfix">
			<div id="contents">
				{contents}
			</div> <!-- id="contents" -->
			<div class="spacer"></div>
			<div id="site-dir">
			<div id="view-menu">
				<div class="button">'
					<button id="edit">Edit Markdown</button>'
					<button id="dir">New Directory</button>'
					<button id="file">New File</button>'
				</div> <!-- class="button -->'
			</div> <!-- id="view-menu" -->
			<div id="edit-menu">
				<button id="save">Save</button>
				<button id="abort">Abort Changes</button>
				<button id="vim">VIM</button>
			</div> <!-- id="edit-menu" -->
				{site_directory}
			</div> <!-- id="site-dir" -->
		</div> <!-- id="container" -->
		<div id="footer">
			<p>This site was made with <em>TAME! (Totally A Markdown Editor)</em></p>
			<p>Handcrafted by &middot; <a href="https://ericdweise.com">Eric D. Weise</a></p>
		</div> <!-- footer -->
	</body>
</html>'''


if __name__ == '__main__':
    site_directory = recurse('.', 0, '')

    for root, _, files in os.walk('.'):
        for f in files:
            if not (f.endswith('.md') or f.endswith('.MD')):
                continue

            md_file = os.path.join(root, f)
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
            html = make_page(title, contents, site_directory)

            with open(html_file, 'w') as fp:
                fp.write(html)
