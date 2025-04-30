import network
import socket
import machine
import time


tx_pin = machine.Pin(17)  # GPIO17 for TX
rx_pin = machine.Pin(16)


# Connect to WiFi
ssid = 'YOUR_SSID'
password = 'YOUR_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print('✅ Connected to WiFi:', wlan.ifconfig())

# UART connection to Pololu 3pi+2040
uart = machine.UART(2, baudrate=115200, tx=tx_pin, rx=rx_pin)

# Start TCP server
addr = socket.getaddrinfo('0.0.0.0', 1234)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('🌐 Waiting for WiFi connection…')

while True:
    cl, addr = s.accept()
    print('🔗 Client connected from', addr)
    cl_file = cl.makefile('rwb', 0)

    try:
        while True:
            line = cl_file.readline()
            if not line:
                break

            try:
                decoded = line.decode().strip()

                # Only forward real commands!
                if decoded:  # Ignore empty lines
                    uart.write(decoded + "\n")
                    print("📤 → Sent to Pololu:", decoded)
            except UnicodeError as e:
                # Error handling for invalid characters
                print("⚠️ Decoding error:", e)

            time.sleep(0.05)

    except Exception as e:
        print("❌ Connection error:", e)

    cl.close()
    print("🔌 Client disconnected")
