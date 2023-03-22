#!/bin/bash
projectDir=backend
DBFileName=db.sqlite3

. ../../venv/bin/activate

cd $projectDir

if [ ! -f "$DBFileName" ]; then
	python3 manage.py migrate
	python3 manage.py loaddata ./fixtures/test/user.json
fi

python3 manage.py runserver '0.0.0.0:8000'
