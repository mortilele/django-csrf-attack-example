from . import common
from . import install

from dotenv import load_dotenv
from fabric.decorators import task
from fabric.state import env

import os

load_dotenv()

env.repository = "https://github.com/mortilele/django-csrf-attack-example.git"
env.repository_ssh = "https://github.com/mortilele/django-csrf-attack-example.git"
env.repo_name = "django-csrf-attack-example"
env.user = "root"
# env.key_filename = "~/work/key/event_service.pem"
env.hosts = [""]


@task
def dev():
    env.config = 'Base'
    env.password = os.getenv('DEV_PASSWORD', None)
    env.hosts = '165.22.75.158'
    env.environ = 'dev'
    env.dotenv_path = '{}/.env'.format(env.repo_name)
    env.key_filename = "/home/mars/.ssh/id_rsa"