#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import time
import os
from gpiozero import LED
#this is a clean version, without uncommented code
#see barcodescanner_debug.py for debuggin ideas

###initial###
qrDecoder = cv2.QRCodeDetector()
#use VideoDevice 0
cap = cv2.VideoCapture(0)

# White LED on GPIO17, status running
led_running_qr_detected = LED(17) # on: detected

# yellow LED on GPIO27, blinking 5 times rapidly: decoding failed, output==[]
led_detection_success_fail = LED(27)

count=0

###Main###

# while True loop is a quick and very dirty solution to keep process running
while True:
    #control LED blinking
    if count<10:
         led_running_qr_detected.off()
    elif 10<=count<20:
         led_running_qr_detected.on()
    else:
         count=0
    count=count+1
    #slow down a tiny bit 
    time.sleep(0.05)
    #make sure LED is off
    led_detection_success_fail.off()
    #try to read image from VideoCapture (Camera)
    readsuccess, img = cap.read()
    detectionsuccess=False

    #Image was read, device exists
    if readsuccess:
        detectionsuccess,points = qrDecoder.detect(img)
    #status info if camera not connected
    else:
        #Blinking LEDs
        for i in range(0,10):
              led_detection_success_fail.on()
              led_running_qr_detected.off()
              time.sleep(0.2)
              led_detection_success_fail.off()
              led_running_qr_detected.on()
              time.sleep(0.2)
              
    if detectionsuccess:
        led_running_qr_detected.on()
        cv2.imwrite("qr_gelesen.jpeg", img)

        #run verify-ehc with saved image and offline trust_list.cbor
        commandstream=os.popen("cd /home/pi/verify-ehc/ && ./verify_ehc.py --image ../emb-impf/qr_gelesen.jpeg --certs-file trust_list.cbor")
        # read output from commandstream object
        output=commandstream.readlines() 

        #if nothing was read 
        if output==[]:
              #yellow  LED starts blinking
              for i in range(0,4):
                  led_detection_success_fail.on()
                  time.sleep(0.1)
                  led_detection_success_fail.off()
                  time.sleep(0.1)
        else:
            #wait a little more
              time.sleep(2)
        
        #close commandline object - manual garbage collect
        commandstream.close()
