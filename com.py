#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import serial
import struct
import crc
import time



def get_hilo(txt):
	tmp ="0000"+txt
	tmplo = int(tmp[-2:])
	tmphi = int(tmp[-4:-2:])
	return tmphi, tmplo

def get_analog_com(in_date):
	date_hi = in_date[3]
	date_lo = in_date[4]
	value = int(date_hi*255)+int(date_lo)
	value = float('{:.1f}'.format(value*0.1))
	return value

class Comport():
	def __init__(self, port, baudrate):
		self.port = port
		self.baudrate = baudrate
		self.com_0 = serial.Serial()
		self.com_0.method = 'rtu'
		self.com_0.port = self.port
		self.com_0.baudrate = self.baudrate
		self.com_0.bytesize = 8
		self.com_0.parity = 'N'
		self.com_0.stopbits = 1
		self.com_0.timeout = 0.1
	
	def up(self):	
		self.com_0.open()

	def down(self):
		self.com_0.close()

	def get_analog_4(self, id, reg):
		self.id = id
		self.reg = str(reg)
		reg_hi, reg_lo = get_hilo(self.reg)
		send =[]
		send.append(self.id)
		send.append(4)
		send.append(reg_hi)
		send.append(reg_lo)
		send.append(0)
		send.append(1)
		crc_hi, crc_lo = crc.crc16(send)
		send.append(crc_hi)
		send.append(crc_lo)
		pack_style = str(len(send)) + 'B'
		send = struct.pack(pack_style, *send)
		self.com_0.write(send)
		get = self.com_0.read(16)
		unpack_style = str(len(get)) + 'B'
		get = struct.unpack(unpack_style, get)
		get = get_analog_com(get)
		return get


#serial_port = Comport('com4', 9600)
#serial_port.up()

#print('Температура 1 = ' + str(serial_port.get_analog_4(3, 13)))
#print('Температура 1 = ' + str(serial_port.get_analog_4(3, 14)))

#serial_port.down()

if __name__ == "__main__":
    pass
