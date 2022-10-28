wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh

chmod +x install_pivariety_pkgs.sh

./install_pivariety_pkgs.sh -p imx519_kernel_driver_low_speed


sudo nano /boot/config.txt
#find the line [all]
#manually add dtoverlay=vc4-kms-v3d,cma-256 under it, like this:
[all]
# Run as fast as firmware / board allows
arm_boost=1
dtoverlay=vc4-kms-v3d,cma-256




Open a terminal
2. Run sudo raspi-config
3. Navigate to Advanced Options
4. Enable Glamor graphic acceleration
5. Go back to Advanced Options
6. Navigate to GL Driver
7. Select GL (Full KMS)
8. Reboot your Pi