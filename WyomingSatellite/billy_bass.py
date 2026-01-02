import RPi.GPIO as GPIO

class BillyBass:
    # Pin Definitions (BCM) - Based on test.py
    MOUTH_IN1 = 23
    MOUTH_IN2 = 24
    BODY_IN3 = 17
    BODY_IN4 = 27
    pins = [MOUTH_IN1, MOUTH_IN2, BODY_IN3, BODY_IN4]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup Pins
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def set_mouth(self, is_open: bool):
        """
        Opens or closes the mouth.

        Args:
            is_open: True to open the mouth, False to close it.
        """
        if is_open:
            GPIO.output(self.MOUTH_IN1, GPIO.HIGH)
            GPIO.output(self.MOUTH_IN2, GPIO.LOW)
        else:
            GPIO.output(self.MOUTH_IN1, GPIO.LOW)
            GPIO.output(self.MOUTH_IN2, GPIO.LOW)

    def move_body(self, out: bool = True):
        """
        Moves the body in or out.

        Args:
            out: True to pop head out (extend), False to relax.
        """
        if out:
            # Head Out: 17 LOW, 27 HIGH (Matches test.py 'Extend Body')
            GPIO.output(self.BODY_IN3, GPIO.LOW)
            GPIO.output(self.BODY_IN4, GPIO.HIGH)
        else:
            # Relax: All LOW
            GPIO.output(self.BODY_IN3, GPIO.LOW)
            GPIO.output(self.BODY_IN4, GPIO.LOW)

    def move_tail(self, out: bool = True):
        """
        Moves the tail.

        Args:
            out: True to extend tail, False to relax.
        """
        if out:
            # Tail Out: 23 HIGH, 24 LOW
            GPIO.output(self.BODY_IN3, GPIO.HIGH)
            GPIO.output(self.BODY_IN4, GPIO.LOW)
        else:
            # Relax: All LOW
            GPIO.output(self.BODY_IN3, GPIO.LOW)
            GPIO.output(self.BODY_IN4, GPIO.LOW)

    def stop_all(self):
        """Sets all control pins to LOW."""
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)


    def cleanup(self):
        """Cleans up GPIO settings."""
        self.stop_all()
        GPIO.cleanup()