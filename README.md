Fortschritt Impfzertifikat, live vom PI 4 mit PI OS lite

In manchen Dokumenten ist ein Personal Access Token zu lesen. Deshalb kann dieses Repository in dieser Form vorerst(!) nicht veröffentlicht werden.
Eine öffentliche Version wird folgen!

## Ausrüstung

RasPI 4, PI Camera v2, Ethernet, Monitor, Tastatur
Image: PI OS Lite via [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
Auf dem PI: Alles als Root-User durchführen

# Konfigschritte

## notwendigerweise bekannte Git-Befehle

### Initial

``` sh
- git init
- git checkout branch
- git clone
- git pull
```

```
git config --global user.name "Jonathan"
git config --global user.email "26322754+nukerxy@users.noreply.github.com"
git push
```

wenn schon ein commit mit falschen Daten vorhanden:

```
git commit --amend --reset-author
```
### Aktuellen Stand speichern

``` sh
git checkout branch
<Make some changes>
git add .
git commit -m "message"
git push [-f]
```
### Sonstige (Zeilen einzeln lesen)

```
git status
git reset
git checkout -- file.extension
git push --set-upstream origin branchname
history > history.txt
```

## Aktualisierung und Tools holen

``` sh
apt update
apt upgrade
apt install python3-pip git -y
```

## Installation Repositories

```sh
cd /home/pi
git clone https://github.com/panzi/verify-ehc
cd /home/pi/verify-ehc
pip3 install -r requirements.txt
cd /home/pi/
git clone https://TOKEN@github.com/nukerxy/emb-impf.git
pip3 install opencv-python
```
(oder apt install python3-opencv) ?

## Dependencies nachinstallieren

``` sh
apt install libqt4-test python3-sip python3-pyqt5 libqtgui4 libjasper-dev libatlas-base-dev
```
und noch dazu:

```
pip3 install opencv-contrib-python==4.1.0.25
apt install libzbar0
```
## Kamera einrichten

``` sh
raspi-config
```
In GUI Kamera aktivieren --> Welche Änderung in File TODO

ggf ist
``` sh
modprobe bcm2835_v4l2 / modprobe bcm2835-v4l2
```
nötig

Es gab eine komische Fehlermeldung bei `modprobe bcm2835_v4l2`
```sh
modprobe: ERROR: ../libkmod/libkomd.c:586 kmod_search_moddep() could not open moddep file '/lib/modules/5.10.17-71+/modules.dep.bin'
modprobe: FATAL: MOdule bcm3825_v4l2 not found in directory /lib/modules/5.10.17-v71+
```

daher wurde
``` sh
apt install --reinstall raspberrypi-bootloader
apt install --reinstall raspberrypi-kernel
```
ausgeführt, das hat es soweit repariert.

## Autostart

``` sh
cd /etc/init.d
nano impfe.sh
chmod 777 impfe.sh
sudo update-rc.d impfe.sh defaults
```
