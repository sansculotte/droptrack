from datetime import datetime
import os
from os.path import join
from fabric.api import task, run, cd, env, lcd, sudo, put, local


local_app_dir       = os.path.dirname(os.path.realpath(__file__))
local_js_src_dir    = join(local_app_dir, 'webapp-js')
local_js_target_dir = join(local_app_dir, 'webapp/static/scripts')
remote_base_dir     = '/opt/droptrack'
remote_app_dir      = '/opt/droptrack/_versions/{0}'.format(datetime.now().strftime('%F_%H-%M'))
remote_config_dir   = '/opt/droptrack/config'
remote_current_dir  = '/opt/droptrack/current'
local_build_dir     = 'build'
revision            = local('git rev-parse --short HEAD', capture=True)
branch              = local('git branch --no-color 2> /dev/null | sed -e \'/^[^*]/d\' -e \'s/* \(.*\)/\\1/\'', capture=True)

# access definitions from .ssh/config
env.use_ssh_config = True
env.shell = '/usr/bin/env bash -l -c'
env.www_user = 'www'
env.www_group = 'www'
env.target = 'local'
env.logfile = None
env.errorfile = None


@task
def test_ssh():
    run('echo $(whoami)@$(hostname)')


@task
def test():
    local("./run_tests.sh -q -x webapp")


@task
def clean():
    local('rm -Rf {}/*'.format(local_build_dir))
    local('rm -Rf {}/*'.format(local_js_target_dir))


@task
def node_deps():
    local("npm install")


@task
def build_js():
    local("mkdir -p {}".format(local_js_target_dir))
    local("npm run test && npm run build")


@task
def assets():
    node_deps()
    build_js()


@task
def prepare_deploy():
    test()
    build()


def prepare_build():
    local('mkdir -p %s' % (local_build_dir))
    clean()


@task
def build():
    print("Building %s" % revision)
    prepare_build()
    print('skipping assets. nothing to do yet')
    # assets()
    local('git archive HEAD | tar -f - -xC {}'.format(
        os.path.join(local_app_dir, local_build_dir)
    ))
    local('cp -a {0}/webapp/static/scripts {1}/webapp/static/'.format(
        local_app_dir,
        local_build_dir
    ))
    set_version()
    local('rm -Rf %s/webapp-js' % local_build_dir)
    local('rm -Rf %s/etc' % local_build_dir)
    local('rm -Rf %s/webapp/data/test' % local_build_dir)
    local('find %s -iname tests_*.py -execdir rm {} \;' % local_build_dir)


def set_version():
    local('sed "s/{{COMMIT_HASH}}/%s/" %s/config.py.dist > %s/config.py' \
          % (revision, local_build_dir, local_build_dir))


# pass version like: fab package:version=<version>
@task
def package(version='test'):
    package_name      = 'droptrack-%s'%(version)
    local_package_dir = 'build/%s'%package_name
    print("Building %s" % revision)
    local('mkdir -p %s/' % (local_package_dir))
    local('rm -Rf %s/*' % (local_package_dir))
    local('git archive HEAD | tar -f - -xC %s/%s' % (local_app_dir, local_package_dir))
    set_version()
    local('rm -Rf %s/tests' % (local_package_dir))
    local('cd %s && tar zcf %s.tar.gz %s' % (local_build_dir, package_name, package_name))


@task
def production():
    env.target = 'production'
    env.hosts = ['droptrack']
    env.user = 'deploy'
    env.password = 'password'
    env.app_env = "config.ProductionConfig" # flasks config environment
    env.secrets = '/opt/droptrack/config/secrets'
    env.logfile = '/opt/droptrack/logs/app.log'
    env.errorfile = '/opt/droptrack/logs/error.log'


@task
def staging():
    env.target = 'staging'
    env.hosts = ['droptrack']
    env.user = 'deploy'
    env.app_env = "config.StagingConfig" # flasks config environment
    env.secrets = '/opt/droptrack/config/secrets'
    env.logfile = '/opt/droptrack/logs/app.log'
    env.errorfile = '/opt/droptrack/logs/error.log'


@task
def deploy():
    with lcd(local_app_dir):
        prepare_deploy()
        run('mkdir -p %s' % (remote_app_dir))
        with cd(remote_app_dir):
            copy_files()
            python_setup()
            sudo('chgrp {0} {1}'.format(env.www_group, remote_app_dir))
            # link to new current version
            run('if [ -L %s ]; then rm %s; fi' % (remote_current_dir, remote_current_dir))
            run('ln -s %s %s' % (remote_app_dir, remote_current_dir))
            # delete old versions
            sudo("cd /opt/droptrack/_versions && ls -C1 -t| awk 'NR>5'|xargs rm -Rf")
    restart()


@task
def python_setup():
    run('/usr/bin/env bash ./setup.sh')


@task
def copy_files():
    put('build/*', './')


@task
def rollback():
    with cd(remote_base_dir):
        versions = run(
            'for f in _versions/*; do echo $f; done'
        ).split()
        if len(versions) > 1:
            versions = sorted(versions)[::-1]
            rollback_version = versions[1]
            run('if [ -L "{0}" ]; then rm "{0}"; fi'.format(remote_current_dir))
            run('ln -s %s %s' % (rollback_version, remote_current_dir))
            restart()
        else:
            print("no version to roll back to")

@task
def restart():
    sudo('service uwsgi restart', shell=False)
