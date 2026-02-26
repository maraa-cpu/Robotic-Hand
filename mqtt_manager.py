import time
from umqttsimple import MQTTClient
import config

class MQTTManager:
    def __init__(self):
        self.client = MQTTClient(
            client_id=config.MQTT_CLIENT_ID,
            server=config.MQTT_BROKER,
            port=config.MQTT_PORT,
            user=config.MQTT_USER,
            password=config.MQTT_PASSWORD,
            keepalive=60
        )
        self.last_command = None

    def _on_message(self, topic, msg):
        try:
            messaggio = msg.decode('utf-8')
            print(f"-> Ordine ricevuto: {messaggio}")
            self.last_command = messaggio
        except:
            pass

    def connect(self):
        try:
            self.client.set_callback(self._on_message)
            self.client.connect()
            self.client.subscribe(config.MQTT_TOPIC_SUB)
            return True
        except Exception as e:
            print("Errore interno MQTT:", e)
            return False

    def check_msg(self):
        try:
            self.client.check_msg()
        except Exception as e:
            pass

    def get_last_command(self):
        cmd = self.last_command
        self.last_command = None
        return cmd

    def publish(self, topic, msg):
        try:
            self.client.publish(topic, msg)
        except Exception as e:
            print("Impossibile pubblicare:", e)
