#!/usr/bin/env python3
import sys
from billy_bass import BillyBass

def main():
    """
    Entry point for the wake script.
    This script initializes the Billy Bass and extends its body to indicate readiness.
    """
    bass = None
    try:
        bass = BillyBass()
        bass.move_body(out=True)
        # No clean up! We want it to stay out while waiting for audio.
    except Exception as e:
        sys.stderr.write(f"Error in wake: {e}\n")
        # Only cleanup if something went wrong to prevent undefined state
        if bass:
            bass.cleanup()

if __name__ == "__main__":
    main()
