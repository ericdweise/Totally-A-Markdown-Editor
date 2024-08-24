import os

from io import BytesIO
from pathlib import Path

import magic
import pypandoc
import yaml


with open("config.yml", "r") as f:
    CONFIG = yaml.safe_load(f)

if not CONFIG["notes_directory"]:
    raise RuntimeError("No notes_directory specified")

NOTES_DIRECTORY = Path(CONFIG["notes_directory"]).resolve()
if not NOTES_DIRECTORY.is_dir():
    raise RuntimeError(f"Invalid notes directory: {NOTES_DIRECTORY}")

SKIP_DIRS = (
    ".bak",
    ".git",
    "assets",
    "htbin"
)


#######################
# "PRIVATE" FUNCTIONS #
#######################

def _is_path_safe(path):
    resolved_path = path.resolve()
    if not resolved_path.is_relative_to(NOTES_DIRECTORY):
        return False

    return True


def _note2path(note):
    while note and note[0] == "/":
        note = note[1:]

    if not note:
        return None

    path = Path(os.path.join(
        NOTES_DIRECTORY,
        note
    )).resolve()

    if not _is_path_safe(path):
        return None

    if path.is_dir():
        return None

    return path


def _path2note(path):
    return f"{path.relative_to(NOTES_DIRECTORY)}"


def _read_title(path):
    try:
        with path.open("r") as f:
            title = f.readline().strip()
    except Exception:
        title = "<Unknown>"

    if (title is None) or (not len(title)):
        return "<Unknown>"

    return title


def _render_markdown(path):
    with path.open("r") as fp:
        # Discard title line
        _ = fp.readline()

        # Load rest of note
        mdstuff = fp.read()

    html = pypandoc.convert_text(
        mdstuff,
        "html5",
        format="md"
    )

    return html


def _render_textfile(path):
    with path.open("r") as fp:
        return fp.read()


######################
# "PUBLIC" FUNCTIONS #
######################

def make_site_dir(root=None):
    if not root:
        root = NOTES_DIRECTORY

    dirs = []
    files = []
    for item in root.iterdir():
        item = item.resolve()
        if not item.is_relative_to(NOTES_DIRECTORY):
            continue

        if item.name.startswith('.') or item.name.startswith('_'):
            continue

        if item.is_dir():
            dirs.append(item)

        elif item.is_symlink():
            continue

        elif item.is_file():
            if item.suffix.lower() in [".md", ".txt"]:
                note = _path2note(item)
                title = _read_title(item)
                files.append(f'<p><button class="sitedir" onclick="$.fn.changeNote(\'{note}\')">{title}</button></p>')
            elif item.suffix.lower() in [".pdf", ".djvu"]:
                note = _path2note(item)
                title = item.name
                files.append(f'<p><a href="download?file={note}">{title}</a></p>')
            else:
                continue

    output = ""
    dirs.sort()
    files.sort()  # TODO: sort by title, not note
    for directory in dirs:
        if directory in SKIP_DIRS:
            continue

        output += f"\n<details><summary>{directory.name}</summary>"
        output += make_site_dir(directory)
        output += "\n</details>"

    for item in files:
        output += item

    return output


def render_note(note):
    path = _note2path(note)

    # TODO: add tex
    if path.suffix == ".md":
        return _render_markdown(path)
    elif path.suffix == ".txt":
        return _render_textfile(path)
    else:
        print(f"Cannot render '{path}''")
        return ""


def read_note_title(note):
    path = _note2path(note)

    return _read_title(path)


def read_raw_note(note):
    path = _note2path(note)
    with path.open("r") as fp:
        return fp.read()


def save_note(note, contents):
    # TODO: Sanitize contents
    path = _note2path(note)
    with path.open("w") as fp:
        fp.write(contents)


def create_new_note(note):
    path = _note2path(note)
    if path.exists():
        return False

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with path.open("w") as fp:
        fp.write("New Note")

    return True


def get_downloadable_file(note):
    filepath = _note2path(note)
    if not filepath:
        return None, None, None

    filename = os.path.split(filepath)[-1]
    if not filename:
        filename = "tame-download"

    mimetype = magic.from_file(filepath, mime=True)

    with open(filepath, 'rb') as fp:
        filebytes = BytesIO(fp.read())

    return filebytes, filename, mimetype
