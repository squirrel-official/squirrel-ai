sudo chmod -R 777 /var/log/
#Install Motion
sudo apt-get install motion -y

#Update motion permissions
chmod -R 777 /var/log/motion
chmod -R 777 /var/lib/motion
sudo chmod -R 777 /etc/motion

#enable Motion on reboot
sudo systemctl enable motion






