
sudo nano /boot/firmware/config.txt
#add the following line in end.
start_x=1

sudo apt update
sudo apt install samba -y

sudo nano /etc/samba/smb.conf
#add the following to file

[AI]
    comment = AI
    path = /usr/local/squirrel-ai
    read only = no
    browsable = yes
[Person-Service]
    comment = Person-Service
    path = /usr/local/person-service
    read only = no
    browsable = yes
[Motion-Config]
    comment = Motion-Config
    path = /etc/motion
    read only = no
    browsable = yes
[Captured-Videos]
    comment = Captured-Videos
    path = /var/lib/motion
    read only = no
    browsable = yes


#create password
sudo smbpasswd -a pi

sudo service smbd restart