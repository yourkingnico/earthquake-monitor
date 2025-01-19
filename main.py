import machine
import network
import urequests
import time

# Import Wi-Fi credentials from a separate file
try:
    from wifi_config import SSID, PASSWORD
except ImportError:
    print("Error: Missing wifi_config.py file with SSID and PASSWORD.")
    raise

# GPIO Pins for LEDs
BLUE = machine.Pin(2, machine.Pin.OUT)  # Built-in blue LED (active-low logic)
YELLOW = machine.Pin(5, machine.Pin.OUT)
RED = machine.Pin(4, machine.Pin.OUT)
GREEN = machine.Pin(0, machine.Pin.OUT)

# USGS API endpoint
SERVER_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
QUERY_PARAMS = "?latitude=34.020728&longitude=-118.692602&maxradiuskm=200&format=text&starttime=NOW-48hours"

# Initialize Wi-Fi connection
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    
    # Blink BLUE LED while connecting
    while not wlan.isconnected():
        BLUE.value(0)  # Turn ON (active-low)
        time.sleep(0.5)
        BLUE.value(1)  # Turn OFF
        time.sleep(0.5)
    
    print("Connected to Wi-Fi:", wlan.ifconfig())
    BLUE.value(1)  # Ensure BLUE LED is OFF after connection

# Handle LED indication
def indicate_led(pin, duration):
    pin.value(1)  # Turn ON (active-high)
    time.sleep(duration)
    pin.value(0)  # Turn OFF

# Main logic
def query_earthquake_data():
    try:
        url = SERVER_URL + QUERY_PARAMS + "&minmagnitude=3.5"
        print(f"Fetching data from: {url}")
        response = urequests.get(url)
        payload = response.text
        response.close()

        print("Response length:", len(payload))
        
        if len(payload) > 300:
            print("Blinking Red (High activity)")
            for _ in range(5):  # Blink 5 times
                indicate_led(RED, 1)
        elif len(payload) > 200:
            print("Turning Red (Moderate activity)")
            indicate_led(RED, 300)  # Stay on for 5 minutes
        else:
            url = SERVER_URL + QUERY_PARAMS + "&minmagnitude=2"
            print(f"Fetching lower magnitude data from: {url}")
            response = urequests.get(url)
            payload = response.text
            response.close()

            if len(payload) > 200:
                print("Turning Yellow (Mild activity)")
                indicate_led(YELLOW, 1200)  # Stay on for 20 minutes
            else:
                print("Turning Green (Low activity)")
                indicate_led(GREEN, 3600)  # Stay on for 1 hour

    except Exception as e:
        print("Error:", str(e))

# Program entry point
def main():
    connect_to_wifi()
    while True:
        query_earthquake_data()
        print("Waiting 1000 seconds before next check...")
        BLUE.value(1)  # Ensure BLUE LED is OFF during delay
        time.sleep(1000)

# Run the program
main()
