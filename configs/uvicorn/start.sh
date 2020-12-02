#!/bin/bash

NAME="csrf_example"                                  # Name of the application
GIT_REPO_NAME=django-csrf-attack-example
DJANGODIR=~/${GIT_REPO_NAME}             # Django project directory
SOCKFILE=~/run/uvicorn.sock  # we will communicte using this unix socket
USER="$(whoami)"                                        # the user to run as
DJANGO_SETTINGS_MODULE=csrf_example.settings             # which settings file should Django use
DJANGO_ASGI_MODULE=csrf_example.asgi                     # WSGI module name
ENV_PATH=~/envs/${GIT_REPO_NAME}

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ${ENV_PATH}/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec uvicorn ${DJANGO_ASGI_MODULE}:application \
  --uds=${SOCKFILE} \
  --log-level=debug