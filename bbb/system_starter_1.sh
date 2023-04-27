# Sets up the bbb

# Solves the problem of not being able to import modules inside the BBB
echo 'export PYTHONPATH=/path/to/bbb:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc

# Installs the required packages for the BBB
pip3 install -r requirements_bbb.txt

# Setting up the service for the API on beaglebone black
sudo mv /home/debian/bbb/configs/api.service /etc/systemd/system/api.service

# Makes the system_runner_2.sh executable
# system_runner_2.sh — Exports PYTHONPATH, removes all main.py active instances, and runs main.py
chmod +x /home/debian/bbb/system_runner_2.sh

# Reloads the daemon, enables the service, and starts the service
sudo systemctl daemon-reload
sudo systemctl enable api.service
sudo systemctl start api.service



# Helpful commands:
    # Check the status of the service
    # sudo systemctl status api.service

    # Check the logs of the service
    # sudo journalctl -u api.service --no-pager --reverse | head -n 20
    # sudo journalctl -u api.service --no-pager | tail -n 20