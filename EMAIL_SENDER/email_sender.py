#!/usr/bin/env python

#import smtplib

#sender = 'from@fromdomain.com'
#receivers = ['to@todomain.com']

#message = """From: From Person <from@fromdomain.com>
#To: To Person <to@todomain.com>
#Subject: SMTP e-mail test

#This is a test e-mail message.
#"""

#try:
#   smtpObj = smtplib.SMTP('localhost')
#   smtpObj.sendmail(sender, receivers, message)         
#   print "Successfully sent email"
#except SMTPException:
#   print "Error: unable to send email"

import smtplib
import getpass

# proxy stuff (requires explicit apt-get install python-socksipy) :
import socks
 
user_in = raw_input("Username: ")
pass_in = getpass.getpass()

#################################

#server = smtplib.SMTP('131.185.80.12', 587)
#server.starttls()
#server.login(user_in, pass_in)

#################################

#server = smtplib.SMTP('131.185.68.61', 25)

#################################
 


msg = "test message"
server.sendmail("imran.ali@dsto.defence.gov.au", "imran.ali@dsto.defence.gov.au", msg)
server.quit()
