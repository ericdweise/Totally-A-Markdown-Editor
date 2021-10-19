#!/bin/bash

set -euo pipefail


pip3 install -r requirements.txt


# Install locations
SITE_DIR="$HOME/.tame"
TAME_DIR="$HOME/.local/bin"


# Copy site files to the user's home folder
if ! [ -d $SITE_DIR ]; then
	echo "> Making directory $SITE_DIR"
	mkdir -p "$SITE_DIR"
fi

if ! [ -d "$SITE_DIR/markdown" ]; then
	echo "> Making directory $SITE_DIR/markdown"
	mkdir -p "$SITE_DIR/markdown"
fi

echo "> Copying site files to $SITE_DIR"
cp index.html $SITE_DIR
cp README.md $SITE_DIR
cp -r assets $SITE_DIR
cp -r htbin $SITE_DIR


# Copy tame file to somewhere on the $PATH
if ! [[ -d $TAME_DIR ]]; then
	echo "> Making directory $TAME_DIR"
    mkdir -p $TAME_DIR
fi

echo "> copying tame to $TAME_DIR"
cp tame $TAME_DIR

if ! [[ $PATH == *$TAME_DIR* ]]; then
	echo "> Adding $TAME_DIR to the PATH by editing $HOME/.profile"
	echo '' >> "$HOME/.profile"
    echo PATH="$TAME_DIR:$PATH" >> "$HOME/.profile"
fi





