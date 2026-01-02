#!/usr/bin/env python3
import sys
import subprocess
import audioop
import time
import signal
import random
from typing import Tuple
from billy_bass import BillyBass

# --- CONFIG ---
# Audio Settings
THRESHOLD = 500   # Lowered to ensure sensitivity
MIN_OPEN_TIME = 0.15 # Minimum time (seconds) to keep mouth open
DEBUG = False     # Set True to see RMS values in logs

class BillySpeaker:
    def __init__(self):
        self.bass = BillyBass()
        self.player = None

    def update_mouth(self, mouth_state: bool, next_toggle_time: float) -> Tuple[bool, float]:
        """
        Checks if it's time to toggle the mouth and updates the state.

        Args:
            mouth_state: Current state of the mouth (True=Open, False=Closed).
            next_toggle_time: Timestamp when the next toggle should happen.

        Returns:
            A tuple containing the updated (mouth_state, next_toggle_time).
        """
        now = time.time()
        if now >= next_toggle_time:
            # If next_toggle_time is 0, we are starting a new sequence -> Force Open
            if next_toggle_time == 0:
                mouth_state = True
            else:
                mouth_state = not mouth_state
            
            self.bass.set_mouth(mouth_state)
            next_toggle_time = now + random.uniform(MIN_OPEN_TIME, 0.3)
            
        return mouth_state, next_toggle_time

    def flap_randomly(self, duration: float):
        """
        Simulates mouth movement for a specific duration.
        Used to cover the latency of the audio buffer draining.

        Args:
            duration: How long to flap in seconds.
        """
        start_time = time.time()
        mouth_state = False
        next_toggle = 0
        
        while (time.time() - start_time) < duration:
            mouth_state, next_toggle = self.update_mouth(mouth_state, next_toggle)
            time.sleep(0.01)
            
        self.bass.set_mouth(False)

    def run(self):
        """
        Main loop: Reads audio from stdin, plays it via aplay,
        and animates the mouth based on volume (RMS).
        """
        self.player = subprocess.Popen(
            ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw"], 
            stdin=subprocess.PIPE
        )

        self.bass.move_body(out=True)
        mouth_state = False
        next_toggle_time = 0
        
        try:
            while True:
                # Read audio chunk
                data = sys.stdin.buffer.read(2048)
                if not data:
                    break 
                
                # Play sound
                self.player.stdin.write(data)
                
                # Ensure data length is even for 16-bit audioop (2 bytes width)
                if len(data) % 2 != 0:
                    data = data[:-1]
                if not data: continue

                # Check volume
                rms = audioop.rms(data, 2)
                if DEBUG:
                    sys.stderr.write(f"RMS: {rms}\n")

                # Animate Mouth
                if rms > THRESHOLD:
                    mouth_state, next_toggle_time = self.update_mouth(mouth_state, next_toggle_time)
                else:
                    if mouth_state:
                        self.bass.set_mouth(False)
                        mouth_state = False
                    next_toggle_time = 0

        except Exception as e:
            sys.stderr.write(f"Error in speak loop: {e}\n")
        finally:
            # Fix: Keep flapping while the audio buffer drains
            self.flap_randomly(1.5)
            
            if self.player:
                self.player.stdin.close()
                self.player.wait()
            
            self.bass.move_body(out=False)
            self.bass.cleanup()

def signal_handler(signum, frame):
    """
    Handles termination signals to exit gracefully.
    
    :param signum: This is automatically passed by the signal module but not used.
    :param frame: This is automatically passed by the signal module but not used.
    """
    sys.exit(0)

def main():
    """
    Main entry point for the Billy Bass speaks
    """
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    speaker = BillySpeaker()
    speaker.run()

if __name__ == "__main__":
    main()
