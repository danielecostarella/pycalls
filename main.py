import requests
import datetime
import serial
import time
import threading

# include configs and credendials (API keys, tokens, passwords)
import config

# Global settings
TELEGRAM_NOTIFY=config.TELEGRAM_NOTIFY

# Serial Port configuration
serial_port= config.serial_port
baudrate = config.baudrate

# API Server
api_url = "http://localhost/api"

def setup_serial_port():
    try:
        ser = serial.Serial(serial_port, 9600, timeout=1)
    except serial.SerialException as e:
        print(f"Error: {e}")
        exit()
    return ser

def modem_serial_init(ser):
    ser.write("ATZ\r\n".encode())
    time.sleep(1)
    ser.write("ATE0 #CID=1\r\n".encode())
    time.sleep(1)

def close_serial_port(ser):
    ser.close()

def read_cid_data(ser):
    """
    Reads the incoming CID lines from the specified serial port and extracts the necessary information.

    Parameters:
    - port (str): The name of the serial port to use.
    """
    print("Waiting for calls...")
    while (1): #not exit_event.is_set():

        try:
            # Read the incoming CID lines from the Modem
            cid_data = {}
            while len(cid_data) < 3:
                line = ser.readline().decode().strip()
                if line.startswith("RING"):
                    print('RINGING')
                elif line.startswith('NMBR'):
                    cid_data['number'] = line.split(' = ')[1].strip()
                    print(line) # DEBUG
                elif line.startswith('TIME'):
                    cid_data['time'] = line.split(' = ')[1].strip()
                    print(line) # DEBUG
                elif line.startswith('DATE'):
                    cid_data['date'] = line.split(' = ')[1].strip()
                    print(line) # DEBUG

            # Check if all the necessary CID data has been received
            if len(cid_data) == 3:
                handle_incoming_call(cid_data)
                #return cid_data
            #else:
            #    return None
        except serial.SerialException as e:
            print(f"Error: {e}")
            #return None

def handle_incoming_call(cid_data):
    # Print the information about the incoming call
    print(f"Incoming call from {cid_data['number']} at {cid_data['time']} on {cid_data['date']}")

    url = api_url+"/calls"
    data = {"name": "3891111", "number": "", "category": "", "receivedOn": "2023-03-11T12:25:52.306Z"} #todo: sostituisci con Now
    
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()  # Get the current time in ISO 8601 format
    data["receivedOn"] = now  # Substitute the value of "receivedOn" with the current time

    caller = look_for_number(cid_data['number'])
    print(caller[0]['name'])
    data["name"] = caller[0]['name']
    data["number"]=cid_data['number']

    print("data to be stored:")
    print(data)

    if (TELEGRAM_NOTIFY):
        message = data["name"]+ " calling from "+cid_data['number']
        send_telegram_notification(message)
    
    response = requests.post(url, json=data)


def look_for_number(number):
    url = api_url+"/find-contact-by-number"+"/"+number
    headers = {'accept': 'application/json'}

    status_code = 0
    data = [{"name": "", "number": "", "category": "", "receivedOn": ""}, status_code]
    response = requests.get(url)

    print("Url got: "+str(response))
    if response.status_code == 200:
        # The request was successful, print the response body
        print(response.json())
    elif response.status_code == 404:
        # Resource not found
        data[0]["name"]="Unknown"
        data[0]["number"]=number
        data[1] = response.status_code
        print(data)
        print("Error: Resource not found")

        #print(response.json())
        return data
    else:
        # An error occurred, print the status code and response body
        print(f"Error {response.status_code}: {response.text}")

    return response.json()

from telegram_sender import TelegramSender
def send_telegram_notification(message):
    sender = TelegramSender(config.bot_token, config.api_id, config.api_hash, config.phone)
    sender.send_message(message)
    sender.disconnect()

def main():
    # Start the thread to read the incoming CID data from the Arduino Uno
    ser = setup_serial_port()
    
    # Inizialize modem
    print("Inizialing modem...")
    modem_serial_init(ser)

    exit_event = threading.Event()
    # Issue: https://github.com/LonamiWebs/Telethon/issues/1253
    #thread = threading.Thread(target=read_cid_data, args=(ser, exit_event))
    #thread.start()

    # Wait for the thread to finish or for the user to interrupt the program
    try:
        read_cid_data(ser)
    except KeyboardInterrupt:
        # Time to exit
        exit_event.set()
        
        # Close the serial port
        close_serial_port(ser)
        print("Serial closed")
        print("Interrupted")

if __name__ == '__main__':
    main()