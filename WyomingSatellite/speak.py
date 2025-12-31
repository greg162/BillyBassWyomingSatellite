import sys
import subprocess
import audioop
import time
import signal
from billy_bass import BillyBass

# --- CONFIG ---
# Audio Settings
THRESHOLD = 1500  # Adjust this if mouth opens too much/little

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
            bass.set_mouth(rms > THRESHOLD)

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
