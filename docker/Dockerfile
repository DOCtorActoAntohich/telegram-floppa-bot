FROM python:3.10-alpine
WORKDIR /app


# Environment.
COPY ./docker/requirements.txt ./requirements.txt
RUN python -m venv .venv
RUN .venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel
RUN .venv/bin/python -m pip install --no-cache-dir -r ./requirements.txt
RUN rm ./requirements.txt


# Bot stuff.
COPY ./floppa ./floppa


# root evil.
RUN addgroup -S cats && adduser -S floppa -g cats

# Change owner of work dir to allow for neat triks, and kill warnings.
RUN chown floppa:cats /app

# root evil, part 2.
USER floppa


# Let's go do some casual chatting (and have fun).
ENTRYPOINT .venv/bin/python -m floppa.main
