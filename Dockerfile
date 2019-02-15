FROM python

EXPOSE 8000

ARG UID=1000
ARG GID=1000
ARG APPDIR=/twarf
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_SHELL=bash

RUN true \
    && groupadd twarf \
        --gid $GID \
    && useradd twarf \
        --gid $GID \
        --uid $UID \
        --create-home \
        --home-dir $APPDIR

# RUN pip install --requirement requirements-dev.txt
RUN pip install --upgrade pip pipenv tox
COPY --chown=twarf:twarf ./ $APPDIR

USER twarf
WORKDIR $APPDIR
CMD pipenv run python -m twarf
