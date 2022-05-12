
sudo nano /boot/firmware/config.txt
#add the following line in end.
start_x=1

sudo apt update
sudo apt install samba -y

sudo nano /etc/samba/smb.conf
#add the following to file

[squirrel-ai]
  comment = AI service
  path = /usr/local/squirrel-ai
  read only = no
  browsable = yes

[person-service]
  comment = person service
  path = /usr/local/person-service
  read only = no
  browsable = yes

[motion-service]
  comment = motion service
  path = /var/lib/motion
  read only = no
  browsable = yes

[motion-config]
  comment = motion service
  path = /etc/motion/
  read only = no
  browsable = yes


#create password
sudo smbpasswd -a pi

sudo service smbd restart