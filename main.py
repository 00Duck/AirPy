import configparser
import datetime
import serial
import requests

"""
    Documentation for the SDS011: https://microcontrollerslab.com/nova-pm-sds011-dust-sensor-pinout-working-interfacing-datasheet/
    PDF URL: https://microcontrollerslab.com/wp-content/uploads/2020/12/NonA-PM-SDS011-Dust-sensor-datasheet.pdf

    0   Message Header  AA
    1   Commander No.   C0
    2   DATA 1          PM2.5 Low
    3   DATA 2          PM2.5 High
    4   DATA 3          PM10 Low
    5   DATA 4          PM10 High
    6   DATA 5          ID byte 1
    7   DATA 6          ID byte 2
    8   Check-sum       Check-sum
    9   Message Tail    AB
"""

def load_settings() -> dict:
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        return {
            "protocol": config["server"]["protocol"],
            "address": config["server"]["address"],
            "port": config["server"]["port"],
            "device_path": config["SDS011"]["device_path"],
            "baudrate": config["SDS011"]["baudrate"]
        }
    except:
        print('failed to open or read config.ini. Please make sure the file exists and contains the following format:')
        print('[server]\nprotocol=<protocol>\naddress=<address>\nport=<port>\n\n[SDS011]\ndevice_path=<device_path>\nbaudrate=<baudrate>')
        exit(1)

def measure(device_path, baudrate) -> tuple[int, int]:
    msg_head = b'\xaa'
    msg_tail = b'\xab'

    try:
        with serial.Serial(device_path, baudrate=baudrate) as ser:
            bytes_data = ser.read(10) #blocks until 10 bytes of data are read

            #convert bytes to an array of bytes
            bytes_arr = [bytes_data[i:i + 1] for i in range(0, len(bytes_data))]
            
            #ensure message head/tail matches per spec or throw this data away
            if bytes_arr[0] != msg_head:
                print("Send failed: message header not present")
                return (None, None)

            if bytes_arr[9] != msg_tail:
                print("Send failed: message tail not present")
                return (None, None)

            #Checksum at position 8 and should equal DATA1 + ... + DATA6 (positions 2-7)
            checksum_test = sum([int.from_bytes(bytes_data[i:i + 1], byteorder='little') for i in range(2, 8)])
            checksum = int.from_bytes(bytes_arr[8], byteorder='little')

            if checksum_test != checksum:
                print("Send failed: checksum did not pass")
                return (None, None)

            #Bytes 2 and 3 are the PM2.5 low and high bytes, respectively
            pm_two_five = int.from_bytes(b''.join(bytes_arr[2:4]), byteorder='little') / 10

            #Bytes 4 and 5 are the PM10 low and high bytes, respectively
            pm_ten = int.from_bytes(b''.join(bytes_arr[4:6]), byteorder='little') / 10

            return (pm_two_five, pm_ten)
    except Exception as e:
        print("Send failed: " + str(e))
        return (None, None)

def main() -> None:
    settings = load_settings()
    now = datetime.datetime.utcnow()
    data_to_send = measure(settings["device_path"], settings["baudrate"])
    if data_to_send != (None, None):
        data_to_send = {"pm_two_five": data_to_send[0], "pm_ten": data_to_send[1], "measured_at": now.strftime('%Y-%m-%d %H:%M:%S')}
        try:
            requests.post('{0}://{1}:{2}'.format(settings["protocol"], settings["address"], settings["port"]), data=data_to_send)
        except Exception as e:
            print('Send failed: ' + str(e));

if __name__ == "__main__":
    main()