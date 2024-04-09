FROM ubuntu:22.04


RUN apt update && \
    apt install -y --no-install-recommends \
        pandoc \
        python3 \
        python3-pip && \
    mkdir /opt/tame

COPY requirements.txt /opt/tame/requirements.txt

RUN pip3 install -r /opt/tame/requirements.txt

COPY database.py /opt/tame
COPY models.py /opt/tame
COPY note_ops.py /opt/tame
COPY tame.py /opt/tame
COPY templates /opt/tame
COPY static /opt/tame

RUN echo 'notes_directory: "/etc/notes"' > /opt/tame/config.yml

CMD python3 /opt/tame/tame.py
