cd /usr/local/
sudo chmod -R 777 .
sudo apt install maven -y
sudo apt update
sudo apt install openjdk-17-jdk -y
git clone https://github.com/squirrel-official/person-service.git

sudo chmod -R 777 /usr/local/person-service/src/main/resources/detection.sh

The following command will open a crontab and then append the following line in end

crontab -e

@reboot mvn spring-boot:run -f /usr/local/person-service/pom.xml

@reboot java -jar -DEMAIL-PASSWORD=<your_password> /usr/local/person-service/target/person-service-0.0.1-SNAPSHOT.jar>>/usr/local/squirrel-ai/logs/person-application.log
Note: The person service downloads the images in the AI folder so AI library installation is important.