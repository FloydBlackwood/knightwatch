# Author: Ian Marshall
# Date: August 5th 2018
import grovepi
# import libraries needed to create and send emails
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import smtplib
import time
import datetime
from credentials import * # import PASSWORD, EMAILFROM, and EMAILTO from credentials. This file is not included in final submission for data security purposes
from picamera import PiCamera
import os
cam = PiCamera()
cam.rotation = 180
pir_sensor = 8
grovepi.pinMode(pir_sensor,"INPUT")

def SendMail(ImgFileName):
	# create message object instance
	msg = MIMEMultipart()
	message = 'Motion has been detected.'
	# setup the parameters of the message
	password = PASSWORD
	msg['From'] = EMAILFROM
	msg['To'] = EMAILTO
	msg['Subject'] = "KnightWatch Home Security"
	# attach image to message body
	msg.attach(MIMEText(message, 'plain'))
	msg.attach(MIMEImage(file(ImgFileName).read()))
	# create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
	server.starttls()
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
	# send the message via the server.
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()
 
	print "successfully sent email to %s:" % (msg['To'])

while True:
	try:
		if grovepi.digitalRead(pir_sensor):
			os.chdir("/home/pi/Pictures") # assign captured images to folder on Raspberry Pi as backup
			filename = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S.jpg") # timestamp images
			print 'Motion Detected'
			cam.start_preview()
			cam.capture(filename)
			cam.stop_preview()
			SendMail(filename) # send captured image to user using sendmail function
			time.sleep(3)
		else:
			print '-'
		time.sleep(1)
	except IOError:
	print "Error"