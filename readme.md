# Billy Bass Wyoming Satellite

![HEY BILLY](/media/completed.jpg)


This project allows you to create a Smart Speaker using a Raspberry Pi, a knock off Billy Bass fish and home assitant. You can see a demo of it in action here: 

https://www.youtube.com/watch?v=FuD_6neGKRo

It has the following features:

  * The body extends to "listen" when the wake word is detected.
  * The mouth flaps in sync with the audio response.
  * Includes a custom wake word model ("Hey Billy") for Wyoming Wake Word.

## Requirements

**Hardware**

  * A knock off Billy Bass from AliExpress - I've included a screenshot of the one I purchased above.
  * Rasperry Pi  - Any version should work fine, this was tested on an RPI 2
  * L298N  - This is used to control the motors in the Billy Bass
  * A USB microphone - I used a $5 one I found at Canada Computers.
  * Speakers - I used some $10 speakers I found at Canada Computers that are USB powered.
  * A power supply that supports multiple voltages.
  * Some wires and basic soldering skills

**Software**

  * Rasperry Pi Imager
  * Home Assistant (with Wyoming Protocol support) -

## Installation Instructions

**Setup the Raspberry Pi**

  * Plugin the USB Microphone and speakers.
  * Flash the SD card using Raspberry Pi Imager:
      * **OS:** Select Raspberry Pi OS Legacy Lite (Bullseye). Note: Newer versions (Bookworm/Python 3.13) may have compatibility issues with Wyoming Satellite on older hardware.
      * **Settings:** Enable SSH and set a username/password.
      * **Network:** I **HIGHLY** recommend using Ethernet. The RPi 2 has limited power; running a USB WiFi dongle + Mic + Audio can cause brownouts.

**Install Wyoming Satellite**

Intall the required dependencies: 

```
sudo apt-get update
sudo apt-get install --no-install-recommends  \
  git \
  python3-venv
```

Clone the Wyoming Satellite repository:

```
git clone https://github.com/rhasspy/wyoming-satellite.git
```

Navigate into the Wyoming Satellite directory:

```
cd wyoming-satellite
```

Run the installation command:

```
cd wyoming-satellite/
python3 -m venv .venv
.venv/bin/pip3 install --upgrade pip
.venv/bin/pip3 install --upgrade wheel setuptools
.venv/bin/pip3 install \
  -f 'https://synesthesiam.github.io/prebuilt-apps/' \
  -e '.[webrtc]'
```

_Note: We use [webrtc] instead of [all] to avoid installing heavy AI libraries incompatible with the RPi 2._

Run setup script below to confirm everything has installed:

```
script/run --help
```

**Audio Setup**

Determine your Audio input and output devices and test Wyoming Satellite - I recommend following the tutorial from the offical Wyoming Satellite instructions: https://github.com/rhasspy/wyoming-satellite/blob/master/docs/tutorial_2mic.md


**Wiring**

Below is the wiring diagram to connect up all the components:

![Wiring Schematic to connect Billy Bass to your Raspberry Pi](/media/schematic.png)

  * Connect the Raspberry Pi to the L298N and the Fish Motors according to this diagram:
    * Voltage: Set your power supply to 6V. Increase slightly if the fish is sluggish, but do not exceed the motor ratings.
    * Polarity: Fish motors often lack clear markings. Connect them randomly first; if the fish moves backward (e.g., mouth closes instead of opening), swap the wires at the L298N terminal.

**Install the Billy Bass scripts**

```
cd ~/
git clone https://github.com/greg162/BillyBassWyomingSatellite.git
```

**Test the Hardware** - Run the included test script to verify wiring:

```
python3 BillyBassWyomingSatellite/wyomingSatellite/test.py
```

As the script runs it will output on the screen what the fish should be doing.

_The script will print actions to the screen. Watch the fish to ensure the movements match the text._

**Running the Satellite**

Navigate to the satellite directory:
```
cd ~/wyoming-satellite/
```
Run the startup command, pointing to the custom scripts for movement. Replace `<PIUSERNAME>` with your actual username (e.g., pi):

```
script/run \
  --name 'BillyBass' \
  --uri 'tcp://0.0.0.0:10700' \
  --mic-command 'arecord -r 16000 -c 1 -f S16_LE -t raw' \
  --snd-command 'python3 /home/<PIUSERNAME>/BillyBassWyomingSatellite/wyomingSatellite/billybass.py talk' \
  --detection-command 'python3 /home/<PIUSERNAME>/BillyBassWyomingSatellite/wyomingSatellite/billybass.py wake'
```

When you ask a question, the fish head should extend out and as he responds his mouth should flap!

## Troubleshooting

**The fish doesn't do one of the actions at all:**
Check your GPIO connections. Ensure the pins defined in billybass.py match your physical wiring.

**I hear a whirring noise, but the fish doesn't move:**
The motor is spinning the wrong way against the mechanism. Swap the two wires for that specific motor at the L298N module.

**The fish extends his head when he should extend his tail:**
The wires for the body motor are swapped. Reverse the connections for the Body Motor on the L298N module.

**The RPi crashes/reboots when the fish moves:**
This is likely a power brownout.

  * Ensure you are using Ethernet, not WiFi.
  * Edit /boot/config.txt and add max_usb_current=1 to ensure USB peripherals get enough power.
  * Ensure the L298N is powered by an external supply, not the Raspberry Pi 5V pin.