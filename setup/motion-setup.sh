#Install Motion
sudo apt-get install motion

#Add permissions and append the line to bottom of file
sudo visudo
root  ALL=(ALL:ALL) NOPASSWD: /usr/local/person-service/src/main/resources/detection.sh

#Update motion permissions
chmod -R 777 /usr/local/person-service/src/main/resources/detection.sh
chmod -R 777 /var/log/motion
chmod -R 777 /var/lib/motion

#enable motion to automatically start and add the following line to bottom of file
sudo crontab -e
@reboot  motion -b

