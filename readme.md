# Billy Bass Wyoming Satellite

![HEY BILLY](/media/completed.png)


This project allows you to create a Smart Speaker using a Raspberry Pi, a knock off Billy Bass fish and home assitant. You can see a demo of it in action here: 

https://www.youtube.com/watch?v=FuD_6neGKRo

It has the following features:

  * The body extends when waiting for a command.
  * The mouth flaps when an audio response is returned.
  * If you connect up your Voice Assistant up to 

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

## Installation Instructions

**Setup the Raspberry Pi**

  * Plugin the USB Microphone and the speakers to your Raspberry Pi.
  * Go through the standard install process to add Raspberry OS to an SD card or SSD and add it to your Raspberry Pi.
    * Install Raspberry Pi OS Legacy Lite - If you use a more modern version you can have issues with Python compatibilty in Wyoming Satellite.
    * When setting it up - ensure that you enable SSH.
    * You'll also be asked about default the WiFi network to connect to. I **HIGHLY** recommend using ethernet as the RPI has limited power and the Mic plus WiFi can cause power issues.

**Install Wyoming Satellite**

  * Switch on your Raspberry PI and SSH into it.
  * Intall the required dependencies: 
```
sudo apt-get update
sudo apt-get install --no-install-recommends  \
  git \
  python3-venv
```
  * Clone the Wyoming Satellite repository:
```
git clone https://github.com/rhasspy/wyoming-satellite.git
```

  * Navigate into the Wyoming Satellite directory:

```
cd wyoming-satellite
```

  * Run the installation command:

```
cd wyoming-satellite/
python3 -m venv .venv
.venv/bin/pip3 install --upgrade pip
.venv/bin/pip3 install --upgrade wheel setuptools
.venv/bin/pip3 install \
  -f 'https://synesthesiam.github.io/prebuilt-apps/' \
  -e '.[webrtc]'
```

NOTE: This differs from the installation instructions on the Wyoming Satellite repository. This is because the `[all]` command attempts to install a library that isn't compatible with this version of Python, but also isn't required for our setup.

  * Run setup script below to confirm everything has installed:

```
script/run --help
```

**Determine your Audio input and output devices and test Wyoming Satellite**

  * For this step I recommend following the tutorial from the offical Wyoming Satellite: https://github.com/rhasspy/wyoming-satellite/blob/master/docs/tutorial_2mic.md
  * Follow the instructions above and then run your wyoming-satellite to confirm everything is working.

**Wiring Everything up**

Below is the wiring diagram to connect up all the components:

![Wiring Schematic to connect Billy Bass to your Raspberry Pi](/media/schematic.png)

When connecting the power supply to your L298 Sensor, I recommend setting the power to 6V  and only increasing if the Billy Bass seems sluggish. 

With a lot of the Billy Bass there isn't an easy way to tell which way around the motors should connect to the L298 module. I recommend connecting it up randomly, then if the fish doesn't do the expected when running the script below, you can swap the wires around.

**Setup the Billy Bass scripts**

SSH into your Billy Bass and ensure you're in the home directory

```
cd ~/
```

Clone this projects repository:

```
git clone https://github.com/greg162/BillyBassWyomingSatellite.git
```

Next, you'll want to test that the fish is wired up correctly, run the included test script:

```
python3 BillyBassWyomingSatellite/test.py
```

As the script runs it will output on the screen what the fish should be doing.


Navigate into the wyoming-satellite directory:

```
cd wyoming-satellite/
```

Run the command to start the wyoming Speaker and test everything works as expected:


**Running the Wyoming Speaker**

Run the Wyoming Speaker start up command, but include/amend the following options:

```
--snd-command 'python3 /home/<PIUSERNAME>/BillyBassWyomingSatellite/billybass.py talk' \
--detection-command 'python3 /home/<PIUSERNAME>/BillyBassWyomingSatellite/billybass.py wake'
```

When you ask a question, the fish head should extend out and as he responds his mouth should flap!

## Troubleshooting

**The fish doesn't do one of the actions at all:**

Check the connections and ensure everything is connected to the correct pins.

**I hear a noise, but the fish doesn't move**

If you hear a wearing sound, but there's no movement, try swapping the motor wires around in your L298 module.

**The fish extends his head when he should extend his body and extends his tail when he should extend his tail when he should extend his head.**

The motor wires are the wrong way around for the body, swap the connections in the L298 module and it should work.
