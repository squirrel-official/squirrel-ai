
https://www.arducam.com/docs/cameras-for-raspberry-pi/64mp-camera-for-raspberry-pi/how-to-use-arducam-64mp-camera-on-rapberry-pi/#forpizero

wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
./install_pivariety_pkgs.sh -p 64mp_pi_hawk_eye_kernel_driver


Open /boot/config.txt, under [all], add the following line( so that it should look like):

[all]
# Run as fast as firmware / board allows
arm_boost=1
dtoverlay=vc4-kms-v3d,cma-512



Edit /boot/cmdline.txt and add cma=800M at the end.


https://www.arducam.com/docs/cameras-for-raspberry-pi/64mp-camera-for-raspberry-pi/how-to-use-arducam-64mp-camera-on-rapberry-pi/#forpizero