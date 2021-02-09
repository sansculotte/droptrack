#!/usr/bin/env bash

set -e

target_host=${1-"droptrack"}
app_dir=${2-"/opt/droptrack"}
remote_user=${3-"deploy"}
filespace=${4-"$app_dir/data"}

python="python3.8"
build_dir="build"
js_target_dir="webapp/static/js"

# timestamp as version
version="$(date +%Y-%m-%d_%H-%M)"

run_remote() {
    ssh "$remote_user"@"$target_host" "$1"
}

# remove build artefacts
clean() {
    rm -Rf "$build_dir"
    rm -Rf "$js_target_dir/*"
}

# assert basic code quality
# with typechecks and unit tests
check() {
    mypy webapp
    ./run_tests.sh webapp
}

prepare_local() {
    clean
    mkdir -p "$build_dir"
    mkdir -p "$js_target_dir"
    # js dependencies
    npm install
    check
}

build() {
    npm run build
    git archive HEAD | tar -f - -xC "$build_dir"
    cp -a webapp/static/scripts $build_dir/webapp/static/
    cp config.py "$build_dir"/config.py
    find "$build_dir" -iname tests_*.py -execdir rm {} \;
}

prepare_remote() {
    run_remote "mkdir -p $app_dir/_versions/$version"
}

deploy() {

    install_dir="$app_dir/_versions/$version/"

    # transfer files
    scp -r "$build_dir/webapp" "$remote_user"@"$target_host":"$install_dir"
    scp -r "$build_dir/migrations" "$remote_user"@"$target_host":"$install_dir"
    scp -C "$build_dir/config.py" "$remote_user"@"$target_host":"$install_dir"
    scp -C "$build_dir/cli.py" "$remote_user"@"$target_host":"$install_dir"
    scp -C "$build_dir/requirements.txt" "$remote_user"@"$target_host":"$install_dir"

    # install requeirements into remote virtualenv
    run_remote "cd $app_dir/_versions/$version && virtualenv -p $python venv"
    run_remote "cd $app_dir/_versions/$version && ./venv/bin/pip install -r requirements.txt"
    run_remote "cd $app_dir/_versions/$version && ./venv/bin/pip install -r smp-audio-requirements.txt"

    # remove current "current" symlink
    run_remote "if [ -L $app_dir/current ]; then rm $app_dir/current; fi"

    # link new
    run_remote "ln -s $app_dir/_versions/$version $app_dir/current"

    # cleanup, remove old installations, keep 5
    run_remote "cd $app_dir/_versions/ && ls -C1 -t| awk 'NR>5'|xargs rm -Rf"

    # run migrations
    run_remote "cd $app_dir/_versions/$version && FLASK_APP='webapp:create_app()' ./venv/bin/flask db upgrade"

    # restart app server
    run_remote "service uwsgi restart"
}

prepare_local
prepare_remote
build
deploy
