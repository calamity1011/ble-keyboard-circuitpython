import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService

# Initialize USB keyboard
kbd = Keyboard(usb_hid.devices)

# Initialize BLE radio and HID service
ble = BLERadio()
hid = HIDService()
advertisement = ProvideServicesAdvertisement(hid)
advertisement.complete_name = "Keyboard"  # Set the BLE connection name

# Initialize NeoPixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    # Start advertising when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    pixel.fill((0, 255, 0))  # Turn on NeoPixel with green color when connected
    while ble.connected:
        # Check for USB key press
        if kbd.key_count > 0:
            keys = kbd.keys
            # Send keys over BLE HID
            hid.keyboard_report = keys
            time.sleep(0.1)

    pixel.fill((0, 0, 0))  # Turn off NeoPixel when disconnected
