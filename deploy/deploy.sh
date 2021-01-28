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

clean() {
    rm -Rf "$build_dir"
    rm -Rf "$js_target_dir/*"
}

prepare_local() {
    clean
    mkdir -p "$build_dir"
    mkdir -p "$js_target_dir"
    # js dependencies
    npm install
    # check
    mypy webapp
    ./run_tests.sh webapp
}

build() {
    npm run build
    git archive HEAD | tar -f - -xC "$build_dir"
    cp -a webapp/static/scripts $build_dir/webapp/static/
    cp config.py.dist "$build_dir"/config.py
    find "$build_dir" -iname tests_*.py -execdir rm {} \;
}

prepare_remote() {
    if [[ ! $(run_remote "ls $app_dir") ]]; then
        echo "Please create install dir $app_dir"
        exit
    fi
    if [[ ! $(run_remote "ls $app_dir/_versions") ]]; then
        echo "Please create install dir $app_dir/_versions"
        exit
    fi
    run_remote "mkdir $app_dir/_versions/$version"
}

deploy() {

    install_dir="$app_dir/_versions/$version/"

    # transfer files
    scp -r "$build_dir/webapp" "$remote_user"@"$target_host":"$install_dir"
    scp -C "$build_dir/config.py" "$remote_user"@"$target_host":"$install_dir"
    scp -C "$build_dir/cli.py" "$remote_user"@"$target_host":"$install_dir"
    scp -C "$build_dir/requirements.txt" "$remote_user"@"$target_host":"$install_dir"

    run_remote "cd $app_dir/_versions/$version && virtualenv -p $python venv"
    run_remote "cd $app_dir/_versions/$version && ./venv/bin/pip install -r requirements.txt"

    # remove current "current" symlink
    run_remote "if [ -L $app_dir/current ]; then rm $app_dir/current; fi"

    # link new
    run_remote "ln -s $app_dir/_versions/$version $app_dir/current"

    # cleanup, remove old installations, keep 5
    run_remote "cd $app_dir/_versions/ && ls -C1 -t| awk 'NR>5'|xargs rm -Rf"

    # run migrations
    run_remote "cd $app_dir/_versions/$version && .venv/bin/flask db upgrade"

    # restart app server
    run_remote "service uwsgi restart"
}

prepare_local
prepare_remote
build
deploy
