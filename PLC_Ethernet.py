import socket
import threading
import time


class PLC_Ethernet:

    def __init__(self,server_ip,server_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((server_ip, server_port))
        print 'waiting for connect...'
        # Connect SOCKET(IP.PORT)
    def send(self,input_msg,input_msg2,input_msg3): 
        try:  
            value = input_msg
            value2 = input_msg2
            value3 = input_msg3
            WRITES = "WRS"+"20".decode("hex")+"CM7002"+"20".decode("hex")+"03"+"20".decode("hex")+value+"20".decode("hex")+value2+"20".decode("hex")+value3+"0D".decode("hex")
            # Continue write "3" value . starting with "CM7002" .the register is CM7002.CM7003.CM7004.
            self.server.sendall(WRITES)
            time.sleep(0.2)
            Rx = self.server.recv(1024)
            self.rec_msg = Rx 
            print 'Command translate is : ' + Rx 

        except Exception as e:
            print e
            print('transfrom hex fail')


    def receive(self): 
        try:  
            
            READS = "RDS"+"20".decode("hex")+"CM7002"+"20".decode("hex")+"3"+"0D".decode("hex")
            # Continue read "3" value.starting with "CM7002" .the register is CM7002.CM7003.CM7004.  
            self.server.sendall(READS)
            time.sleep(0.2)
            Rx = self.server.recv(1024)
            self.rec_msg = Rx
            print 'Register value is : ' + Rx 
            PCRead = Rx
            if PCRead == "00045 00046 00047\r\n":
                print "nmsl"
                print "Taiwan No.1"
            # If the read value is "00045 00046 00047 \r\n" .the string will be printed.
        except Exception as e:
            print e
            print('transfrom hex fail')




if __name__ =='__main__':
    plc = PLC_Ethernet('192.168.4.101',8501)
    # Connect PLC(IP.PORT).
    while True :
 
        print('Enter CM7002 Value: ')
        input_msg = raw_input()
        print('Enter CM7003 Value : ')
        input_msg2 = raw_input()
        print('Enter CM7004 Value : ')
        input_msg3 = raw_input()
        plc.send(input_msg,input_msg2,input_msg3)
        time.sleep(0.2)
        plc.receive()

