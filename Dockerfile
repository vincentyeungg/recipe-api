FROM python:3.9-alpine3.13
LABEL maintaner="ahjoo123"

# don't buffer output
ENV PYTHONUNBUFFERED 1

# copy over local requirements file
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copy over local django app
COPY ./app /app
# run commands on docker image from directory with django app
WORKDIR /app
# expose port to access django dev server
EXPOSE 8000

# intial arg DEV set to false
# this flag will be updated in the docker-compose file
ARG DEV=false

RUN python -m venv /py && \
    # upgrade pip version inside venv
    /py/bin/pip install --upgrade pip && \
    # install dependencies from the requirements file inside venv
    /py/bin/pip install -r /tmp/requirements.txt && \
    # basic shell command, install requirements.dev.txt when DEV is false, and will be false when we run dev server
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # can remove the /tmp file after dependencies are installed
    rm -rf /tmp && \
    # access the server system with another user instead of the root user
    # limits our user to certain privileges instead in case of system compromise
    adduser \
        --disabled-password \
        --no-create-home \
        # new user name
        django-user

ENV PATH="/py/bin:$PATH"

# specifies the user we are switching to
USER django-user
