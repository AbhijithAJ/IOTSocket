'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/

'''
import socket
import ssl
from datetime import datetime

data_maxLength = 65535
fields_maxLength =1024
sock = ''
device_id = ''
device_key = ''
time_stamps = []

def connectionSet(host, port, id_, key, Encrypt=1, cert_path=None):
    global sock, device_id, device_key
    device_id = id_
    device_key = key
    sock = socket.create_connection((host, port))
    if Encrypt == 1:
        ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT).load_verify_locations(cert_path)
        sock = ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    sock.settimeout(1)

def chkTime(device_time, server_time):
    """
    Check if the time matches the server time and 
    to make sure there are no reused data 
    """
    global time_stamps
    frmt = "%H.%M.%S.%f"
    time_drop_max = 3  # packet with time difference 30sec will not be accepted
    if(device_time in time_stamps):
        return False
    else:
        if len(time_stamps) < 100:
            time = datetime.strptime(
                device_time , frmt) - datetime.strptime(server_time, frmt)
            if len(time_stamps) > 1:           # to remove old time stamps (to reduce memory usage)
                stamps_time = datetime.strptime(
                    time_stamps[-1], frmt) - datetime.strptime(server_time, frmt)
                if (stamps_time.seconds > time_drop_max):
                    time_stamps = []
            if (time.seconds > time_drop_max):
                return 0
            elif (time.seconds < time_drop_max):
                time_stamps.append(device_time)
                return 1
        else:
            raise Exception(
                "ERROR: DOS attack more than 300 req from "+str(device_id))

def recvData():
    time_now = str(datetime.now().time())           # 15:13:54.420103
    time_now = time_now.replace(':', '.')
    try:
        # 65535 max data (including headers)
        data = sock.recv(data_maxLength)
    except socket.timeout as _:
        data = b''
        pass
    except Exception as _:
        raise Exception("socket closed/refused by server")
    data = data.decode()
    if not data:
        return ''
    else:
        data = data.split('|#|')   # split data at delimeter
        del data[-1]
        for data in data:
            # split headers and data
            fields, data = data.split("\r\n\r\n", 1)
            fields, data = fields.strip() if len(
                fields) < fields_maxLength else 0, data.strip() if len(data) < (data_maxLength-3000) else 0
            headers = {}
            for field in fields.split('\r\n'):
                # split each line by http field name and value
                key, value = field.split(':')
                headers[key] = value
                if len(headers) > 10:
                    break
            if len(headers) != 5 or len(data) < 5:
                raise Exception("ERROR: Headers issue ")
            else:
                if(headers['IOT'] == '1.1'):
                    time_chk = chkTime(headers['TIME'], time_now)
                    if(time_chk):
                        return data
                    else:
                        raise Exception(
                            "ERROR: Incorrect time stamp "+headers['TIME'])
                else:
                    raise Exception(
                        "ERROR: Incorrect IOT version detected ")
                        
def _headers():
    time_now = str(datetime.now().time())
    time_now = time_now.replace(':','.')
    headers = '''IOT:1.1
DATE:12/12/2019
TIME:{time_now}
DEVICE:{device_id}
KEY:{device_key}


'''.format(time_now=time_now, device_id= device_id, device_key=device_key)
    return headers

def sendData(data):
    if len(data) > 5 and len(data) < 60000:
        try:
            headers = _headers()
            data = headers.replace('\n','\r\n') + data.replace('|#|','') + '|#|'
            sock.send(data.encode())      
        except socket.timeout as e:
            print (e)
        except Exception as e:
            raise Exception("socket closed by server")

# ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None)
