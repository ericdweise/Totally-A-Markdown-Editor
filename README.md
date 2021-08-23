TAME is Totally A Markdown Editor!

Hi, there!
You've discovered _TAME_,the most docile markdown editor on the web. 
I created this because I was frustrated with all the other options out there.
These were either:

1. Aggressive memory and power consumers, and
2. Greedy, and wanted to steal my data or sell me services.

You won't find anything fancy in this domesticated environment, but you will be able to edit whatever you like.
_And_, we won't steal your data; It's all yours!
(Just make sure to back it up...)


# Installation
You only need two thing to run TAME on your computer:

1. A modern web browser. Edge, Safari, and Firefox should all work.
2. Python3

## Install Python3
```bash
sudo apt install git python3 python3-pip
```

## Clone TAME
```bash
git clone https://github.com/ericdweise/Totally-A-Markdown-Editor.git
```

## Install Python Libraries
```bash
pip3 install -r requirements.txt
```


# Running Tame
## Starting Your Webserver
From the root of the Git repository use this command:
```bash
./run
```

## Building Your Notes Website
As you add Markdown files to your notes directory you can rebuild the HTML files using:
```bash
./htbin/build.py
```


# Writing Your Notes
## Adding Git Version Controlled Notes as a Submodule
```bash
git submodule add <REPOSITORY_URL> markdown
```

## Copying Markdown Files
Create a folder called `markdown` and add your Markdown files here.

## TAME Specifics
TAME stores your notes in Markdown files and displays them in your browser using HTML.

The first line of your Markdown file will be used as the Note title.
The title will be displayed in the site directory and at the top of the page when you open the note.


# License
TAME - Totally A Markdown Editor
Copyright (C) 2021 Eric D. Weise

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Ongoing Work
- New background photo
- Add ajax response when a note has been successfully saved. Reload page after receipt, print error if there was an error.
- Add arguments to `run`: bind addresses, port
