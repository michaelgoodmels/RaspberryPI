import network
import usocket as socket
from machine import Pin

# WLAN-Daten
WLAN_SSID = "maui"
WLAN_PASSWORD = "Swordfi$h"

# GPIO-Pins definieren
led_pins = {
    10: Pin(10, Pin.OUT),
    11: Pin(11, Pin.OUT),
    12: Pin(12, Pin.OUT),
    13: Pin(13, Pin.OUT),
    14: Pin(14, Pin.OUT),
    15: Pin(15, Pin.OUT)
}

# WLAN einrichten
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WLAN_SSID, WLAN_PASSWORD)

# Warten, bis verbunden
while not wlan.isconnected():
    pass

# IP-Adresse anzeigen
print("Verbunden - IP-Adresse:", wlan.ifconfig()[0])


def generate_html():
    buttons_html = ""
    for gpio_number, pin in led_pins.items():
        button_color = "#40E0D0" if pin.value() else "#1B4F72"
        buttons_html += f"""
            <button style='background-color: {button_color}; 
                           color: white; padding: 20px 40px; margin: 10px 0; 
                           font-size: 20px; font-family: Comic Sans MS, cursive; 
                           border: 3px solid white; 
                           border-radius: 15px; 
                           box-shadow: 3px 3px 0 white; 
                           outline: none; transition: transform 0.1s; width: 80%;'
                    onclick="location.href='/gpio/{gpio_number}'">
                GPIO {gpio_number}
            </button>
        """
    return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Pico Steuerseite</title>
                <style>
                    body {{
                        background-color: #ADD8E6; /* hellblau */
                        font-family: Comic Sans MS, cursive;
                        text-align: center;
                    }}
                    button:hover {{
                        transform: translate(-3px, -3px);
                        box-shadow: 6px 6px 0 white;
                    }}
                    #header {{
                        background-color: #333;
                        color: white;
                        padding: 10px;
                    }}
                    #footer {{
                        background-color: #333;
                        color: white;
                        padding: 5px;
                        position: fixed;
                        width: 100%;
                        bottom: 0;
                    }}
                    img {{
                        height: 50px;
                        vertical-align: middle;
                    }}
                </style>
            </head>
            <body>
                <div id="header">
                    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/cb/Raspberry_Pi_Logo.svg/1200px-Raspberry_Pi_Logo.svg.png" 
                         alt="Raspberry Pi Logo">
                    <h1>GPIO Steuerung fuer Raspberry Pi Pico</h1>
                </div>
                <p>Druecke einen Button, um den entsprechenden GPIO zu schalten.</p>
                {buttons_html}
                <div id="footer">
                    &copy; 2025 Michael Good
                </div>
            </body>
        </html>
    """


def send_response(conn, content):
    response = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + content
    conn.send(response)
    conn.close()


def handle_connection(conn):
    request = conn.recv(1024).decode()
    print("Request:", request)

    path = request.split(" ")[1]

    if path.startswith("/gpio/"):
        try:
            gpio_number = int(path.split("/")[2])
            if gpio_number in led_pins:
                led_pins[gpio_number].value(not led_pins[gpio_number].value())
                print(f"GPIO {gpio_number} geschaltet.")
                send_response(conn, generate_html())
                return
        except (IndexError, ValueError):
            pass

    send_response(conn, generate_html())


server = socket.socket(socket.SOCK_STREAM)
server.bind(('', 80))
server.listen(5)
print("Server gestartet")

while True:
    conn, addr = server.accept()
    print("Verbunden mit", addr)
    handle_connection(conn)
