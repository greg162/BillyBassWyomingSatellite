#!/usr/bin/env python3
from billy_bass import BillyBass
import time

def run_diagnostic():
    """
    Runs a quick Power On Self Test (POST) to verify hardware.
    """
    bass = BillyBass()
    print("--- Billy Bass Diagnostic ---")

    try:
        # 1. Mouth Check
        print("[1/3] Testing Mouth...")
        for _ in range(3):
            bass.set_mouth(True)
            time.sleep(0.15)
            bass.set_mouth(False)
            time.sleep(0.15)

        # 2. Tail Check
        print("[2/3] Testing Tail...")
        bass.move_tail(True)
        time.sleep(0.5)
        bass.move_tail(False)
        time.sleep(0.5)

        # 3. Body Check
        print("[3/3] Testing Body...")
        bass.move_body(True)
        time.sleep(1.0)
        bass.move_body(False)
        
        print("--- Diagnostic Complete ---")

    except KeyboardInterrupt:
        print("\nDiagnostic interrupted.")
    finally:
        bass.cleanup()

if __name__ == "__main__":
    run_diagnostic()