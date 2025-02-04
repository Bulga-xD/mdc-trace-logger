#!/usr/bin/env bash

# Resolve links: $0 may be a link
app_path=$0

# Need this for daisy-chained symlinks.
while
  APP_HOME=${app_path%"${app_path##*/}"} # leaves a trailing /; empty if no leading path
  [ -h "$app_path" ]
do
  ls=$(ls -ld "$app_path")
  link=${ls#*' -> '}
  case $link in         #(
  /*) app_path=$link ;; #(
  *) app_path=$APP_HOME$link ;;
  esac
done

APP_HOME=$(cd "${APP_HOME:-./}" && pwd -P) || exit

python -m venv --clear "$APP_HOME"/.venv
source "$APP_HOME"/.venv/bin/activate
python -m pip install --upgrade pip==24.3.1
python -m pip install -e '.[test]'