# example script to show how uri routing and parameters work
#
# create a file called secrets.py alongside this one and add the
# following two lines to it:
#
#	WIFI_SSID = "<ssid>"
#	WIFI_PASSWORD = "<password>"
#
# with your wifi details instead of <ssid> and <password>.

from phew import server, connect_to_wifi
from phew.template import render_template
import json
import secrets
from lcdutil import LCDUTIL
from machine import Pin,Timer,I2C
from Addresses import Lcd1,Lcd2,Lcd3

def get_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()
    
def getData(file):
    '''
    Open json file and read it 
    '''
    with open(file,"r") as f:
        return json.loads(f.read())

    
def run():
#initilaize I2C protocol

#   i2c= I2C(0,sda=Pin(16), scl=Pin(17),freq=400000)
#   lcd = LCDUTIL(i2c)
#         # print(i2c.scan())
  ip = connect_to_wifi(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
  print(ip)
#   lcd.lcd_show(Lcd3,"IP Adres",0,0,32,text2= ip,x2=0,y2=33,size2=16)
  

  # Reboot raspberry Pi
  @server.route("/reboot", methods=["GET", "POST"])
  def reboot(request):
      #import sys
      #sys.exit()
      from machine import reset
      reset()
      return await render_template("login.html")

  @server.route("/save", methods=["POST"])
  def save_form(request):
       fields = ["enc3_col","enc2_col","enc1_col","enc3_fc","enc2_fc","enc1_fc","start_delay","max_trech"]
       data  = getData("settings.json")
       for field in fields:
           value = request.form.get(field,None)
           print ("{},{}".format (field,value))
            # update each value in the dictionary
           data.update({field:value})
        # save settings file
       with open("settings.json","w") as f:
           f.write(json.dumps(data))

       return await render_template("saved.html")

  # url parameter and template render
  @server.route("/loginuser", methods=["GET","POST"])
  def logged(request):
      
      user = request.form.get("user",None)
      password = request.form.get("password",None)
      if (user,password) in secrets.PASSWORDS.items():
          try:
            data  = getData("settings.json")
            print (data)
            #   https://icons.iconarchive.com/icons/icons8/windows-8/128/Industry-Electrical-Sensor-icon.png
            server.serve_file("diagram32.png") 
            return await render_template("kalmeijer.html",data = data)
          except:
              # No data could be written our faulty data
            return await render_template("404.html",message = "Data file is corrupted"), 404
      else:
          # No user was found pass word or user are fault
          return await render_template("404.html",message = "Unkown user"), 404

  # url parameter and template render
  @server.route("/", methods=["GET"])
  def login(request):
      return await render_template("login.html")
  
  
  
  # catchall example
  @server.catchall()
  def catchall(request):
    return render_template("404.html",message = "Unkown command"), 404
 # Return Favicon
  server.serve_file("favicon.ico")
 
  # start the webserver
  server.run()



