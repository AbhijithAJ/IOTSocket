# Secured IOT Socket Server 

 - Time based verification
 - TLS/SSL 
 - Device Validation

## ABOUT

IOT Socket Server handle multiple clients (with unique deviceID and its key) simultaneously for bidirectional communication.
It is similar to websocket. Here we can handle each client individually from there device id.

IOT devices like Raspberry can also use this module as client with IOTSocketClient module.


**How is it secured ?**

To prevent Replay attacks and device cloning attacks, every data transmission from client to server or vice versa there is a time stamp which is compared with server/client present time. If the time doesn't match (tolerance of -3 sec) or if there is any reused time then socket is closed.

By using these headers for every transmission, IOT devices over WiFi can also be secured.

*NOTE:*
- Make sure the device time is in sync with server time (use RTC)
- Re-establish client socket connection every 24 hours
- SSL key pinning on client side.
- Verify device id and key from database
- Client socket will be closed if there is no data for 90 sec

### Installation
You can install IOTSocket by running the following command
```
sudo python setup.py install
```
### Example Server
```python
from IOTSocket import IOTSocketServerSSL, IOTSocket
import time
host = "0.0.0.0"
port = 9000

certfile_path = "/root/cert.pem"
keyfile_path = "/root/cert.key"
delimiter = '\r\n#*\r\n'
# give some insecure data te be filtered and sanitized to ''
lst_of_dataToBeRemoved = [delimiter]
prev_call = 0

# this function will be called recursively to check if server want to push any data
def from_server_to_client():
    '''
    create a fifo named pipe make u r backend application like php
    to write into it. Make sure you return list in format
    ['id1 data1','id2 data2', 'id3 data3'...... ]

    '''
    return []

class handleEachClientHere(IOTSocket):

    def DeviceVerify(self, id_, key):          # 'id_' - int , 'key' - string
        '''
        Verify weather device id and key matches in database records
        and check if it is activated and return 1
        else 0
        '''
        return 1

    def handleMessage(self, id_, data):
        '''
        handle client id and data for further processing.
        create a fifo named pipe and pass the data to your 
        backed application       
        '''
        for i in lst_of_dataToBeRemoved:            # remove delimiters/data if any are present in client data to prevent clashes
            data.replace(i, '')
        print(id_, data)

    def handleClose(self, error_repo=''):
        '''
        handle error if any during socket handling
        error start with "ERROR: " 
        and normal close will end with normal message
        '''
        if "ERROR:" in str(error_repo):
            print(error_repo)
        else:
            pass
# server = IOTSocketServer(host,port,from_server_to_client, handleEachClientHere)        # without ssl
server = IOTSocketServerSSL(host, port, from_server_to_client,
                            handleEachClientHere, certfile=certfile_path, keyfile=keyfile_path)
server.serveforever()
```
### Example client
```python

from IOTSocket import IOTSocketClient as s
import time
'''
client for raspberry 
'''
host = '127.0.0.1'
port = 9000
device_id = '1234567890'
device_key ='1432qrzd23'
certfile_path = "/root/cert.pem"      # for key pinning (certificate pinning)
prev_call = 0

def someThingtoSend():
    '''
    read data from sensor for every 10 sec 
    '''
    global prev_call
    now = time.time()
    if ((now - prev_call) > 10) or prev_call == 0:
        example = 'temp=33.5&humid=40%'
        prev_call = now
        return example
    else:
        return ''

def handleCmdsFromServer(data):
    print(data)

while 1: # reconnect if socket is closed
    try:
        s.connectionSet(host,port,device_id,device_key,Encrypt=True, cert_path= certfile_path)  # set IOT Socket connection with valid Device ID and Key. 
        # Continuously check for receiving / transmitting of data
        while 1:
            data = someThingtoSend()
            if data != '':
                s.sendData(data)     # send data to server if data is available to send
            rcv_data = s.recvData()  # receive data from server if available
            if len(rcv_data) > 5:
                handleCmdsFromServer(rcv_data)   # handle your data here

    except Exception as n:
        print(n)



```

### Additional Information

There is no hand shake. Connection is established directly on 1st request from client. Make sure the client and server time are in sync.

Read/Write to your application from using fifo named pipe recursively without closing. 

Please go through the code for better understanding of the protocol.

---
## License & copyright
© Abhijith Boppe, Security analyst

linkedin.com/in/abhijith-boppe

Licensed under the [MIT License](LICENSE)
