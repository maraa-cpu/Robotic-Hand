from machine import Pin,PWM
import time

class ServoMotor:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin, Pin.OUT))
        self.pwm.freq(50)
        self.pwm.duty(0)

    def set_angle(self, angle):
        duty_min = 26
        duty_max = 128
        angle = max(0, min(180, angle))
        duty = int(duty_min + (angle / 180) * (duty_max - duty_min))
        self.pwm.duty(duty)
