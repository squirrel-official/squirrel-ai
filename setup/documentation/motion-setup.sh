sudo chmod -R 777 /var/log/
#Install Motion
sudo apt-get install motion -y

#Add permissions and append the line to bottom of file
sudo visudo

root  ALL=(ALL:ALL) NOPASSWD: /usr/local/person-service/src/main/resources/detection.sh
root  ALL=(ALL:ALL) NOPASSWD: /usr/local/person-service/src/main/resources/motion-restart.sh
pi  ALL=(ALL:ALL) NOPASSWD: /usr/sbin/service  motion stop
pi  ALL=(ALL:ALL) NOPASSWD: /usr/sbin/service  motion start


#Update motion permissions
sudo chmod -R 777 /usr/local/person-service/src/main/resources/detection.sh
sudo chmod -R 777 /usr/local/person-service/src/main/resources/motion-restart.sh
sudo chmod -R 777 /var/log/motion
sudo chmod -R 777 /var/lib/motion
sudo chmod -R 777 /etc/motion


#if unable to connect using  my-security.local then use following command and update the hostname
#from previousname to new hostname

#sudo nano /etc/hostname



