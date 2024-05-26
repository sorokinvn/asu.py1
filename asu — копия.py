#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modbus_crc16 import crc16
import struct
import configparser
import serial
import pygame
import datetime
import tkinter as tk
from tkinter import*

# окно журнал
def window_event():
	w_event = tk.Toplevel()
	w_event.grab_set()
	w_event.iconbitmap('image/icon.ico')
	w_event.title('Журнал событий')
	w_event.geometry('640x480')
	w_event.resizable(0, 0)
	frame_w_event = Frame(w_event, width = 630, height = 470,
	relief = GROOVE, borderwidth = 2)
	frame_w_event.place(x = 5, y = 5)

# окно о программе
def window_about():
	w_a = tk.Toplevel()
	w_a.grab_set()
	w_a.iconbitmap('image/icon.ico')
	w_a.title('О программе')
	w_a.geometry('400x220')
	w_a.resizable(0, 0)
	frame_wa = Frame(w_a, width = 390, height = 210,
	relief = GROOVE, borderwidth = 2)
	frame_wa.place(x = 5, y = 5)
	ab_text = Text(frame_wa, width = 45, height = 8, font = "Arial 11",
		bg = 'snow2', relief = GROOVE, borderwidth = 2)
	ab_text.insert(INSERT, "Программа автоматизированного мониторинга\
		\nсистемы электроснабжения объекта КСА УВД\
		\nРГЦ ЕС ОрВД (Иркутск)\
		\n\
		\nПрограмма разаботана инженерно-техническим\
		\nперсоналом службы ЭРТОС\
		\n\
		\nversion: v.01     Иркутск 2021 г.")
	ab_text.configure(state = 'disabled')
	ab_text.place(x=10, y=10)
	bt_about = Button(frame_wa, width = 10, text = 'OK', command = w_a.destroy)
	bt_about.place(x = 295, y = 175)

# рисуем текущее время
def g_time():
	gdt = datetime.datetime.now()
	gdt = str(gdt.hour) + ":" + str(gdt.minute) + ":" + str(gdt.second)
	lb_time.configure(text = gdt)
	root.after(1000, g_time)

# проверяем flag_alarm и в случае если True выдаем аварию
def g_test():
	tmp = flag_alarm.get()
	if tmp == 1:
		lb_alarm.configure(image = image_alarm_red)
		pygame.mixer.music.play(-1)
	else:
		lb_alarm.configure(image = image_alarm_green)
		pygame.mixer.music.stop()
	root.after(1000, g_test)

# читаем config-файл
def read_config(num):
	num = str(num)
	ini = configparser.ConfigParser()
	ini.read('config_com.ini')
	com = serial.Serial()
	com.id = ini.get(num, 'id')
	com.method = ini.get(num, 'method')
	com.port = ini.get(num, 'port')
	com.baudrate = ini.getint(num, 'baudrate')
	com.bytesize = ini.getint(num, 'bytesize')
	com.parity = ini.get(num, 'parity')
	com.stopbits = ini.getint(num, 'stopbits')
	com.timeout = ini.getfloat(num, 'timeout')
	return com

# ПРОЦЕДУРА ВЫЧИСЛЕНИЯ Hi, Lo БАЙТ
def get_hilo(txt):
	tmp = "0000" + txt
	tmplo = int(tmp[-2:])
	tmphi = int(tmp[-4:-2:])
	return tmphi, tmplo

# ПРОЦЕДУРА ПРЕОБРАЗОВАНИЯ indate в десятичный вид
def get_analog_com(in_date, kn):
	datehi = in_date[3]
	datelo = in_date[4]
	value = int(datehi*255)+int(datelo)
	value = float('{:.1f}'.format(value*kn))
	return(value)	

