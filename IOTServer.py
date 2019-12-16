'''
Developed by Abhijith Boppe - linkedin.com/in/abhijith-boppe/

'''
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
    to write into it make sure u return list in format
    ['id1 data1','id2 data2', 'id3 data3'...... ]

    '''
    return []

class handleEachClientHere(IOTSocket):

    def DeviceVerify(self, id_, key):          # 'id_' - int , 'key' - string
        '''
        Verify weather device id and key matches in database records
        and check if it is activated.
        Check from db 
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
