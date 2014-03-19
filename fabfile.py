from fabric.api import *


env.hosts = ['localhost']


def grunt():
    local('grunt deploy')


def git_add_deploy_assets():
    local('git add --all yausite/deploy/*')


def git_commit():
    local("git commit -m 'Updated deploy assets'")


def heroku_push():
    local("git push heroku master")


def heroku_syncdb():
    local("heroku run python manage.py syncdb")


def heroku_migrate():
    local("heroku run python manage.py migrate")


def deploy():
    grunt()
    git_add_deploy_assets()
    git_commit()
    heroku_push()
    heroku_syncdb()
    heroku_migrate()
