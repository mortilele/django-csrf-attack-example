#!/bin/bash

NAME="csrf_example_gunicorn"                                  # Name of the application
GIT_REPO_NAME=django-csrf-attack-example
DJANGODIR=~/${GIT_REPO_NAME}             # Django project directory
SOCKFILE=~/run/gunicorn.sock  # we will communicte using this unix socket
USER="$(whoami)"                                        # the user to run as
NUM_WORKERS=4                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=csrf_example.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=csrf_example.wsgi                    # WSGI module name
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
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name ${NAME} \
  --workers ${NUM_WORKERS} \
  --worker-class=gevent \
  --worker-connections=500 \
  --timeout 60 \
  --user=${USER} \
  --bind=unix:${SOCKFILE} \
  --log-level=debug \
  --log-file=-
