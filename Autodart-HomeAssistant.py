import requests
import time
import paho.mqtt.client as mqtt
import sys
import signal

# MQTT-Konfiguration (bitte anpassen)
MQTT_BROKER = ""# HA IP-Adresse
MQTT_PORT = 1883
MQTT_TOPIC = ""
MQTT_USERNAME = ""
MQTT_PASSWORD = ""

API_URL = "http://IP-ADRESSEvonAUTODART-SERVER:3180/api/state"

# Flag für die Schleifensteuerung
running = True

def signal_handler(sig, frame):
    global running
    print("Beenden wird eingeleitet...")
    running = False

# Signalhandler für sauberen Shutdown einrichten
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_api_state():
    try:
        response = requests.get(API_URL, timeout=5)  # Timeout für Anfragen
        response.raise_for_status()  # Löst eine Exception bei HTTP-Fehlern aus
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der API-Daten: {e}")
        return None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbunden mit dem MQTT-Broker")
    else:
        print(f"Fehler beim Verbinden: {rc}")

def on_publish(client, userdata, mid):
    print("Nachricht veröffentlicht")

if __name__ == "__main__":
    # MQTT-Client einrichten
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Fehler beim Verbinden mit dem MQTT-Broker: {e}")
        sys.exit(1)

    client.loop_start()

    try:
        while running:
            state = get_api_state()
            if state is not None:
                print(state)  # Ausgabe der Daten in der Konsole
                client.publish(MQTT_TOPIC, str(state))
            time.sleep(1)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        print("MQTT-Client wird gestoppt...")
        client.loop_stop()
        client.disconnect()
        print("Programm beendet.")
