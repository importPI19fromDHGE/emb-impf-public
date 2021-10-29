#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import time
import os
from gpiozero import LED
tstart=time.time()
qrDecoder = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)

#on: program is running
#off: qr_detected
led_running_qr_detected = LED(17) # White, status

#blinking 5 times rapidly: fail, output==[]
led_detection_success_fail = LED(27) #yellow
print("init")
count=0
while True:
    if count<10:
         led_running_qr_detected.off()
    elif 10<=count<20:
         led_running_qr_detected.on()
    else:
         count=0
    count=count+1
    time.sleep(0.05)
    led_detection_success_fail.off()
    readsuccess, img = cap.read()
#    print("read image")
    detectionsuccess=False
    #tbeforedetect=time.time()

    if readsuccess:
        detectionsuccess,points = qrDecoder.detect(img)
        tafterdetect=time.time()
    else:
        print("read failed")
        for i in range(0,10):
              led_detection_success_fail.on()
              led_running_qr_detected.off()
              time.sleep(0.2)
              led_detection_success_fail.off()
              led_running_qr_detected.on()
              time.sleep(0.2)
    if detectionsuccess:
        led_running_qr_detected.on()
        print("detected")
        print("time since start: \n",tafterdetect-tstart)
        cv2.imwrite("qr_gelesen.jpeg", img)
        tafterwrite=time.time()
       #print("start:",tbeforedetect-tstart,"detect:",tafterdetect-tbeforedetect,"write",tafterwrite-tafterdetect)
       #time.sleep(1)
       # manually run first: run ./verify_ehc.py --certs-from AT,DE --save-certs trust_list.cbor
       # check if trust_list.cbor exists TODO
        commandstream=os.popen("cd /home/pi/verify-ehc/ && ./verify_ehc.py --image ../emb-impf/qr_gelesen.jpeg --certs-file trust_list.cbor")
        output=commandstream.readlines() # readlines has \n or something
        if output==[]: #yellow  LED starts blinking
              for i in range(0,4):
                  led_detection_success_fail.on()
                  time.sleep(0.1)
                  led_detection_success_fail.off()
                  time.sleep(0.1)
              print("Error in barcodescanner.py: could not process qr code, try again!")
             # cv2.imwrite("latest_qr_process_error_"+str(tafterdetect-tstart)+".jpeg",img)
              cv2.imwrite("latest_qr_process_error.jpeg",img)
        else:
             #led_detection_success_fail.on()
              time.sleep(2)
             # print("output",output)
        print("completed")
      # print(commandstream.readlines())
        commandstream.close()
       # TODO clean up this output
#      time.sleep(3)
    #else:
        #print("QR Code not detected")
        #time.sleep(0.01)
        #For debugging
        #cv2.imwrite("qr_notfound.jpeg",img)
#    cap.release()

