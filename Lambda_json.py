from machine import UART, Pin
import time
import ure

# Define the Bluetooth UART object
bt = UART(0, 9600)

# Define the GPIO pins for controlling the LEDs and fans
L1 = Pin(6, Pin.OUT)
L2 = Pin(7, Pin.OUT)
# F1 = Pin(4, Pin.OUT)
# F2 = Pin(5, Pin.OUT)

# Define a regular expression pattern for matching Alexa commands
alexa_pattern = ure.compile(r'(TurnOn|TurnOff)(Light|Fan)(Intent)')

while True:
    try:
        br = bt.readline()
        if br:
            # Decode the received data from bytes to string
            br = br.decode().strip()
            
            # Match the received data against the Alexa pattern
            match = alexa_pattern.match(br)
            if match:
                # Extract the matched groups (action and device)
                action = match.group(1)
                device = match.group(2)
                
                # Control the lights and fans based on the Alexa command
                if device == 'Light':
                    if action == 'TurnOn':
                        L1.value(1)
                    elif action == 'TurnOff':
                        L1.value(0)
                elif device == 'Fan':
                    if action == 'TurnOn':
                        L2.value(1)
                    elif action == 'TurnOff':
                        L2.value(0)
                # You can add similar logic for controlling other devices, like fans, based on the intents
                
            else:
                # Print an error message for invalid Alexa commands
                print('Invalid Alexa command:', br)
                
    except:
        time.sleep(1)
