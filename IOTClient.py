'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/

'''
'''
client for raspberry 
'''

from IOTSocket import IOTSocketClient as sock
import time

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
    now = time.time()
    if ((now - prev_call) > 10) or prev_call == 0:
        example = 'temp=33.5&humid=40%'
        prev_call = now
        return example
    else:
        return ''

def handleCmdsFromServer(data):
    '''
    This function is called when ever there is 
    data/command from the server.
    '''
    print(data)

while 1: # reconnect if socket is closed
    try:
        sock.connectionSet(host,port,device_id,device_key,Encrypt=False, cert_path= certfile_path)  # set IOT Socket connection with valid Device ID and Key.
        # Continiously check for receiving / tansmiting of data
        while 1:
            data = someThingtoSend()
            if data != '':
                sock.sendData(data)     # send data to server if data is available to send
            rcv_data = sock.recvData()  # receive data from server if available
            if len(rcv_data) > 5:
                handleCmdsFromServer(rcv_data)   # handle your data here

    except Exception as n:
        print(n)
