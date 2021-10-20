# Über

Mit diesem Projekt wird ein primitver Scanner von EU-Health-Certificates auf einem Raspberry PI realisiert.

## Ausrüstung

Raspberry PI 4 B, PI Camera v2, Ethernet, Monitor, Tastatur
Image: PI OS Lite via [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
Alles als Root-User durchführen.

## Ordnerstruktur

Die Dateien wurden folgendermaßen angelegt:
verify-ehc/ wurde [geklont](https://github.com/panzi/verify-ehc). Dabei wurde `verify-ehc.py` geringfügig manipuliert (siehe unten.)
```
path_to_folder/
├── verify-ehc/ #geklontes Repository
│   ├── trustlist-cbor.schema.json
│   ├── trustlist-json.schema.json
│   ├── verify_ehc.py #verändert
│   └── trust_list.cbor #heruntergeladen via command
└── emb-impf/ #geklontes Repository
    └── barcodescanner.py
```
```
etc/
└── init.d/
    └── impfe.sh
```

Im konkreten Fall gilt hier:
```sh
path_to_folder/=home/pi/
```

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

wenn schon ein commit mit falschen Daten vorhanden war:

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

## Änderungen an verify-ehc/

### Modifikationen verify_ehc.py
zu beginn
```python
from gpiozero import LED
```
in
`verify_ehc([...]]) -> bool:`

Zu Beginn, timedelta wurde hinzugefügt, Zeile 1684 \
Dadurch ist ein Impfzertifikat erst 14 Tage nach Erstellung gültig \
!!**Vorsicht, möglicher Bug bei anderen Zertifikatstypen**!!
```python
if cert.not_valid_before is not None and issued_at + timedelta(seconds=1209600) < cert.not_valid_before:
        cert_expired = True
```
Ende der Funktion, Zeile 1700 ff. \
Damit wird geprüft, dass die vorgesehene Anzahl Impfungen erfolgt ist
```python
    fully_vaccinated=True
    if 'v' in ehc and 'vaccination' in usage:
       sd=ehc['v'][0]['sd']
       dn=ehc['v'][0]["dn"]
       if sd != dn:
           fully_vaccinated=False
    print(f'Valid Key Usage: {usage_valid}')
    print(f'Signature Valid: {valid}')

    return valid and not cert_expired and not revoked and usage_valid and fully_vaccinated
```
Am Ende der Datei, LED-Steuerung, Z 2450 ff.
```python
        if certs is not None:
            ok=verify_ehc(ehc_msg, issued_at, certs, args.print_exts)
            led=LED(22)
            if ok:
                print("certificate valid, not expired")
                led.on()
                sleep(5)
                led.off()
            else:
                print("certificate not valid or expired or wrong key usage")
                for i in range(0,10):
                    led.on()
                    sleep(0.1)
                    led.off()
                    sleep(0.1)
```
## anderes
ausführbar machen, z.B.
```sh
cd path_to_folder/verify-ehc
chmod +x verify_ehc.py
```

Mit Internetverbindung, für Offline-Nutzung: Zertifikate speichern
```sh
cd path_to_folder/verify-ehc
./verify_ehc.py --certs-from AT,DE --save-certs trust_list.cbor
```

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
