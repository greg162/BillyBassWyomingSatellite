from billy_bass import BillyBass

if __name__ == "__main__":
    bass = BillyBass()
    bass.move_body(out=True)
    # No cleanup()! We want it to stay out while waiting for audio.
