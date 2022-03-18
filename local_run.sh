#! /bin/sh
echo "======================================================================"
echo "Running started" 
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env

export FLASK_APP=main.py     
export FLASK_DEBUG=1
flask run

deactivate
