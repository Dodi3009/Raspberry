import cv2
import requests
import serial
import time
import signal

running = True

# Gestione del segnale di interruzione
def signal_handler(sig, frame):
    global running
    print("Interruzione ricevuta. Chiusura in corso...")
    running = False

# Configura la porta seriale
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

def send_string(string):
    if ser.is_open:
        ser.write((string + '\n').encode())
    else:
        print("Porta seriale chiusa.")

# URL del server
url = 'http://213.233.44.94:5000/upload_image'

# Registra il gestore del segnale
signal.signal(signal.SIGINT, signal_handler)

# Inizializza la webcam
cap = cv2.VideoCapture(0)

send_string("inizio")

while running:
    ret, frame = cap.read()
    if not ret:
        print("Errore nell'acquisizione del frame.")
        break

    # Timestamp inizio acquisizione
    start_time = time.time()

    # Codifica il frame come immagine JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    files = {'frame': buffer.tobytes()}

    try:
        # Invia il frame al server
        response = requests.post(url, files=files)
        response_time = time.time()  # Timestamp dopo la risposta del server
        data = response.json()

        if "eyes" in data:
            eye_positions = data["eyes"]
            for (center_x, center_y) in eye_positions:
                send_time = time.time()  # Timestamp prima di inviare alla COM3
                print(f"Occhio rilevato a: ({center_x}, {center_y})")
                send_string(f"{center_x} {center_y}")

                # Calcola la latenza
                total_latency = send_time - start_time
                server_latency = response_time - start_time
                print(f"Latenza totale: {total_latency:.3f} s")
                print(f"Latenza server: {server_latency:.3f} s")
        else:
            print(data.get("error", "Errore sconosciuto"))

    except Exception as e:
        print(f"Errore nella comunicazione con il server: {e}")

    # Esce con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
send_string("fine")
ser.close()

