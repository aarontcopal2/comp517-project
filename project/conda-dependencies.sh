conda create --name Comp517 python=3.6
eval "$(conda shell.bash hook)"
conda activate Comp517

# crawler dependencies
pip install beautifulsoup4
pip install validators
pip install requests
pip install pyodbc