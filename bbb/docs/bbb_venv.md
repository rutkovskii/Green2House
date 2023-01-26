## Setting up and using a virtual environment in BBB
### Install venv on Debian of BBB (Not sure, must double check)
    sudo apt-get install python3-venv

### Create venv (inside root folder on BBB)  
    python3 -m venv venv

### Activate venv
    source venv/bin/activate

### Proceed to BBB folder
    cd bbb

### Install dependencies 
    pip install -r requirements_bbb.txt
    or 
    pip3 install -r requirements_bbb.txt

### Deactivate venv (when finished working)
    deactivate


## Dependency management
### Install new dependency
    pip install <package_name>
    or 
    pip3 install <package_name>

### Save new dependency to requirements_bbb.txt (to be done from bbb folder)
    pip freeze > requirements_bbb.txt
    or 
    pip3 freeze > requirements_bbb.txt


### Uninstall dependency
    pip uninstall <package_name>
    or 
    pip3 uninstall <package_name>