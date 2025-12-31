import sys
import subprocess
import audioop
import time
import signal
import random
from billy_bass import BillyBass

# --- CONFIG ---
# Audio Settings
THRESHOLD = 500   # Lowered to ensure sensitivity
MIN_OPEN_TIME = 0.15 # Minimum time (seconds) to keep mouth open
DEBUG = False     # Set True to see RMS values in logs

# Initialize Billy Bass
bass = BillyBass()

def cleanup(signum, frame):
    """Handle shutdown signals gracefully"""
    bass.move_body(out=False)
    bass.cleanup()
    sys.exit(0)

# Register cleanup on exit
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

def run():
    # Start the actual audio player (aplay)
    # We pipe our stdin (audio from HA) to aplay's stdin
    player = subprocess.Popen(
        ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw"], 
        stdin=subprocess.PIPE
    )

    bass.move_body(out=True)
    mouth_state = False
    next_toggle_time = 0
    
    try:
        while True:
            # Read audio chunk
            data = sys.stdin.buffer.read(2048)
            if not data:
                break 
            
            # 1. Play sound
            player.stdin.write(data)
            
            # 2. Check volume
            rms = audioop.rms(data, 2)
            if DEBUG:
                sys.stderr.write(f"RMS: {rms}\n")

            # 3. Animate Mouth (Anime Style Flapping)
            if rms > THRESHOLD:
                now = time.time()
                if now >= next_toggle_time:
                    # If coming from silence, force open, otherwise toggle
                    if next_toggle_time == 0:
                        mouth_state = True
                    else:
                        mouth_state = not mouth_state
                    
                    bass.set_mouth(mouth_state)
                    next_toggle_time = now + random.uniform(0.1, 0.3)
            else:
                if mouth_state:
                    bass.set_mouth(False)
                    mouth_state = False
                next_toggle_time = 0

    except Exception as e:
        pass
    finally:
        if player:
            player.stdin.close()
            player.wait()
        bass.move_body(out=False)
        bass.cleanup()

if __name__ == "__main__":
    run()
