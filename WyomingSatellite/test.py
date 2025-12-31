from billy_bass import BillyBass
import time

# Initialize Billy Bass
bass = BillyBass()

try:
    print("Testing Mouth...")
    # Move Mouth Open
    bass.set_mouth(True)
    time.sleep(0.5)
    bass.set_mouth(False)
    time.sleep(0.5)

    # Extend the tail
    print("Extending Tail...")
    bass.move_tail(True)
    time.sleep(2)
    bass.stop_all()

    print("Resetting")
    time.sleep(2)

    # Extend the body
    print("Extending Body...")
    bass.move_body(True)
    time.sleep(2)
    bass.stop_all()

    print('Resetting')
    time.sleep(2)

    # Extend the body and open the mouth
    print("Extending Body and Opening Mouth...")

    bass.move_body(True)
    bass.set_mouth(True)

    time.sleep(0.1)
    bass.set_mouth(False)

    time.sleep(0.1)
    bass.set_mouth(True)

    time.sleep(0.1)
    bass.set_mouth(False)

    time.sleep(0.1)
    bass.set_mouth(True)

    time.sleep(0.1)
    bass.set_mouth(False)

    time.sleep(0.1)
    bass.set_mouth(True)

    time.sleep(0.1)
    bass.set_mouth(False)

    time.sleep(0.1)
    bass.set_mouth(True)

    bass.stop_all()

except KeyboardInterrupt:
    print("Stopping...")

finally:
    bass.cleanup()
    print("Cleaned up GPIO.")