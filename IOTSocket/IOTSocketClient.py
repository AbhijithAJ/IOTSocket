'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/

'''
import socket
import ssl
import time

data_maxLength = 65535
fields_maxLength =1024
sock = ''
device_id = ''
device_key = ''
time_stamps = []

def connectionSet(host, port, id_, key, Encrypt=1, cert_path=None):
    global sock, device_id, device_key, time_stamps
    device_id = id_
    device_key = key
    time_stamps = []
    sock = socket.create_connection((host, port))
    if Encrypt == 1:
        ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT).load_verify_locations(cert_path)
        sock = ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    sock.settimeout(1)

def chkTime(server_time, device_time):
    """
    Check if the time matches the server time and 
    to make sure there are no reused time (no replay attacks) 
    """
    global time_stamps
    time_drop_max = 3  # packet with time difference 30sec will not be accepted
    device_time = float(device_time)
    server_time = float(server_time)
    if(server_time in time_stamps):
        return False
    else:
        if len(time_stamps) < 100:
            time_diff = abs(device_time - server_time)
            if len(time_stamps) > 1:           # to remove old time stamps (to reduce memory usage)
                if (abs(time_stamps[-1] - server_time) > time_drop_max):
                    time_stamps = []
            if (time_diff > time_drop_max):
                return 0
            elif (time_diff < time_drop_max):
                time_stamps.append(server_time)
                return 1
        else:
            raise Exception(
                "ERROR: DOS attack more than 100 req from "+str(device_id))

def recvData():
    # time_now = str(datetime.now().time())           # 15:13:54.420103
    # time_now = time_now.replace(':', '.')
    time_now = f'{time.time():.4f}'
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
        while '' in data:
            data.remove('')
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
    time_now = f'{time.time():.4f}'
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
