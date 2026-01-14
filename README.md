# Autodart Home Assistant MQTT Bridge

Ein Python-Script, das den Status einer Autodart-API abfragt und über MQTT an Home Assistant weiterleitet.

## Beschreibung

Dieses Script fungiert als Bridge zwischen einer Autodart-API und Home Assistant. Es fragt kontinuierlich den Status der Autodart-API ab und veröffentlicht die Daten über MQTT, sodass sie in Home Assistant verwendet werden können.

## Features

-  Kontinuierliches Polling der Autodart-API (jede Sekunde)
-  MQTT-Integration für Home Assistant
-  Graceful Shutdown bei SIGINT/SIGTERM

## Voraussetzungen

- Python 3.7 oder höher
- Zugriff auf eine Autodart-API
- MQTT-Broker (z.B. Mosquitto)
- Home Assistant (optional)

## Installation

1. Repository klonen:
```bash
git https://github.com/1337Rafael1337/autodart-homeassistant.git
cd autodart-homeassistant
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Konfiguration

Öffne `Autodart-HomeAssistant.py` und passe die folgenden Variablen an:

```python
# MQTT-Konfiguration
MQTT_BROKER = "192.168.1.253"           # IP-Adresse deines MQTT-Brokers
MQTT_PORT = 1883                        # MQTT-Port (Standard: 1883)
MQTT_TOPIC = "Beispiel:homeassistant/dart/licht" # MQTT-Topic
MQTT_USERNAME = "dein_username"         # MQTT-Benutzername
MQTT_PASSWORD = "dein_passwort"         # MQTT-Passwort

# API-Konfiguration
API_URL = "http://IP-ADRESSEvonAUTODART-SERVER:3180/api/state"# URL deiner Autodart-API
```

## Verwendung

### Linux / macOS
Script starten:
```bash
python3 Autodart-HomeAssistant.py
```

### Windows
Script starten über PowerShell oder CMD:
```cmd
python Autodart-HomeAssistant.py
```

Das Script läuft kontinuierlich und:
1. Fragt jede Sekunde die Autodart-API ab
2. Veröffentlicht die erhaltenen Daten auf dem konfigurierten MQTT-Topic
3. Gibt Status-Informationen in der Konsole aus

Zum Beenden: `Ctrl+C` drücken

**Hinweis**: Das Script kann auch mit PyInstaller zu einer ausführbaren EXE-Datei kompiliert werden.

## Home Assistant Integration

Nach dem Start des Scripts sind die Daten über MQTT in Home Assistant verfügbar:

Du kannst einen MQTT-Sensor in Home Assistant erstellen:

```yaml
mqtt:
  sensor:
    - name: "Autodart Status"
      state_topic: "Beispiel:homeassistant/dart/licht"
      value_template: "{{ value_json }}"
```

## Autostart (Optional)

### Als systemd Service (Linux)

1. Service-Datei erstellen:
```bash
sudo nano /etc/systemd/system/autodart-ha.service
```

2. Folgenden Inhalt einfügen:
```ini
[Unit]
Description=Autodart Home Assistant MQTT Bridge
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/pfad/zum/script
ExecStart=/usr/bin/python3 /pfad/zum/script/Autodart-HomeAssistant.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Service aktivieren und starten:
```bash
sudo systemctl enable autodart-ha.service
sudo systemctl start autodart-ha.service
```

### Windows Autostart

Für Autostart unter Windows gibt es mehrere Möglichkeiten:
- Über die **Aufgabenplanung** (Task Scheduler) beim Systemstart
- Script in den **Autostart-Ordner** legen (Shell:Startup)
- Mit **PyInstaller** zu einer EXE kompilieren und dann in Autostart einbinden

## Fehlerbehandlung

Das Script beinhaltet Fehlerbehandlung für:
- API-Verbindungsfehler (Timeout: 5 Sekunden)
- MQTT-Verbindungsprobleme
- Unerwartete Fehler während der Laufzeit

Bei Fehlern werden entsprechende Meldungen in der Konsole ausgegeben.

## Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei für Details

## Support

Bei Fragen oder Problemen erstelle bitte ein Issue im GitHub Repository.
