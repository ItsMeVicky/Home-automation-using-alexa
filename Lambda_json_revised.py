import json
import ure
from machine import UART, Pin
import time

# Define the Bluetooth UART object
bt = UART(0, 9600)

# Define the GPIO pins for controlling the LEDs and fans
L1 = Pin(6, Pin.OUT)
L2 = Pin(7, Pin.OUT)

# Define a regular expression pattern for matching Alexa commands
alexa_pattern = ure.compile(r'(TurnOn|TurnOff)(Light|Fan)(Intent)')

def lambda_handler(event, context):
    try:
        # Extract the voice command from the event object
        voice_command = event['request']['intent']['slots']['voiceCommand']['value']
        
        # Send the voice command to the Bluetooth module
        bt.write(voice_command.encode()) # Encode the voice command as bytes and send to the Bluetooth module
        
        # Wait for response from the Bluetooth module
        time.sleep(1)
        
        # Read the response from the Bluetooth module
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
                
                # Prepare the response for Alexa
                response = {
                    'version': '1.0',
                    'response': {
                        'outputSpeech': {
                            'type': 'PlainText',
                            'text': 'Command sent to home automation devices.' # Customize the response text as needed
                        },
                        'shouldEndSession': True
                    }
                }
                
            else:
                # Prepare the response for Alexa with an error message for invalid commands
                response = {
                    'version': '1.0',
                    'response': {
                        'outputSpeech': {
                            'type': 'PlainText',
                            'text': 'Invalid Alexa command.' # Customize the error response text as needed
                        },
                        'shouldEndSession': True
                    }
                }
                
        else:
            # Prepare the response for Alexa with an error message for no response from Bluetooth module
            response = {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'No response from home automation devices.' # Customize the error response text as needed
                    },
                    'shouldEndSession': True
                }
            }
        
    except Exception as e:
        # Prepare the response for Alexa with an error message for any exception occurred
        response = {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Error: {}'.format(str(e)) # Customize the error response text as needed
                },
                'shouldEndSession': True
            }
        }
    
    return response
