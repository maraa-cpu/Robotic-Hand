import time
import settings
import network
from servomotor import ServoMotor
from wifi_manager import WIFIManager
from mqtt_manager import MQTTManager

PIN_POLLICE = 26  
PIN_INDICE  = 27  
PIN_MEDIO   = 14  
PIN_ANULARE = 12  
PIN_MIGNOLO = 13  

def main():
    print("Avvio Sistema")

    dita = [
        ServoMotor(PIN_POLLICE),
        ServoMotor(PIN_INDICE),
        ServoMotor(PIN_MEDIO),
        ServoMotor(PIN_ANULARE),
        ServoMotor(PIN_MIGNOLO)
    ]

    wifi = WIFIManager()
    wifi.connect()

    mqtt = MQTTManager()
    if mqtt.connect():
        print("Connesso al broker MQTT! In attesa di comandi.")
    else:
        print("Errore: impossibile connettersi a MQTT.")
        return

    for dito in dita:
        dito.set_angle(0)
        time.sleep_ms(15)

    ultimo_invio = time.ticks_ms()
    wlan = network.WLAN(network.STA_IF) 

    while True:
        mqtt.check_msg()
        cmd = mqtt.get_last_command()
        
        if cmd:
            try:
                valori = cmd.split(',')
                if len(valori) == 5:
                    angoli = [int(v) for v in valori]
                    for i in range(5):
                        dita[i].set_angle(angoli[i])
                        time.sleep_ms(15) 
            except ValueError:
                print("Dati non validi:", cmd)
        
        ora = time.ticks_ms()
        if time.ticks_diff(ora, ultimo_invio) > 2000:
            rssi = wlan.status('rssi')
            mqtt.publish(b"robot/mano/telemetria", str(rssi))
                
            ultimo_invio = ora
            
        time.sleep_ms(10)

if __name__ == "__main__":
    main()


