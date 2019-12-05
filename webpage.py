from flask import Flask, render_template
import datetime
import watering

app = Flask(__name__)

# Template for the website
def template(message = ""):
  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d %H:%M")
  templateData = {
    'title' : 'Automated Watering',
    'time' : timestring,
    'message' : message
  }
  return templateData

# Website on startup
@app.route("/")
def hello():
  templateData = template()
  return render_template('index.html', **templateData)

# Website that has loaded the water log (on button press)
@app.route("/water_log")
def checkLog():
  templateData = template(message = watering.getWaterLog())
  return render_template('index.html', **templateData)

# Website that has loaded the reservoir status (on button press)
@app.route("/reservoir")
def checkSupply():
  templateData = template(message = watering.getRefillStatus())
  return render_template('index.html', **templateData)
  
# Run the server  
if __name__ == "__main__":
  app.run(host='127.0.1.1', port=80, debug=True)
