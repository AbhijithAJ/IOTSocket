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
    (id must be numeric values only)
    
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

        (make sure u remove delimeters and other vulnerable strings which effect the backend application)
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
