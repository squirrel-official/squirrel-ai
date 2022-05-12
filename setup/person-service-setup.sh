cd /usr/local/
sudo chmod -R 777 .
sudo apt install maven -y
git clone https://github.com/squirrel-official/person-service.git

sudo chmod -R 777 /usr/local/person-service/src/main/resources/detection.sh

The following command will open a crontab and then append the following line in end

crontab -e

@reboot mvn spring-boot:run -f /usr/local/person-service/pom.xml


Note: The person service downloads the images in the AI folder so AI library installation is important.