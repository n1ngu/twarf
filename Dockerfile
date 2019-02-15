FROM python

EXPOSE 8000

ARG UID=1000
ARG GID=1000
ARG APPDIR=/app
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_SHELL=bash

RUN true \
    && groupadd app \
        --gid $GID \
    && useradd app \
        --gid $GID \
        --uid $UID \
        --create-home \
        --home-dir $APPDIR

# RUN pip install --requirement requirements-dev.txt
RUN pip install --upgrade pip pipenv tox
COPY --chown=app:app ./ $APPDIR

USER app
WORKDIR $APPDIR
CMD pipenv run python -m twarf
