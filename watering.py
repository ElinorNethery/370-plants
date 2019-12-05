from gpiozero import LightSensor, Button, LED
from time import sleep
import datetime
import smtplib

# Initialize sensors
waterLevelSensor = Button(20)
moistureSensor = LightSensor(21)
waterPump = LED(26, False)

# Email variables
SMTP_SERVER = 'smtp.gmail.com' # the email server
SMTP_PORT = 587 # server port
GMAIL_USERNAME = 'apieohboy@gmail.com'
GMAIL_PASSWORD = 'raspberrypI4'

class Emailer:
  def sendmail(self, recipient, subject, content):
    # CREDIT TO BC ROBOTICS FOR THIS EMAIL CODE (only this email code though)
    # Headers
    headers= ["From: " + GMAIL_USERNAME, "subject: " + subject, "To: " + recipient, "MIME-VERSION: 1.0", "Content Type: text/html"]
    headers = "\r\n".join(headers)
    
    # Connecting to Gmail server
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    
    # Login to Gmail
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    
    # Send email and exit
    session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
    session.quit
    
# Set up email variables
sent = Emailer()
notifEmail = 'eknether@rams.colostate.edu'

# How long the pump will run
waterTime = 10
# How long the device is foced to wait after it waters the plant
sleepAfterWater = 15

def sendMessage():
  waterPump.off()
  subject = "Water Supply"
  content = "Refill water supply please!"
  f = open("resevoir.txt", "w")
  f.write("Refill water supply please!")
  f.close()
  sent.sendmail(notifEmail, subject, content)
 
# Setting the function that runs when the water level sensor is triggered
waterLevelSensor.when_pressed = sendMessage

# Will start the sensors when the sensor detects something dry, stops when it is wet or when the switch is triggered
def startSensors():
  while True:
    moistureSensor.wait_for_light()
    if not waterLevelSensor.is_pressed:
      f = open("resevoir.txt", "w")
      f.write("Water supply is full")
      f.close()
      waterPlant()
    else:
      waterLevelSensor.wait_for_release()
      moistureSensor.wait_for_light()
    sleep(sleepAfterWater)
  waterPump.off()

# Function that turns on the pump and updates the log
def waterPlant():
  f = open("water_log.txt", "w")
  f.write("Last watered at {}".format(datetime.datetime.now()))
  f.close()
  waterPump.on()
  subject = "Watered!"
  content = "Your plant was just watered!"
  sent.sendmail(notifEmail, subject, content)

# Function that is used by the webpage to grab the water_log content
def getWaterLog():
  try:
    f = open("water_log.txt", "r")
    return f.readline()
  except:
    return "Hasn't been watered yet!"

# Function that is used by the webpage to grab the resevoir.txt content
def getRefillStatus():
  try:
    f = open("resevoir.txt", "r")
    return f.readline()
  except:
    return "Doesn't need to be refilled!"

startSensors()
    