#ПРОЦЕДУРА ЧТЕНИЯ АНАЛОГОВОГО ЗНАЧЕНИЯ (ТЕМПЕРАТУРЫ) ИЗ УСТРОЙСТВА
def RinTemp(com_s, id_name, addr):
	addr_hi, addr_lo = get_hilo(str(addr))
	send =[]
	send.append(int(id_name))
	send.append(4)
	send.append(addr_hi)
	send.append(addr_lo)
	send.append(0)
	send.append(1)
	crchi, crclo = crc16(send)
	send.append(crchi)
	send.append(crclo)
	packstyle = str(len(send)) + 'B'
	send = struct.pack(packstyle, *send)
	com_s.write(send)
	read_com = com_s.read (64)
	unpackstyle = str(len(read_com)) + 'B'
	read_com = struct.unpack(unpackstyle, read_com)
	return read_com

def get_value(com_n, ad, kn):
	value = RinTemp(com_n, com_n.id, ad)
	value = get_analog_com(value, kn)
	return value

# создаем главное окно программы
root = tk.Tk()
root.iconbitmap('image/icon.ico')
root.title('АСУ ДЭС РГЦ ЕС ОрВД Иркутск')
root.geometry('1024x768')
root.resizable(0, 0)

# инициализируем микшер и подгружаем звук аларма
pygame.mixer.init()
sound_alarm = pygame.mixer.music.load('sound/alarm.wav')

flag_alarm = BooleanVar()

# читаем ati_test из config-файл
com0 = read_config('ati_test')
com0_id = com0.id
com0_method = com0.method
com0_name = com0.port
com0_baudrate = com0.baudrate
com0_bytesize = com0.bytesize
com0_parity = com0.parity
com0_stopbits = com0.stopbits
com0_timeout = com0.timeout

com0.open()

print (get_value(com0, 34, 0.1))

# читаем ati_gep100 из config-файл
com1 = read_config('ati_gep100')
com1_id = com1.id
com1_method = com1.method
com1_name = com1.port
com1_baudrate = com1.baudrate
com1_bytesize = com1.bytesize
com1_parity = com1.parity
com1_stopbits = com1.stopbits
com1_timeout = com1.timeout

# читаем ati_gep110 из config-файл
com2 = read_config('ati_gep110')
com2_id = com2.id
com2_method = com2.method
com2_name = com2.port
com2_baudrate = com2.baudrate
com2_bytesize = com2.bytesize
com2_parity = com2.parity
com2_stopbits = com2.stopbits
com2_timeout = com2.timeout

# читаем ati_gep33 из config-файл
com3 = read_config('ati_gep33')
com3_id = com3.id
com3_method = com3.method
com3_name = com3.port
com3_baudrate = com3.baudrate
com3_bytesize = com3.bytesize
com3_parity = com3.parity
com3_stopbits = com3.stopbits
com3_timeout = com3.timeout

# загружаем картинку GEP
image_gep = PhotoImage(file = 'image/gep.png')

# загружаем картинку UPS
image_ups = PhotoImage(file = 'image/ups.png')
image_ups = image_ups.subsample(2, 2)

image_ups_srt = PhotoImage(file = 'image/ups_srt.png')
image_ups_srt = image_ups_srt.subsample(2, 2)

# загружаем картинку зеленой лампы
image_green = PhotoImage(file = 'image/green_light.png')
image_green = image_green.subsample(4, 4)

# загружаем картинку красной лампы
image_red = PhotoImage(file = 'image/red_light.png')
image_red = image_red.subsample(4, 4)

# создаем фрейм главного окна
frame_root = Frame(root, width = 1014, height = 758, relief = GROOVE, borderwidth = 2)
frame_root.place(x = 5, y = 5)

# создаем фрейм ВРУ_1 и GEP_100
frame_vru1 = Frame(frame_root, width = 550, height = 200,
	relief = GROOVE, borderwidth = 2)
frame_vru1.place(x = 110, y = 5)

# создаем картинку GEP_100
lb_gep100 = Label(frame_vru1, image = image_gep, relief = RIDGE, borderwidth = 2)
lb_gep100.place(x=5, y=5)

lb_t_gep100 = Label(frame_vru1, width = 9, text = 'GEP 100', font = "Arial 12 bold",
	bg = 'orange', relief = RIDGE, borderwidth = 2)
lb_t_gep100.place(x=57, y=153)

lb_s_gep100 = Label(frame_vru1, width = 12, text = 'ОСТАНОВЛЕН', font = "Arial 12 bold",
	bg = 'spring green', relief = RIDGE, borderwidth = 2)
