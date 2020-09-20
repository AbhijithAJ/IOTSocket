<h1 align="center">
  IoTSocket v1.0
<div align="center">

[![Generic badge](https://img.shields.io/badge/Made_By-ABHIJITH_BOPPE-BLUE.svg)](https://www.linkedin.com/in/abhijith-boppe/)  
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Generic badge](https://img.shields.io/badge/pypi_package-1.0-DARKGREEN.svg)](https://pypi.org/project/IOTSocket/) [![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://github.com/AbhijithAJ/IOTSocket/blob/master/LICENSE) [![PayPal](https://img.shields.io/badge/donate-PayPal-blue.svg)](https://www.paypal.me/abhijithboppes)     
</div>


</h1>

 - Time based verification
 - TLS/SSL 
 - TCP/IP
 - Device Validation
---
## ABOUT

IOT Socket Server handle multiple clients (with unique deviceID and its key) simultaneously for bidirectional communication.
It is similar to WebSocket. Here we can handle each client individually from there device id.

IOT devices like Raspberry can also use this module as client with IOTSocketClient module.


**How is it secured ?**

To prevent Replay attacks and device cloning attacks.

For every data transmission from client to server or vice versa there is a time stamp which is compared with server/client present time. If the time doesn't match (tolerance of -2 sec) or if there is any reused time then socket is closed.

By using these headers for every transmission, IOT devices over WiFi can also be secured.

*NOTE:*
- Make sure the device time is in sync with server time (use RTC)
- Re-establish client socket connection every 24 hours
- SSL key pinning on client-side.
- Verify device id and key from database
- Client socket will be closed if there is no data for 90 sec

### Installation
You can install IOTSocket by running the following command
```
pip install IOTSocket
```
### Example Server
```python
'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/
'''
from IOTSocket import IOTSocketServer, IOTSocketServerSSL, IOTSocket
import time
from clrprint import *

host = "127.0.0.1"
port = 9000

# give certificate path and key path
certfile_path = "/user/cert.pem"
keyfile_path = "/user/cert.key"
delimiter = '\r\n#*\r\n'

# give some insecure data te be filtered and sanitized to ''
lst_of_data_to_remove = [delimiter]
prev_call = 0

# this function will be called recursively to check if server want to push any data
def from_server_to_client():
    '''
    create a FIFO named pipe, make your backend application like PHP
    to write into it and you return a list. Like: ['id1 data1', 'id2 data2', 'id3 data3', .....]

    Ex: ['23234 ON SWITCH 1','23235 OFF LIGHT','232365 GET ALL SENSOR VALUES']
    (id must be numaric values only)
    
    '''
    return []

class handleEachClientHere(IOTSocket):
    def DeviceVerify(self, id_, key):          # 'id_' - int , 'key' - string
        '''
        This method is called when a new client is connected.
        Verify whether device id and key matches in database records
        and check if it is activated.
        (Check from DB)
        '''        
        return 1    #return True if verified successfully else false

    def handleMessage(self, id_, data):
        '''
        handle client id and data for further processing.
        create a fifo named pipe and pass the data to your
        backed application

        (make sure u remove delimiters and other vulnerable strings which effect the backend application)
        '''
        for i in lst_of_data_to_remove:         # remove delimiters/data, if any are present in client data to prevent clashes
            data.replace(i, '')
        clrprint(id_, data,clr='b')

    def handleClose(self, error_repo=''):
        '''
        handle error if any during socket handling
        error start with "ERROR: "
        and normal socket close will end with normal message
        '''
        if "ERROR:" in str(error_repo):
            clrprint(error_repo,clr='r')
        else:
            pass

clrprint(f"Server started listening on socket {host}:{port}", clr='g')
server = IOTSocketServer(host, port, from_server_to_client,handleEachClientHere)        # without ssl
# server = IOTSocketServerSSL(host, port, from_server_to_client, handleEachClientHere, certfile = certfile_path, keyfile = keyfile_path)
server.serveforever()
```
### Example client
```python

'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/

client example for raspberry 
'''

from IOTSocket import IOTSocketClient as sock
import time
from clrprint import *

host = '127.0.0.1'
port = 9000
device_id = '1234567890'
device_key ='1432qrzd23'
certfile_path = "/user/cert.pem"      # for key pinning (certificate pinning)
prev_call = 0

def someThingtoSend():
    '''
    this function is called recursively.
    read data from sensor and return data
    '''
    global prev_call
    time_now = time.time()
    if (abs(time_now - prev_call) > 10) or prev_call == 0: # send sensor data every 10 seconds
        example = 'temp=33.5&humid=40%'
        prev_call = time_now
        return example
    else:
        return ''

def handleCmdsFromServer(data):
    '''
    This function is called when ever there is 
    data/command from the server.
    '''
    clrprint(data,clr='b')

while 1: # reconnect if socket is closed
    try:
        clrprint(f"\nEstablishing socket connection to {host}:{port}",clr='y')
        sock.connectionSet(host,port,device_id,device_key,Encrypt=False, cert_path= certfile_path)  # set IOT Socket connection with valid Device ID and Key.
        # Continuously check for receiving / transmitting of data
        clrprint(f"Connection established successfully",clr='g')
        while 1:
            data = someThingtoSend()
            if data != '':
                sock.sendData(data)     # send data to server if data is available to send
            rcv_data = sock.recvData()  # receive data from server if available
            if len(rcv_data) > 5:
                handleCmdsFromServer(rcv_data)   # handle your data here

    except Exception as n:
        clr = 'r' if "ERROR:" in str(n) else 'y'
        clrprint(n,clr='r')
        clrprint('closing socket',clr='y')      
        try:
            sock.sock.close()
        except:
            pass
        time.sleep(10)
        

```

### Additional Information

The connection is established directly on 1st request from client. Make sure the client and server time are in sync.

Read/Write to your application from using fifo named pipe recursively without closing. 

Please go through the code for better understanding of the protocol.

<br>
<a href="https://www.buymeacoffee.com/abhijithboppe" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" width="55%" ></a>

---
## License & copyright
© Abhijith Boppe, Security analyst

linkedin.com/in/abhijith-boppe

Licensed under the [MIT License](LICENSE)
