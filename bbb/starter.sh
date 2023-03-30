
# Solves the problem of not being able to import modules inside the BBB
echo 'export PYTHONPATH=/path/to/bbb:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc


pip3 install -r requirements_bbb.txt