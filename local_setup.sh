#! /bin/sh
echo "======================================================================"
echo "Setup started"
echo "----------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install python"
    python3 -m venv .env
fi


pip install virtualenv 
pip install --upgrade pip

pip install -r requirements.txt
virtualenv .venv 

deactivate