lb_s_gep100.place(x=160, y=153)

# создаем надписи дополнительных параметров GEP_100
sw_pos_t_gep100 = Label(frame_vru1, width = 7, text = 'SW_POS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
sw_pos_t_gep100.place(x=426, y=5)

key_pos_t_gep100 = Label(frame_vru1, width = 7, text = 'KEY_POS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
key_pos_t_gep100.place(x=426, y=27)

status_t_gep100 = Label(frame_vru1, width = 7, text = 'STATUS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
status_t_gep100.place(x=426, y=49)

sw_pos_gep100 = Label(frame_vru1, width = 7, text = 'ВРУ', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
sw_pos_gep100.place(x=485, y=5)

key_pos_gep100 = Label(frame_vru1, width = 7, text = 'АВТО', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
key_pos_gep100.place(x=485, y=27)

status_gep100 = Label(frame_vru1, width = 7, text = 'НОРМА', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
status_gep100.place(x=485, y=49)

# создаем надписи параметров GEP_100
ua_t_gep100 = Label(frame_vru1, width = 5, text = 'Ua, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
ua_t_gep100.place(x=320, y=5)

ub_t_gep100 = Label(frame_vru1, width = 5, text = 'Ub, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
ub_t_gep100.place(x=320, y=27)

uc_t_gep100 = Label(frame_vru1, width = 5, text = 'Uc, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
uc_t_gep100.place(x=320, y=49)

f_t_gep100 = Label(frame_vru1, width = 5, text = 'F, Hz', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
f_t_gep100.place(x=320, y=71)

ua_gep100 = Label(frame_vru1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ua_gep100.place(x=365, y=5)

ub_gep100 = Label(frame_vru1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ub_gep100.place(x=365, y=27)

uc_gep100 = Label(frame_vru1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
uc_gep100.place(x=365, y=49)

f_gep100 = Label(frame_vru1, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
f_gep100.place(x=365, y=71)

# создаем надписи параметров ВРУ_1
ua_t_vru1 = Label(frame_vru1, width = 5, text = 'Ua, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
ua_t_vru1.place(x=320, y=102)

ub_t_vru1 = Label(frame_vru1, width = 5, text = 'Ub, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
ub_t_vru1.place(x=320, y=124)

uc_t_vru1 = Label(frame_vru1, width = 5, text = 'Uc, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
uc_t_vru1.place(x=320, y=146)

f_t_vru1 = Label(frame_vru1, width = 5, text = 'F, Hz', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
f_t_vru1.place(x=320, y=168)

ua_vru1 = Label(frame_vru1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ua_vru1.place(x=365, y=102)

ub_vru1 = Label(frame_vru1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ub_vru1.place(x=365, y=124)

uc_vru1 = Label(frame_vru1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
uc_vru1.place(x=365, y=146)

f_vru1 = Label(frame_vru1, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
f_vru1.place(x=365, y=168)

# создаем фрейм ВРУ_2 и GEP_110_2
frame_vru2 = Frame(frame_root, width = 550, height = 200, relief = GROOVE, borderwidth = 2)
frame_vru2.place(x = 110, y = 210)

# создаем картинку GEP_110_2
lb_gep110 = Label(frame_vru2, image = image_gep, relief = RIDGE, borderwidth = 2)
lb_gep110.place(x=5, y=5)

lb_t_gep110 = Label(frame_vru2, width = 9, text = 'GEP 110-2', font = "Arial 12 bold",
	bg = 'orange', relief = RIDGE, borderwidth = 2)
lb_t_gep110.place(x=57, y=153)

lb_s_gep110 = Label(frame_vru2, width = 12, text = 'ОСТАНОВЛЕН', font = "Arial 12 bold",
	bg = 'spring green', relief = RIDGE, borderwidth = 2)
lb_s_gep110.place(x=160, y=153)

# создаем надписи дополнительных параметров GEP_110_2
sw_pos_t_gep110 = Label(frame_vru2, width = 7, text = 'SW_POS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
sw_pos_t_gep110.place(x=426, y=5)

key_pos_t_gep110 = Label(frame_vru2, width = 7, text = 'KEY_POS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
key_pos_t_gep110.place(x=426, y=27)

sw_pos_gep110 = Label(frame_vru2, width = 7, text = 'ВРУ', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
sw_pos_gep110.place(x=485, y=5)

key_pos_gep110 = Label(frame_vru2, width = 7, text = 'АВТО', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
key_pos_gep110.place(x=485, y=27)

# создаем надписи параметров GEP_110
ua_t_gep110 = Label(frame_vru2, width = 5, text = 'Ua, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
ua_t_gep110.place(x=320, y=5)

ub_t_gep110 = Label(frame_vru2, width = 5, text = 'Ub, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
ub_t_gep110.place(x=320, y=27)

uc_t_gep110 = Label(frame_vru2, width = 5, text = 'Uc, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
uc_t_gep110.place(x=320, y=49)

f_t_gep110 = Label(frame_vru2, width = 5, text = 'F, Hz', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
f_t_gep110.place(x=320, y=71)

ua_gep110 = Label(frame_vru2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ua_gep110.place(x=365, y=5)

ub_gep110 = Label(frame_vru2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ub_gep110.place(x=365, y=27)

uc_gep110 = Label(frame_vru2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
uc_gep110.place(x=365, y=49)

f_gep110 = Label(frame_vru2, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
f_gep110.place(x=365, y=71)

# создаем надписи параметров ВРУ_2
ua_t_vru2 = Label(frame_vru2, width = 5, text = 'Ua, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
ua_t_vru2.place(x=320, y=102)

ub_t_vru2 = Label(frame_vru2, width = 5, text = 'Ub, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
ub_t_vru2.place(x=320, y=124)

uc_t_vru2 = Label(frame_vru2, width = 5, text = 'Uc, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
uc_t_vru2.place(x=320, y=146)

f_t_vru2 = Label(frame_vru2, width = 5, text = 'F, Hz', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
f_t_vru2.place(x=320, y=168)

ua_vru2 = Label(frame_vru2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ua_vru2.place(x=365, y=102)

ub_vru2 = Label(frame_vru2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ub_vru2.place(x=365, y=124)

uc_vru2 = Label(frame_vru2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
uc_vru2.place(x=365, y=146)

f_vru2 = Label(frame_vru2, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
f_vru2.place(x=365, y=168)

# создаем фрейм ВРУ_3 и GEP_33_3
frame_vru3 = Frame(frame_root, width = 550, height = 200,
	relief = GROOVE, borderwidth = 2)
frame_vru3.place(x = 110, y = 415)

# создаем картинку GEP_33_3
lb_gep33 = Label(frame_vru3, image = image_gep, relief = RIDGE,	borderwidth = 2)
lb_gep33.place(x=5, y=5)

lb_t_gep33 = Label(frame_vru3, width = 9, text = 'GEP 33-3', font = "Arial 12 bold",
	bg = 'orange', relief = RIDGE, borderwidth = 2)
lb_t_gep33.place(x=57, y=153)

lb_s_gep33 = Label(frame_vru3, width = 12, text = 'ОСТАНОВЛЕН', font = "Arial 12 bold",
	bg = 'spring green', relief = RIDGE, borderwidth = 2)
lb_s_gep33.place(x=160, y=153)

# создаем надписи дополнительных параметров GEP_33
sw_pos_t_gep33 = Label(frame_vru3, width = 7, text = 'SW_POS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
sw_pos_t_gep33.place(x=426, y=5)

key_pos_t_gep33 = Label(frame_vru3, width = 7, text = 'KEY_POS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
key_pos_t_gep33.place(x=426, y=27)

status_t_gep33 = Label(frame_vru3, width = 7, text = 'STATUS', relief = GROOVE,
	borderwidth = 2, bg = 'cadet blue')
status_t_gep33.place(x=426, y=49)

sw_pos_gep33 = Label(frame_vru3, width = 7, text = 'ВРУ', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
sw_pos_gep33.place(x=485, y=5)

key_pos_gep33 = Label(frame_vru3, width = 7, text = 'АВТО', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
key_pos_gep33.place(x=485, y=27)

status_gep33 = Label(frame_vru3, width = 7, text = 'НОРМА', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
status_gep33.place(x=485, y=49)

# создаем надписи параметров GEP_33
ua_t_gep33 = Label(frame_vru3, width = 5, text = 'Ua, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
ua_t_gep33.place(x=320, y=5)

ub_t_gep33 = Label(frame_vru3, width = 5, text = 'Ub, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
ub_t_gep33.place(x=320, y=27)

uc_t_gep33 = Label(frame_vru3, width = 5, text = 'Uc, V', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
uc_t_gep33.place(x=320, y=49)

f_t_gep33 = Label(frame_vru3, width = 5, text = 'F, Hz', relief = GROOVE,
	borderwidth = 2, bg = 'orange')
f_t_gep33.place(x=320, y=71)

ua_gep33 = Label(frame_vru3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ua_gep33.place(x=365, y=5)

ub_gep33 = Label(frame_vru3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ub_gep33.place(x=365, y=27)

uc_gep33 = Label(frame_vru3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
uc_gep33.place(x=365, y=49)

f_gep33 = Label(frame_vru3, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
f_gep33.place(x=365, y=71)

# создаем надписи параметров ВРУ_3
ua_t_vru3 = Label(frame_vru3, width = 5, text = 'Ua, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
ua_t_vru3.place(x=320, y=102)

ub_t_vru3 = Label(frame_vru3, width = 5, text = 'Ub, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
ub_t_vru3.place(x=320, y=124)

uc_t_vru3 = Label(frame_vru3, width = 5, text = 'Uc, V', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
uc_t_vru3.place(x=320, y=146)

f_t_vru3 = Label(frame_vru3, width = 5, text = 'F, Hz', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
f_t_vru3.place(x=320, y=168)

ua_vru3 = Label(frame_vru3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ua_vru3.place(x=365, y=102)

ub_vru3 = Label(frame_vru3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
ub_vru3.place(x=365, y=124)

uc_vru3 = Label(frame_vru3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
uc_vru3.place(x=365, y=146)

f_vru3 = Label(frame_vru3, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
f_vru3.place(x=365, y=168)

# создаем фрейм UPS_1
frame_ups1 = Frame(frame_root, width = 230, height = 200, relief = GROOVE, borderwidth = 2)
frame_ups1.place(x = 775, y = 5)

# создаем картинку UPS_1
lb_ups1 = Label(frame_ups1, image = image_ups, relief = RIDGE,	borderwidth = 2)
lb_ups1.place(x=5, y=5)

lb_t_ups1 = Label(frame_ups1, width = 5, text = 'UPS 1', font = "Arial 12 bold", bg = 'sky blue',
	relief = RIDGE, borderwidth = 2)
lb_t_ups1.place(x=23, y=150)

# создаем надписи параметров UPS_1
temp_t_ups1 = Label(frame_ups1, width = 10, text = 'Темп АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
temp_t_ups1.place(x=100, y=5)

level_t_ups1 = Label(frame_ups1, width = 10, text = 'Заряд АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
level_t_ups1.place(x=100, y=27)

low_t_ups1 = Label(frame_ups1, width = 10, text = 'Низкий АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
low_t_ups1.place(x=100, y=107)

alarm_t_ups1 = Label(frame_ups1, width = 10, text = 'Авария', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
alarm_t_ups1.place(x=100, y=129)

battary_t_ups1 = Label(frame_ups1, width = 10, text = 'От АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
battary_t_ups1.place(x=100, y=151)

overload_t_ups1 = Label(frame_ups1, width = 10, text = 'Перегруз', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
overload_t_ups1.place(x=100, y=173)

temp_ups1 = Label(frame_ups1, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
temp_ups1.place(x=180, y=5)

level_ups1 = Label(frame_ups1, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
level_ups1.place(x=180, y=27)

low_ups1 = Label(frame_ups1, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
low_ups1.place(x=180, y=107)

alarm_ups1 = Label(frame_ups1, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
alarm_ups1.place(x=180, y=129)

battary_ups1 = Label(frame_ups1, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
battary_ups1.place(x=180, y=151)

overload_ups1 = Label(frame_ups1, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
overload_ups1.place(x=180, y=173)

# создаем фрейм UPS_2
frame_ups2 = Frame(frame_root, width = 230, height = 200, relief = GROOVE, borderwidth = 2)
frame_ups2.place(x = 775, y = 210)

# создаем картинку UPS_2
lb_ups2 = Label(frame_ups2, image = image_ups, relief = RIDGE, borderwidth = 2)
lb_ups2.place(x=5, y=5)

lb_t_ups2 = Label(frame_ups2, width = 5, text = 'UPS 2', font = "Arial 12 bold", bg = 'sky blue',
	relief = RIDGE, borderwidth = 2)
lb_t_ups2.place(x=23, y=150)

# создаем надписи параметров UPS_2
temp_t_ups2 = Label(frame_ups2, width = 10, text = 'Темп АКБ', relief = GROOVE, borderwidth = 2,
	bg = 'sky blue')
temp_t_ups2.place(x=100, y=5)

level_t_ups2 = Label(frame_ups2, width = 10, text = 'Заряд АКБ', relief = GROOVE, borderwidth = 2,
	bg = 'sky blue')
level_t_ups2.place(x=100, y=27)

low_t_ups2 = Label(frame_ups2, width = 10, text = 'Низкий АКБ', relief = GROOVE, borderwidth = 2,
	bg = 'sky blue')
low_t_ups2.place(x=100, y=107)

alarm_t_ups2 = Label(frame_ups2, width = 10, text = 'Авария', relief = GROOVE, borderwidth = 2,
	bg = 'sky blue')
alarm_t_ups2.place(x=100, y=129)

battary_t_ups2 = Label(frame_ups2, width = 10, text = 'От АКБ', relief = GROOVE, borderwidth = 2,
	bg = 'sky blue')
battary_t_ups2.place(x=100, y=151)

overload_t_ups2 = Label(frame_ups2, width = 10, text = 'Перегруз', relief = GROOVE, borderwidth = 2,
	bg = 'sky blue')
overload_t_ups2.place(x=100, y=173)

temp_ups2 = Label(frame_ups2, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
temp_ups2.place(x=180, y=5)

level_ups2 = Label(frame_ups2, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
level_ups2.place(x=180, y=27)

low_ups2 = Label(frame_ups2, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
low_ups2.place(x=180, y=107)

alarm_ups2 = Label(frame_ups2, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
alarm_ups2.place(x=180, y=129)

battary_ups2 = Label(frame_ups2, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
battary_ups2.place(x=180, y=151)

overload_ups2= Label(frame_ups2, width = 5, text = 'OK', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
overload_ups2.place(x=180, y=173)

# создаем фрейм UPS_3
frame_ups3 = Frame(frame_root, width = 230, height = 100, relief = GROOVE, borderwidth = 2)
frame_ups3.place(x = 775, y = 415)

# создаем картинку UPS_3
lb_ups3 = Label(frame_ups3, image = image_ups_srt, relief = RIDGE, borderwidth = 2)
lb_ups3.place(x=5, y=5)

lb_t_ups3 = Label(frame_ups3, width = 5, text = 'UPS 3', font = "Arial 12 bold", bg = 'sky blue',
	relief = RIDGE, borderwidth = 2)
lb_t_ups3.place(x=23, y=55)

# создаем надписи параметров UPS_3
temp_t_ups3 = Label(frame_ups3, width = 10, text = 'Темп АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
temp_t_ups3.place(x=100, y=5)

level_t_ups3 = Label(frame_ups3, width = 10, text = 'Заряд АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
level_t_ups3.place(x=100, y=27)

low_t_ups3 = Label(frame_ups3, width = 10, text = 'ВХ. НАПР.', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
low_t_ups3.place(x=100, y=49)

alarm_t_ups3 = Label(frame_ups3, width = 10, text = 'ВЫХ. НАПР', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
alarm_t_ups3.place(x=100, y=71)

temp_ups3 = Label(frame_ups3, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
temp_ups3.place(x=180, y=5)

level_ups3 = Label(frame_ups3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
level_ups3.place(x=180, y=27)

low_ups3 = Label(frame_ups3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
low_ups3.place(x=180, y=49)

alarm_ups3 = Label(frame_ups3, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
alarm_ups3.place(x=180, y=71)

# создаем фрейм UPS_4
frame_ups4 = Frame(frame_root, width = 230, height = 100,
	relief = GROOVE, borderwidth = 2)
frame_ups4.place(x = 775, y = 515)

# создаем картинку UPS_4
lb_ups4 = Label(frame_ups4, image = image_ups_srt, relief = RIDGE, borderwidth = 2)
lb_ups4.place(x=5, y=5)

lb_t_ups4 = Label(frame_ups4, width = 5, text = 'UPS 4', font = "Arial 12 bold", bg = 'sky blue',
	relief = RIDGE, borderwidth = 2)
lb_t_ups4.place(x=23, y=55)

# создаем надписи параметров UPS_4
temp_t_ups4 = Label(frame_ups4, width = 10, text = 'Темп АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
temp_t_ups4.place(x=100, y=5)

level_t_ups4 = Label(frame_ups4, width = 10, text = 'Заряд АКБ', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
level_t_ups4.place(x=100, y=27)

low_t_ups4 = Label(frame_ups4, width = 10, text = 'ВХ. НАПР.', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
low_t_ups4.place(x=100, y=49)

alarm_t_ups4 = Label(frame_ups4, width = 10, text = 'ВЫХ. НАПР', relief = GROOVE,
	borderwidth = 2, bg = 'sky blue')
alarm_t_ups4.place(x=100, y=71)

temp_ups4 = Label(frame_ups4, width = 5, text = '00.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
temp_ups4.place(x=180, y=5)

level_ups4 = Label(frame_ups4, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
level_ups4.place(x=180, y=27)

low_ups4 = Label(frame_ups4, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
low_ups4.place(x=180, y=49)

alarm_ups4 = Label(frame_ups4, width = 5, text = '000.0', relief = GROOVE,
	borderwidth = 2, bg = 'spring green')
alarm_ups4.place(x=180, y=71)

# создаем левый фрейм с часами и кнопками
frame_bt = Frame(frame_root, width = 100, height = 745,
	relief = GROOVE, borderwidth = 2)
frame_bt.place(x = 5, y = 5)

# создаем фрейм с часами и городом
frame_lb_t = tk.Frame(frame_bt, width = 90,
	height = 60, relief = GROOVE, borderwidth = 2)
frame_lb_t.place(x=3, y=3)

lb_time = Label(frame_lb_t, width = 8, text = "00:00:00", font = "Arial 13 bold")
lb_time.place(x=0, y=10)

lb_city = Label(frame_bt, width = 8, text = "ИРКУТСК", font = "Arial 10",
	relief = GROOVE, borderwidth = 2)
lb_city.place(x=13, y=50)

# создаем лампочку общей сигнализации
image_alarm_red = PhotoImage(file = 'image/red.png')
image_alarm_red = image_alarm_red.subsample(10, 10)

image_alarm_green = PhotoImage(file = 'image/green.png')
image_alarm_green = image_alarm_green.subsample(10, 10)

lb_alarm = Label(frame_bt, image = image_alarm_green)
lb_alarm.place(x=20, y=90)

# создаем чекбаттон звук
ch_sound = Checkbutton(frame_bt, text = 'ЗВУК', variable = flag_alarm, onvalue = 1,
	offvalue = 0)
ch_sound.place(x=5, y=150)

# создаем кнопку инфо
bt_about = Button(frame_bt, width = 10, text = 'Инфо', command = window_about)
bt_about.place(x = 7, y =200)

# создаем кнопку журнал
bt_event = Button(frame_bt, width = 10, text = 'Журнал', command = window_event)
bt_event.place(x = 7, y =235)

# создаем кнопку выход
bt_exit = Button(frame_bt, width = 10, text = 'Выход', command = root.destroy)
bt_exit.place(x = 7, y =270)

# создаем визуализацию COM_test
frame_com0 = tk.Frame(frame_bt, width = 90,	height = 65,
	relief = GROOVE, borderwidth = 2)
frame_com0.place(x=3, y=408)

tx_com0 = Label(frame_com0, width = 3, text = 'Tx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2, bg = 'gray99')
tx_com0.place(x=62, y=5)

rx_com0 = Label(frame_com0, width = 3, text = 'Rx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2, bg = 'gray99')
rx_com0.place(x=62, y=22)

name_com0 = Label(frame_com0, width = 12, text = str(com0_name), font = "Arial 8", relief = GROOVE,
	borderwidth = 2)
name_com0.place(x=5, y=39)

br_com0 = Label(frame_com0, width =10, text = str(com0_baudrate) + ', ' + str(com0_bytesize) +
	', ' + str(com0_parity) + ', ' + str(com0_stopbits), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
br_com0.place(x=5, y=5)

id_com0 = Label(frame_com0, width =10, text = str(com0_id), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
id_com0.place(x=5, y=22)

# создаем визуализацию COM_gep100
frame_com1 = tk.Frame(frame_bt, width = 90,	height = 65,
	relief = GROOVE, borderwidth = 2)
frame_com1.place(x=3, y=475)

tx_com1 = Label(frame_com1, width = 3, text = 'Tx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2)
tx_com1.place(x=62, y=5)

rx_com1 = Label(frame_com1, width = 3, text = 'Rx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2)
rx_com1.place(x=62, y=22)

name_com1 = Label(frame_com1, width = 12, text = str(com1_name), font = "Arial 8", relief = GROOVE,
	borderwidth = 2)
name_com1.place(x=5, y=39)

br_com1 = Label(frame_com1, width =10, text = str(com1_baudrate) + ', ' + str(com1_bytesize) +
	', ' + str(com1_parity) + ', ' + str(com1_stopbits), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
br_com1.place(x=5, y=5)

id_com1 = Label(frame_com1, width =10, text = str(com1_id), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
id_com1.place(x=5, y=22)

# создаем визуализацию COM_gep110
frame_com2 = tk.Frame(frame_bt, width = 90,	height = 65,
	relief = GROOVE, borderwidth = 2)
frame_com2.place(x=3, y=542)

tx_com2 = Label(frame_com2, width = 3, text = 'Tx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2)
tx_com2.place(x=62, y=5)

rx_com2 = Label(frame_com2, width = 3, text = 'Rx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2)
rx_com2.place(x=62, y=22)

name_com2 = Label(frame_com2, width = 12, text = str(com2_name), font = "Arial 8", relief = GROOVE,
	borderwidth = 2)
name_com2.place(x=5, y=39)

br_com2 = Label(frame_com2, width =10, text = str(com2_baudrate) + ', ' + str(com2_bytesize) +
	', ' + str(com2_parity) + ', ' + str(com2_stopbits), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
br_com2.place(x=5, y=5)

id_com2 = Label(frame_com2, width =10, text = str(com2_id), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
id_com2.place(x=5, y=22)

# создаем визуализацию COM_gep33
frame_com3 = tk.Frame(frame_bt, width = 90,	height = 65,
	relief = GROOVE, borderwidth = 2)
frame_com3.place(x=3, y=542)

tx_com3 = Label(frame_com3, width = 3, text = 'Tx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2)
tx_com3.place(x=62, y=5)

rx_com3 = Label(frame_com3, width = 3, text = 'Rx', font = "Arial 6", relief = GROOVE,
	borderwidth = 2)
rx_com3.place(x=62, y=22)

name_com3 = Label(frame_com3, width = 12, text = str(com3_name), font = "Arial 8", relief = GROOVE,
	borderwidth = 2)
name_com3.place(x=5, y=39)

br_com3 = Label(frame_com3, width =10, text = str(com3_baudrate) + ', ' + str(com3_bytesize) +
	', ' + str(com3_parity) + ', ' + str(com3_stopbits), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
br_com3.place(x=5, y=5)

id_com3 = Label(frame_com3, width =10, text = str(com3_id), font = "Arial 6", relief = GROOVE,	borderwidth = 2)
id_com3.place(x=5, y=22)

g_time()
g_test()

root.mainloop()
com0.close()
