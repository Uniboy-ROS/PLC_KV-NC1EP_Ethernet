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
                self.server.settimeout(1)
                self.server.connect((ip, port))
                print ip + ' connected!'
                connedted = True

            except socket.error as e:
                print("Error -->"+str(e))
                print("WARNING Connecttime is over!!!\r\n")
                print("Please reconnect thx\r\n")

    def check_type(self,register_type):
        if (register_type == 'R' or register_type == 'B' or register_type == 'MR' 
        or register_type == 'LR' or register_type == 'CR' or register_type == 'T'
        or register_type == 'C' or register_type == 'CTC' or register_type == 'VB' 
        or register_type == 'DM' or register_type == 'CM' or register_type == 'EM' 
        or register_type == 'FM' or register_type == 'ZF' or register_type == 'W' 
        or register_type == 'TM' or register_type == 'Z' or register_type == 'VM' 
        or register_type == 'TC' or register_type == 'TS' or register_type == 'CC'
        or register_type == 'CS' or register_type == 'AT') :   
            return True
        else:
            print 'register_type format error'
            print 'register_type should be  R or B or MR or LR or CR or T or C or CTC or VB !!!\r\n' 
            return False

    def check_id(self,register_id):
        if type(register_id) == int and register_id >= 0:   
            return True
        else:
            print 'register_id format error'
            print 'register_id should be Positive Integer !!!\r\n' 
            return False

    def check_format(self,data_format):
        if (data_format == '' or data_format == '.U' or data_format == '.S'
        or data_format == '.D' or data_format == '.L' or data_format == '.H'):
            return True
        else:
            print 'data_format error'
            print 'data_format should be none or .U or .S or .D or .L or .H !!!\r\n' 
            return False

    def force_set(self,register_type,register_id):
        if self.check_type(register_type) and self.check_id(register_id):
            for i in range(0,3,1):
                try:
                    register_id = str(register_id)
                    SET = "ST" + "20".decode("hex") + register_type + register_id + "0D".decode("hex")
                    # SET = "ST" + ' ' + register_type + register_id + "0D".decode("hex")
                    self.server.sendall(SET)
                    Rx = self.server.recv(1024)
                    self.rec_msg = Rx 
                    if Rx == "OK\r\n" :
                        print "set successed"
                        return True
                        # start = True
                    elif Rx == "E1\r\n":
                        print "Command error"
                        return False
                    elif Rx == "E0\r\n":
                        print "Register number error"
                        return False
                except socket.error as e:            
                    print("Error -->"+str(e))
                    # plc.force_set(register_type,register_id) 危險
                    self.server.sendall(SET)

        else:
            return False

           
          
    def force_reset(self,register_type,register_id):
        if self.check_type(register_type) and self.check_id(register_id):
            for i in range(0,3,1):
                try:
                    register_id = str(register_id)
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

        else:
            return False


    def continous_force_set(self,register_type,start_register_id,number):
        if self.check_type(register_type) and self.check_id(start_register_id):
            for i in range(0,3,1):
                try:
                    start_register_id = str(start_register_id)
                    number = str(number)
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

        else:
            return False

    def continous_force_reset(self,register_type,start_register_id,number):
        if self.check_type(register_type) and self.check_id(start_register_id):
            for i in range(0,3,1):
                try:
                    start_register_id = str(start_register_id)
                    number = str(number)
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

        else:
            return False

    def data_read(self,register_type,register_id,data_format=''):
        if self.check_type(register_type) and self.check_id(register_id) and self.check_format(data_format):
            for i in range(0,3,1):
                try:
                    register_id = str(register_id)
                    READ = "RD" + "20".decode("hex") + register_type + register_id + data_format  + "0D".decode("hex")
                    self.server.sendall(READ)
                    time.sleep(0.2)
                    Rx = self.server.recv(1024)
                    self.rec_msg = Rx
                    print 'The register format is : ' + data_format
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
        else:
            return False
        # 繼電器*2 R（可省略） 00000~199915*4 （位） 0001~1000 0001~0500
        # 鏈路繼電器B 0000~7FFF （位） 0001~1000 0001~0500
        # 內部輔助繼電器*2 MR 00000~399915*3 （位） 0001~1000 0001~0500
        # 鎖存繼電器*2 LR 00000~99915 （位） 0001~1000 0001~0500
        # 控制繼電器CR 0000~7915 （位） 0001~1000 0001~0500
        # 工作繼電器VB 0000~F9FF （位） 0001~1000 0001~0500
        # 資料記憶體*2 DM 00000~65534 .U 0001~1000 0001~0500


    def consecutive_data_read(self , register_type , start_register_id , data_format , number):
        if self.check_type(register_type) and self.check_id(start_register_id) and self.check_format(data_format):
            for i in range(0,3,1):
                try:
                    start_register_id = str(start_register_id)
                    number = str(number)
                    READS = "RDS" + "20".decode("hex") + register_type + start_register_id + data_format + "20".decode("hex") + number + "0D".decode("hex")
                    self.server.sendall(READS)
                    time.sleep(0.2)
                    Rx = self.server.recv(1024)
                    self.rec_msg = Rx
                    print 'The registers format are : ' + data_format
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
        else:
            return False
        # data_format 
        # .U : Decimal, 16bit, unsigned 
        # .S : Decimal, 16bit, signed 
        # .D : Decimal, 32bit, unsigned 
        # .L : Decimal, 32bit, signed 
        # .H : Hex, 16bit

    def write_data(self,register_type,register_id,data_format,data):
        if self.check_type(register_type) and self.check_id(register_id) and self.check_format(data_format):
            for i in range(0,3,1):
                try:
                    register_id = str(register_id)
                    data = str(data)
                    WRITE = "WR"+"20".decode("hex")+ register_type + register_id + data_format + "20".decode("hex") + data + "0D".decode("hex")
                    self.server.sendall(WRITE)
                    time.sleep(0.2)
                    Rx = self.server.recv(1024)
                    self.rec_msg = Rx

                    print data

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
        else:
            return False

    def consecutive_write_data(self,register_type,start_register_id,data_format,data_list):
        if self.check_type(register_type) and self.check_id(start_register_id) and self.check_format(data_format):
            data_value = str(len(data_list)) + ' '
            for data in data_list:
                data_value = data_value + str(data) + ' '
            data_value = data_value[0:-1]
            # print data_value
            for i in range(0,3,1):
                try:
                    start_register_id = str(start_register_id)               
                    # data_list = amount+' '+value1+' '+value2+' '+value3
                    # b = len(data_list)
                    # c = str(b)
                    # data_list.insert(0,c)
                    # space = ' '
                    # data_list = space.join(data_list)

                    WRITES = "WRS"+"20".decode("hex")+register_type+start_register_id+data_format+"20".decode("hex")+data_value+"0D".decode("hex")
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

        else:
            return False



if __name__ =='__main__':
    plc = Keyence_PLC_Ethernet('192.168.4.101',8501)
    # input_msg = raw_input()
    # plc.force_reset('MR',4)
    
    # plc.data_read('DM',1,'.S')
    # plc.data_read('DM',2,'.X')
    # plc.data_read('DM',4,'.S')
    # plc.data_read('CM',7100,'.L')
    # plc.data_read('R',515)
    # plc.consecutive_data_read('R',506,'',3)
    
    # plc.write_data('CM',7100,'.L',-123)
    
    a = [1,2,35,-4,6]
    b = [52784616,27365317]

    plc.consecutive_write_data('DM',10,'.D',b)
    # plc.continous_force_reset('R',506,3)
    # plc.consecutive_data_read('R',506,3)

        

        

