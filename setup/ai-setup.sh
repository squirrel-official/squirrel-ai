# Ubuntu 22.04 server 64 bit
cd /usr/local/
sudo chmod -R 777 .

sudo apt update
sudo apt install python3-pip -y
sudo apt-get install libjpeg-dev zlib1g-dev  -y
sudo apt-get install libssl-dev -y
sudo apt-get install libgtk2.0-dev -y
sudo apt-get install pkg-config -y
sudo apt-get install ffmpeg libsm6 libxext6  -y
sudo apt-get update
sudo apt-get install -y cmake

pip3 install Pillow
pip3 install dlib --force-reinstall --no-cache-dir --global-option=build_ext
pip3 install face_recognition -v
pip3 install opencv-contrib-python -v
sudo apt-get install -y python3-opencv

pip3 install tflite-support
sudo apt install python3-h5py -y
pip3 install tensorflow-aarch64

mkdir /usr/local/squirrel-ai/wanted-criminals
mkdir  /usr/local/squirrel-ai/captured
mkdir  /usr/local/squirrel-ai/logs
mkdir /usr/local/squirrel-ai/visitor
mkdir /usr/local/squirrel-ai/archives

sudo chmod -R 777 .