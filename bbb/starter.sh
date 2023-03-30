
# Solves the problem of not being able to import modules inside the BBB
echo 'export PYTHONPATH=/path/to/bbb:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc


pip3 install -r requirements_bbb.txt



# Setting up the service for the API on beaglebone black
sudo mv /home/debian/bbb/configs/api.service /etc/systemd/system/api.service

# exports PYTHONPATH, removes all api.py active instances, and runs api.py
chmod +x /home/debian/bbb/scripts/start_api.sh 

sudo systemctl daemon-reload
sudo systemctl enable api.service
sudo systemctl start api.service


# Check the status of the service
# sudo systemctl status api.service

# Check the logs of the service
# sudo journalctl -u api.service --no-pager --reverse | head -n 20
# sudo journalctl -u api.service --no-pager | tail -n 20