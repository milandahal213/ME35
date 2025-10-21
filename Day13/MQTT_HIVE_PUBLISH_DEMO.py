import network
import time
from umqtt.simple import MQTTClient
import ssl
import secrets

# Wi-Fi credentials
SSID = secrets.SSID
PASSWORD = secrets.PWD

# MQTT settings
MQTT_BROKER = secrets.mqtt_url 
MQTT_PORT = 8883
MQTT_USERNAME = secrets.mqtt_username 
MQTT_PASSWORD = secrets.mqtt_password 
CLIENT_ID = "esp32_client"
TOPIC_PUB = "/test/me35"
TOPIC_SUB = "ME35/milan"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        
    if wlan.isconnected():
        print("WiFi Connected! IP:", wlan.ifconfig()[0])
        return True
    else:
        print("WiFi connection failed!")
        return False

def mqtt_connect():
    try:
        client = MQTTClient(
            client_id=CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USERNAME,
            password=MQTT_PASSWORD,
            ssl=True,  # Enable SSL
            ssl_params={'server_hostname': MQTT_BROKER}  # Important for certificate validation
        )
        client.connect()
        print("MQTT Connected successfully!")
        return client
    except OSError as e:
        print(f"MQTT Connection failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if connect_wifi():
    client = mqtt_connect()
    if client:
        try:
            client.publish(TOPIC_PUB, b'Hello from ESP32!')
            print("Message published successfully!")
        except Exception as e:
            print(f"Publish failed: {e}")