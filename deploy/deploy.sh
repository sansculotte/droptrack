#!/usr/bin/env bash

set -e

target_host=${1-"droptrack"}
install_dir=${2-"/opt/droptrack"}
remote_user=${3-"deploy"}
filespace=${4-"$install_dir/data"}

python="python3.8"
build_dir="build"
js_target_dir="webapp/static/js"

# timestamp as version
version="$(date +%s)"

run_remote() {
    ssh "$remote_user"@"$target_host" "$1"
}

clean() {
    rm -Rf "$build_dir"
    rm -Rf "$js_target_dir/*"
}

prepare() {
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
    if [[ ! $(run_remote "ls $install_dir") ]]; then
        echo "Please create install dir $install_dir"
        exit
    fi
    if [[ ! $(run_remote "ls $install_dir/_versions") ]]; then
        echo "Please create install dir $install_dir/_versions"
        exit
    fi
    run_remote "mkdir $install_dir/_versions/$version"
}

deploy() {
    
    # transfer files
    scp -r "$build_dir/webapp" "$remote_user"@"$target_host":"$install_dir/_versions/$version"

    run_remote "cd $install_dir/_versions/$version \
                && virtualenv -p $python venv\
                && ./venv/bin/pip install -r requirements.txt"

    # remove current "current" symlink
    run_remote "if [ -L $install_dir/current ]; then rm $install_dir/current; fi"

    # link new
    run_remote "ln -s $install_dir/_versions/$version $install_dir/current"

    # cleanup, remove old installations, keep 5
    run_remote "cd $install_dir/_versions/ && ls -C1 -t| awk 'NR>5'|xargs rm -Rf"

    # run migrations
    run_remote "cd $install_dir/_versions/$version && .venv/bin/flask db upgrade"

    # restart app server
    run_remote "service uwsgi restart"
}

prepare
build
deploy
