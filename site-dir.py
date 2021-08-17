#!/usr/bin/env python3

import functools
import os
import pprint


def get_title(path):
    with open(path, 'r') as f:
        title = f.readline().strip()

    while title[0] in ('#', ' '):
        title = title[1:]

    if not len(title):
        title = 'Unknown'

    return title


def toc_recurse(root, depth, string):
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
        if directory == 'assets':
            continue
        if directory == '.bak':
            continue
        string += '\n'
        string += '\t'*depth
        string += f'<details><summary>{directory}</summary>'
        string = toc_recurse(os.path.join(root, directory), depth+1, string)
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


if __name__ == '__main__':
    string = toc_recurse('.', 0, '')
    print(string)
