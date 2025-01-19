# Earthquake Monitor with ESP8266 🌍🔴
Displays color status on micro computer depending on live earthquake data for Los Angeles Region.
Similar to [nicktorres.net/earthquake](https://www.nicktorres.net/earthquake/), but simpler and for a micro computer. 

This project uses an ESP8266 microcontroller with **MicroPython** to monitor earthquake activity through the USGS Earthquake API. It uses LEDs to visually indicate the severity of earthquakes detected within a 200 km radius of a given location. 

---

## 📋 Features
- **Earthquake Detection**: Queries the USGS API for earthquake data.
- **Severity Indication**: Uses LEDs (Red, Yellow, Green, Blue) to represent different severity levels.
- **Wi-Fi Connectivity**: Easily connect to a Wi-Fi network.
- **Modular Design**: Cleanly separates sensitive credentials for security.

### Why is the logic so weird?
Fair question, hear me out. At first I wanted to query the earthquake data, parse through it, and determine a severity status based on number of events, magnitude, and current time. This strategy proved very difficuly considering this microcomputer doesn't even have a system clock, and to parse through all the data in this fashion we quickly run out of memory!

Do deal with these constraints, a more creative approach was needed. Given the limited libraries, limited storage, and lack of clock, earthquake severity is determined simply by making a conditional sequence of API requests with pre set query parameters like minimum magnitude, and start time. Because we simply don't have the memory to parse the responses, the script simply checks the response length to determine if we have events with the specified minimum magnitude and time frame. if the response is less than 200 characters, we know that there wasn't any matching earthquake data returned based on the average length of an empty response. If there is more than 200 characters, we can assume at least one matching data event was returned, thus allowing us to determine the earthquake severity without parsing through the response! 

The lack of a clock really made this difficult, considering we are relying on the API query parameters, and we need to supply the startTime parameter. It took me a while to hack around and figure out that I could pass NOW-48hours as a valid query Param, and that this NOW value would use the current UTC time on the API side. This is because the parameter supports relative time expressions! Considering the two options of when to generate the startTime parameter, this situation seems optimal for the use case. Because it's a real time system where we want to get the latest earthquake data available, it's preferred to generate the time on the server side, as opposed to a few milliseconds earlier on the micro computer about to make request. This ensures the most up to date date is returned.


## 🛠️ Dependencies

### Hardware
1. **ESP8266 Development Board** (e.g., NodeMCU or Wemos D1 Mini).
2. **LEDs**:
   - Red, Yellow, Green, and Blue LEDs.
   - 220-330 Ohm resistors for current limiting.
3. **USB Cable**: To connect ESP8266 to your computer.
4. **Breadboard** and jumper wires.

### Software
1. **Python 3.x**: Install from [python.org](https://www.python.org/).
2. **MicroPython Firmware**: Download from [MicroPython ESP8266 Firmware](https://micropython.org/download/esp8266/).
3. **esptool**: To flash MicroPython firmware.
   ```bash
   pip install esptool

   Visual Studio Code:
4. Download VS Code.
    Install the Pymakr extension for MicroPython file management.
5. Serial Terminal (optional): Tools like PuTTY or Arduino Serial Monitor to debug.

🚀 Setup Instructions
Step 1: Flash MicroPython on ESP8266
Erase Existing Firmware: $python -m esptool --port COM3 erase_flash

Flash MicroPython Firmware: Replace the <path_to_bin> with your .bin file path:
$python -m esptool --port COM3 write_flash -fm dio -fs 4MB 0x00000 <path_to_bin>


python -m esptool --port COM3 write_flash -fm dio -fs 4MB 0x00000 <path_to_bin>
Verify Installation:
Open a serial terminal (e.g., PuTTY) at 115200 baud.
Press Enter to see the MicroPython >>> prompt.

Step 2: Set Up Project Files
Clone or download this repository:

Open wifi_config.py and replace placeholders with your SSID and password:

SSID = "your_wifi_ssid"
PASSWORD = "your_wifi_password"

Step 3: Upload Files to ESP8266
Open Visual Studio Code.
Install the Pymakr extension.
Configure Pymakr:
Open the Command Palette (Ctrl+Shift+P) and select Pymakr > Global Settings.
Set the address to COM3 (or your ESP8266's port).
Upload files to ESP8266:
Click the "Sync" button in Pymakr or run Pymakr > Upload from the Command Palette.

Step 4: Run the Program
Open the Pymakr terminal or connect via a serial terminal (e.g., PuTTY).
Run the script.

💡 How It Works
The ESP8266 connects to the Wi-Fi network using credentials in wifi_config.py.
The earthquake.py script queries the USGS Earthquake API for recent earthquake data.
Based on the severity (magnitude) of earthquakes:
Red LED: Severe activity.
Yellow LED: Moderate activity.
Green LED: Low activity.
Blue LED: Debugging or connected status.
LEDs light up for varying durations depending on the detected activity.

🐍 Python Code Structure
main.py
Main script to query earthquake data, analyze severity, and control LEDs.

wifi_config.py
Stores Wi-Fi credentials securely. This file is ignored in .gitignore.




🔧 Troubleshooting
Cannot Connect to Wi-Fi: Check the SSID and PASSWORD in wifi_config.py.
No LEDs Lighting Up: Verify GPIO pin connections and LED resistors.
Serial Connection Issues: Ensure the correct COM port and baud rate (115200).

🛡️ Security Notes
Do Not Commit wifi_config.py: This file contains sensitive Wi-Fi credentials.
Use .gitignore to prevent accidental uploads.

