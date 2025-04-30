import machine
import time

uart = machine.UART(0, baudrate=115200, tx=machine.Pin(28), rx=machine.Pin(29))
buffer = b''  # Buffer to store incoming data

while True:
    if uart.any():
        data = uart.read(uart.any())  # Read all available bytes
        if data:
            buffer += data  # Append to buffer
            # Check if we have a complete command (ends with \n)
            if b'\n' in buffer:
                # Split buffer at newline
                command, buffer = buffer.split(b'\n', 1)
                print("Kommando empfangen:", command)
                if command == b'LED_ON':
                    machine.Pin(25, machine.Pin.OUT).value(1)
                elif command == b'LED_OFF':
                    machine.Pin(25, machine.Pin.OUT).value(0)
    time.sleep(0.01)  # Small delay to prevent tight looping
