
#https://linuxhint.com/install-jellyfin-raspberry-pi/

sudo apt update && sudo apt upgrade

sudo wget -O- https://repo.jellyfin.org/jellyfin_team.gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/jellyfin.gpg

echo "deb [arch=$( dpkg --print-architecture ) signed-by=/usr/share/keyrings/jellyfin.gpg] https://repo.jellyfin.org/debian bullseye main" | sudo tee /etc/apt/sources.list.d/jellyfin.list

sudo apt update

sudo apt install jellyfin

jellyfin --version

systemctl status jellyfin

sudo systemctl enable jellyfin
