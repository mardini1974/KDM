from ota import OTAUpdater
import network
import secrets
from time import sleep

def connect_wifi(ssid,password):
        """ Connect to Wi-Fi."""

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        
        
        



repo_name = "KDM"
branch = "main"
firmware_url = f"{secrets.rep_url}/{repo_name}/{branch}/"        
connect_wifi(secrets.WIFI_SSID,secrets.WIFI_PASSWORD)
filenames = ["test.py","test2.html"]
ota_updater = OTAUpdater(firmware_url, filenames )

# ota_updater.check_for_updates()
ota_updater.download_and_install_update_if_available()