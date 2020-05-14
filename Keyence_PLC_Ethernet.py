#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time


class Keyence_PLC_Ethernet:

    def __init__(self,ip,port):
        connedted = False
        while not connedted:
            try:
                print 'waiting for connect...'
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.settimeout(3)
                self.server.connect((ip, port))
                print ip + ' connected!'
                connedted = True

            except socket.error as e:
                print("Error -->"+str(e))
                print("WARNING Connecttime is over!!!\r\n")
                print("Please reconnect thx\r\n")


    def force_set(self,register_type,register_id):
        for i in range(0,3,1):
            try:   
                SET = "ST" + "20".decode("hex") + register_type + register_id + "0D".decode("hex")
                # SET = "ST" + ' ' + register_type + register_id + "0D".decode("hex")
                self.server.sendall(SET)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx 

                if Rx == "OK\r\n" :
                    print "force_set OK"
                elif Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return 
            
            except socket.error as e:            
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(SET)

             
          
            
    def force_reset(self,register_type,register_id):
        for i in range(0,3,1):
            try:
                RESET = "RS" + "20".decode("hex") + register_type + register_id + "0D".decode("hex")
                self.server.sendall(RESET)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx 

                if Rx == "OK\r\n" :
                    print "force_reset OK"
                elif Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return
                
            except socket.error as e:
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(RESET)



    def continous_force_set(self,register_type,start_register_id,number):
        for i in range(0,3,1):
            try:
                SETS = "STS" + "20".decode("hex") + register_type + start_register_id + "20".decode("hex") + number + "0D".decode("hex")
                self.server.sendall(SETS)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx 

                if Rx == "OK\r\n" :
                    print "continous_force_set OK"
                elif Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return

            except socket.error as e:           
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(SETS)


    def continous_force_reset(self,register_type,start_register_id,number):
        for i in range(0,3,1):
            try:
                RESETS = "RSS" + "20".decode("hex") + register_type + start_register_id + "20".decode("hex") + number + "0D".decode("hex")
                self.server.sendall(RESETS)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx 

                if Rx == "OK\r\n" :
                    print "continous_force_reset OK"
                elif Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return

            except socket.error as e:
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(RESETS)

    def data_read(self,register_type,register_id):
        for i in range(0,3,1):
            try:
                READ = "RD" + "20".decode("hex") + register_type + register_id + "0D".decode("hex")
                self.server.sendall(READ)
                time.sleep(0.2)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx
                print 'The register value is : ' + Rx 

                if Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return

            except socket.error as e:
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(READ)

        # 繼電器*2 R（可省略） 00000~199915*4 （位） 0001~1000 0001~0500
        # 鏈路繼電器B 0000~7FFF （位） 0001~1000 0001~0500
        # 內部輔助繼電器*2 MR 00000~399915*3 （位） 0001~1000 0001~0500
        # 鎖存繼電器*2 LR 00000~99915 （位） 0001~1000 0001~0500
        # 控制繼電器CR 0000~7915 （位） 0001~1000 0001~0500
        # 工作繼電器VB 0000~F9FF （位） 0001~1000 0001~0500
        # 資料記憶體*2 DM 00000~65534 .U 0001~1000 0001~0500


    def consecutive_data_read(self,register_type, start_register_id,number):
        for i in range(0,3,1):
            try:
                READS = "RDS" + "20".decode("hex") + register_type + start_register_id + "20".decode("hex") + number + "0D".decode("hex")
                self.server.sendall(READS)
                time.sleep(0.2)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx
                print 'The registers value are : ' + Rx 

                if Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return

            except socket.error as e:
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(READS)

        # data_format 
        # .U : Decimal, 16bit, unsigned 
        # .S : Decimal, 16bit, signed 
        # .D : Decimal, 32bit, unsigned 
        # .L : Decimal, 32bit, signed 
        # .H : Hex, 16bit

    def write_data(self,register_type,register_id,data_format,data):
        for i in range(0,3,1):
            try:
                WRITE = "WR"+"20".decode("hex")+register_type+register_id+data_format+"20".decode("hex")+data+"0D".decode("hex")
                self.server.sendall(WRITE)
                time.sleep(0.2)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx

                if Rx == "OK\r\n" :
                    print "write_data OK"
                elif Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return

            except socket.error as e:
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(WRITE)

    def consecutive_write_data(self,register_type,start_register_id,data_format,data_list):
      
        for i in range(0,3,1):
            try:
                # data_list = amount+' '+value1+' '+value2+' '+value3
                data_list=' '
    
                for data in x:
                    data_list = data_list + data
                
                WRITES = "WRS"+"20".decode("hex")+register_type+start_register_id+data_format+"20".decode("hex")+data_list+"0D".decode("hex")
                self.server.sendall(WRITES)
                time.sleep(0.2)
                Rx = self.server.recv(1024)
                self.rec_msg = Rx

                if Rx == "OK\r\n" :
                    print "write_data OK"
                elif Rx == "E1\r\n":
                    print "Command error"
                elif Rx == "E0\r\n":
                    print "Register number error"
                return

            except socket.error as e:
                print("Error -->"+str(e))
                # plc.force_set(register_type,register_id) 危險
                self.server.sendall(WRITES)





if __name__ =='__main__':
    plc = Keyence_PLC_Ethernet('192.168.4.101',8501)
    input_msg = raw_input()
    plc.force_set('R','001')
    
    x = ['3',' ','9',' ','02',' ','68']
    plc.consecutive_write_data('CM','7002','.U',x)
    # plc.continous_force_reset('R','506','3')

    
    comment =  '''
    register_type = str
    register_id = str
    start_register_id = str
    number = str
    data_format = str
    data = str
    data_list = str
    

    while True:
        print('Which command do you want to use: ')
        input_msg = raw_input()
        if input_msg == "SET" or input_msg == "set" :
            plc.force_set(register_type,register_id)
        elif input_msg == "RESET" or input_msg == "reset" :
            plc.force_reset(register_type,register_id)
        elif input_msg == "SETS" or input_msg == "sets" :
            plc.continous_force_set(register_type,start_register_id,number) 
        elif input_msg == "RESETS" or input_msg == "resets" :
            plc.continous_force_reset(register_type,start_register_id,number)
        elif input_msg == "READ" or input_msg == "read" :
            plc.data_read(register_type,register_id)
        elif input_msg == "READS" or input_msg == "reads" :
            plc.consecutive_data_read(register_type,start_register_id,number)
        elif input_msg == "WRITE" or input_msg == "write" :
            plc.write_data(register_type,register_id,data_format,data)
        elif input_msg == "WRITES" or input_msg == "writes" :
            plc.consecutive_write_data(register_type,start_register_id,data_format,data_list)
        else :  
            print "Enter command error! try again!"

        '''
        

        

