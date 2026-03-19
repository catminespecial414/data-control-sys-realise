# devices/__init__.py
import random

from devices import buzzer

buzzer_pin = 11

class DeviceManager:
    def initialize(pin):
        #初始化蜂鸣器
        buzzer.setup(pin=buzzer_pin)
    def bin(self):
        buzzer.beep(0.5)