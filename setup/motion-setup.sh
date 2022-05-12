sudo chmod -R 777 /var/log/
#Install Motion
sudo apt-get install motion -y

#Add permissions and append the line to bottom of file
sudo visudo
root  ALL=(ALL:ALL) NOPASSWD: /usr/local/person-service/src/main/resources/detection.sh

#Update motion permissions
sudo chmod -R 777 /var/log/motion
sudo chmod -R 777 /var/lib/motion
sudo chmod -R 777 /etc/motion
#enable motion to automatically start and add the following line to bottom of file
sudo crontab -e
@reboot  motion -b

