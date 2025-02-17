# Help Received: Slides from Canvas, ChatGPT to understand how to calculate distance from time and speed

from machine import Pin, PWM
import time

# Define pins for the HC-SR04 sensor
trigger_pin = Pin(5, Pin.OUT)  # GPIO5 (D1)
echo_pin = Pin(4, Pin.IN)     # GPIO4 (D2)

# Define pins for the LEDs
red_led = Pin(12, Pin.OUT)     # GPIO12 (D6) for red LED
green_led = Pin(13, Pin.OUT)   # GPIO13 (D7) for green LED

# Set initial state of LEDs (green LED on, red LED off)
red_led.off()
green_led.on()

# Function to measure distance using HC-SR04
def measure_distance():
    # Send 10us pulse to trigger
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    
    # Measure the time it takes for the echo to return
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
    
    # Calculate distance (in cm)
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * 0.0343) / 2  # Speed of sound is 343m/s or 0.0343 cm/us
    return distance

# Main loop
while True:
    # Measure distance
    distance = measure_distance()
    
    # Check if distance is less than 10 cm
    if distance < 10:
        # Turn on red LED, turn off green LED
        red_led.on()
        green_led.off()
        print(distance, " - in range")
    else:
        # Turn on green LED, turn off red LED
        red_led.off()
        green_led.on()
        print(distance, " - not in range")
    
    # Wait for a short period before taking another measurement
    time.sleep(0.2)