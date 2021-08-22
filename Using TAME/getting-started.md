Getting Started with TAME


# Using TAME
A quick start guide to 


# Installation
You only need two thing to run TAME on your computer:

1. A modern web browser. Edge, Safari, and Firefox should all work.
2. Python3

## Install Python3
### Ubuntu
```bash
sudo apt install python3 python3-pip
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
As you add Markdown files to your notes directory you can rebuild the site using:
```bash
./htbin/build.py
```


# File Format
TAME stores your notes in Markdown files and displays them in your browser using HTML.

The first line of your Markdown file will be used as the Note title.
The title will be displayed in the site directory and at the top of the page when you open the note.
