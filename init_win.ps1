$AppHome=$PSScriptRoot

python -m venv --clear $AppHome/.venv
.$AppHome/.venv/Scripts/Activate.ps1
python -m pip install --upgrade pip==23.2.1
python -m pip install -e '.[test]'