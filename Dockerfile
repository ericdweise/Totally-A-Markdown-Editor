FROM ubuntu:22.04

COPY requirements.txt /opt/tame/requirements.txt
RUN apt update && \
    apt install -y --no-install-recommends \
        libmagic1 \
        pandoc \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install -r /opt/tame/requirements.txt

COPY database.py /opt/tame
COPY models.py /opt/tame
COPY note_ops.py /opt/tame
COPY tame.py /opt/tame
COPY templates /opt/tame/templates
COPY static /opt/tame/static

RUN echo 'notes_directory: "/etc/notes"' > /opt/tame/config.yml

WORKDIR /opt/tame

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0", "tame:create_app()"]
