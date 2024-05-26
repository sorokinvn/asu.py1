#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as sq
import datetime
import pygame
import sqlite3
import struct
import serial
import tkinter as tk
from tkinter import*
from tkinter import ttk
from modbus_crc16 import crc16
import time
from threading import Thread

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
		self.com_0.timeout = 0.300
	
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
		crc_hi, crc_lo = crc16(send)
		send.append(crc_hi)
		send.append(crc_lo)
		pack_style = str(len(send)) + 'B'
		send = struct.pack(pack_style, *send)
		self.com_0.write(send)
		get = self.com_0.read(8)
		unpack_style = str(len(get)) + 'B'
		get = struct.unpack(unpack_style, get)
		get = get_analog_com(get)
		return get


# объявляем класс COMID
class Comid():
	def __init__(self, com, baudrate):
		self.comm = com
		self.baudrate = baudrate
	
	def creat(self):
		pass


# объявляем класс UPS
class Ups():
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
		self.temp_min = 15
		self.temp_max = 25
		self.level_min = 30
		self.level_mean = 50
		self.u_min = 207
		self.u_max = 253

	def creat(self):

		# создаем фрейм ups
		self.frame_ups = Frame(frame_root, width = 220, height = 200, relief = GROOVE,
			borderwidth = 2)
		self.frame_ups.place(x = self.x, y = self.y)

		# рисуем картинку ups
		lb_image_ups = Label(self.frame_ups, image = image_ups, relief = RIDGE, borderwidth = 2)
		lb_image_ups.place(x=5, y=5)

		# рисуем имя ups
		lb_name_ups = Label(self.frame_ups, width = 6, text = self.name, font = "Arial 12 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_name_ups.place(x=19, y=153)

		# рисуем поля параметров ups
		lb_temp_ups = Label(self.frame_ups, text = 'ТЕМП, C', width = 8, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_temp_ups.place(x=100, y=5)

		self.lb_temp_ups_value = Label(self.frame_ups, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_temp_ups_value.place(x=170, y=5)

		lb_level_ups = Label(self.frame_ups, text = 'ЗАРЯД, %', width = 8, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_level_ups.place(x=100, y=27)

		self.lb_level_ups_value = Label(self.frame_ups, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_level_ups_value.place(x=170, y=27)

		lb_involt_ups = Label(self.frame_ups, text = 'ВХОД, В', width = 8, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_involt_ups.place(x=100, y=49)

		self.lb_involt_ups_value = Label(self.frame_ups, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_involt_ups_value.place(x=170, y=49)

		lb_outvolt_ups = Label(self.frame_ups, text = 'ВЫХОД, В', width = 8, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_outvolt_ups.place(x=100, y=71)

		self.lb_outvolt_ups_value = Label(self.frame_ups, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_outvolt_ups_value.place(x=170, y=71)

	# задаем значение температуры
	def set_temp(self, value):
		self.value = value
		self.lb_temp_ups_value.config(text = self.value)
		if self.value <= self.temp_min or self.value >= self.temp_max:
			self.lb_temp_ups_value.config(bg = 'red')
		else:
			self.lb_temp_ups_value.config(bg = 'spring green')

	def set_level(self, value):
		self.value = value
		self.lb_level_ups_value.config(text = self.value)
		if self.value <= self.level_mean and self.value >= self.level_min:
			self.lb_level_ups_value.config(bg = 'gold')
		if self.value < self.level_min:
			self.lb_level_ups_value.config(bg = 'red')
		if self.value > self.level_mean:
			self.lb_level_ups_value.config(bg = 'spring green')

	def set_involtage(self, value):
		self.value = value
		self.lb_involt_ups_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_involt_ups_value.config(bg = 'red')
		else:
			self.lb_involt_ups_value.config(bg = 'spring green')

	def set_outvoltage(self, value):
		self.value = value
		self.lb_outvolt_ups_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_outvolt_ups_value.config(bg = 'red')
		else:
			self.lb_outvolt_ups_value.config(bg = 'spring green')


# объявляем класс GEP
class Gep():
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
		self.u_min = 207
		self.u_max = 253
		self.f_min = 49.6
		self.f_max = 50.4

	def creat(self):
		
		# создаем фрейм gep
		self.frame_gep = Frame(frame_root, width = 540, height = 200, relief = GROOVE,
			borderwidth = 2)
		self.frame_gep.place(x = self.x, y = self.y)
		
		# рисуем картинку gep
		lb_image_gep = Label(self.frame_gep, image = image_gep, relief = RIDGE, borderwidth = 2)
		lb_image_gep.place(x=5, y=5)
		
		# рисуем имя gep
		lb_name_gep = Label(self.frame_gep, width = 9, text = self.name, font = "Arial 12 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_name_gep.place(x=57, y=153)
		
		# рисуем поле статуса gep
		self.lb_status_gep = Label(self.frame_gep, width = 12, font = "Arial 12 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_status_gep.place(x=160, y=153)

		# рисуем поля параметров gep
		lb_gep = Label(self.frame_gep, text = 'СЕТЬ ДЭС', width = 12, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		lb_gep.place(x=320, y=5)

		lb_ua_gep = Label(self.frame_gep, text = 'Ua, В', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_ua_gep.place(x=320, y=27)

		self.lb_ua_gep_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_ua_gep_value.place(x=369, y=27)
		
		lb_ub_gep = Label(self.frame_gep, text = 'Ub, В', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_ub_gep.place(x=320, y=49)

		self.lb_ub_gep_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_ub_gep_value.place(x=369, y=49)
		
		lb_uc_gep = Label(self.frame_gep, text = 'Uc, В', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_uc_gep.place(x=320, y=71)

		self.lb_uc_gep_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_uc_gep_value.place(x=369, y=71)
		
		lb_f_gep = Label(self.frame_gep, text = 'F, Гц', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_f_gep.place(x=320, y=93)

		self.lb_f_gep_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_f_gep_value.place(x=369, y=93)

		lb_sw_gep = Label(self.frame_gep, text = 'ПОЛОЖЕНИЕ ATyS', width = 15, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		lb_sw_gep.place(x=320, y=146)

		self.lb_sw_gep_value = Label(self.frame_gep, width = 12, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_sw_gep_value.place(x=440, y=146)

		lb_key_gep = Label(self.frame_gep, text = 'РЕЖИМ ATyS', width = 15, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		lb_key_gep.place(x=320, y=168)

		self.lb_key_gep_value = Label(self.frame_gep, width = 12, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_key_gep_value.place(x=440, y=168)

		# рисуем поля параметров вру
		lb_vru = Label(self.frame_gep, text = 'СЕТЬ ВРУ', width = 12, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		lb_vru.place(x=440, y=5)

		lb_ua_vru = Label(self.frame_gep, text = 'Ua, В', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_ua_vru.place(x=440, y=27)

		self.lb_ua_vru_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_ua_vru_value.place(x=489, y=27)

		lb_ub_vru = Label(self.frame_gep, text = 'Ub, В', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_ub_vru.place(x=440, y=49)

		self.lb_ub_vru_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_ub_vru_value.place(x=489, y=49)
		
		lb_uc_vru = Label(self.frame_gep, text = 'Uc, В', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_uc_vru.place(x=440, y=71)

		self.lb_uc_vru_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_uc_vru_value.place(x=489, y=71)
		
		lb_f_vru = Label(self.frame_gep, text = 'F, Гц', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_f_vru.place(x=440, y=93)

		self.lb_f_vru_value = Label(self.frame_gep, width = 5, font = "Arial 8 bold",
			relief = RIDGE, borderwidth = 2)
		self.lb_f_vru_value.place(x=489, y=93)
		

	# задаем статус gep
	def set_status(self, status):
		self.status = status
		if self.status == 0:
			self.lb_status_gep.config(text = 'ОСТАНОВЛЕН', bg = 'gray99')
		if self.status == 1:
			self.lb_status_gep.config(text = 'РАБОТАЕТ', bg = 'spring green')

	# задаем значение ua gep
	def set_ua_gep(self, value):
		self.value = value
		self.lb_ua_gep_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_ua_gep_value.config(bg = 'red')
		else:
			self.lb_ua_gep_value.config(bg = 'spring green')
		
	# задаем значение ub gep
	def set_ub_gep(self, value):
		self.value = value
		self.lb_ub_gep_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_ub_gep_value.config(bg = 'red')
		else:
			self.lb_ub_gep_value.config(bg = 'spring green')
		
	# задаем значение uc gep
	def set_uc_gep(self, value):
		self.value = value
		self.lb_uc_gep_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_uc_gep_value.config(bg = 'red')
		else:
			self.lb_uc_gep_value.config(bg = 'spring green')

	# задаем значение f gep
	def set_f_gep(self, value):
		self.value = value
		self.lb_f_gep_value.config(text = self.value)
		if self.value <= self.f_min or self.value >= self.f_max:
			self.lb_f_gep_value.config(bg = 'red')
		else:
			self.lb_f_gep_value.config(bg = 'spring green')

	# задаем положение ati
	def set_sw_pos(self, value):
		self.value = value
		if self.value == 2 or self.value == 9:
			self.lb_sw_gep_value.config(text = 'ВРУ')
		if self.value == 1 or self.value == 10:
			self.lb_sw_gep_value.config(text = '0')
		if self.value == 3 or self.value == 36:
			self.lb_sw_gep_value.config(text = 'ДЭС')

	# задаем режим ati
	def set_key_pos(self, value, gep_type):
		self.value = value
		self.gep_type = gep_type
		if self.gep_type == 110:
			if self.value == 0:
				self.lb_key_gep_value.config(text = 'АВТО', bg = 'spring green')
			if self.value == 4:
				self.lb_key_gep_value.config(text = 'РУЧНОЙ', bg = 'coral')
		if self.gep_type == 100 or self.gep_type == 33:
			if self.value == 0:
				self.lb_key_gep_value.config(text = 'РУЧНОЙ', bg = 'coral')
			if self.value == 16:
				self.lb_key_gep_value.config(text = 'АВТО', bg = 'spring green')
			if self.value == 32:
				self.lb_key_gep_value.config(text = 'ПРОВЕРКА', bg = 'coral')
			if self.value == 64:
				self.lb_key_gep_value.config(text = 'ЗАПРЕТ', bg = 'coral')

	# задаем значение ua вру
	def set_ua_vru(self, value):
		self.value = value
		self.lb_ua_vru_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_ua_vru_value.config(bg = 'red')
		else:
			self.lb_ua_vru_value.config(bg = 'spring green')

	def set_ub_vru(self, value):
		self.value = value
		self.lb_ub_vru_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_ub_vru_value.config(bg = 'red')
		else:
			self.lb_ub_vru_value.config(bg = 'spring green')
	
	def set_uc_vru(self, value):
		self.value = value
		self.lb_uc_vru_value.config(text = self.value)
		if self.value <= self.u_min or self.value >= self.u_max:
			self.lb_uc_vru_value.config(bg = 'red')
		else:
			self.lb_uc_vru_value.config(bg = 'spring green')

	def set_f_vru(self, value):
		self.value = value
		self.lb_f_vru_value.config(text = self.value)
		if self.value <= self.f_min or self.value >= self.f_max:
			self.lb_f_vru_value.config(bg = 'red')
		else:
			self.lb_f_vru_value.config(bg = 'spring green')

# функция создания окна Описание
def window_about():
	w_about = tk.Toplevel()
	w_about.grab_set()
	w_about.iconbitmap('image/icon.ico')
	w_about.title('О программе')
	w_about.geometry('400x220')
	w_about.resizable(0, 0)	
	frame_about = Frame(w_about, width = 390, height = 210,
	relief = GROOVE, borderwidth = 2)
	frame_about.place(x = 5, y = 5)
	about_text = Text(frame_about, width = 45, height = 8, font = "Arial 11",
		bg = 'gray95', relief = GROOVE, borderwidth = 2)
	about_text.insert(INSERT, "Программа автоматизированного мониторинга\
		\nсистемы электроснабжения объекта КСА УВД\
		\nРГЦ ЕС ОрВД (Иркутск)\
		\n\
		\nПрограмма разаботана инженерно-техническим\
		\nперсоналом службы ЭРТОС\
		\n\
		\nversion: v.01     Иркутск 2021 г.")
	about_text.configure(state = 'disabled')
	about_text.place(x=10, y=10)
	about_exit = Button(frame_about, width = 10, text = 'OK', font = "Arial 8 bold",
		command = w_about.destroy)
	about_exit.place(x = 295, y = 175)
	w_about.mainloop()

def window_event():
	def wr_msg():
		tree.insert('', 'end', value = ('4', datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'Ua', '265'))

	w_event = tk.Toplevel()
	w_event.grab_set()
	w_event.iconbitmap('image/icon.ico')
	w_event.title('Журнал событий')
	w_event.geometry('500x400')
	w_event.resizable(0, 0)	
	frame_event = Frame(w_event, width = 490, height = 390,
	relief = GROOVE, borderwidth = 2)
	frame_event.place(x = 5, y = 5)
	bt_exit = Button(frame_event, width = 10, text = 'OK', font = "Arial 8 bold",
		command = w_event.destroy)
	bt_exit.place(x = 395, y = 350)

	# создаем таблюцу журнала событий
	tree = ttk.Treeview(frame_event, columns = ('id', 'time', 'name', 'val'),
		height = 15, show = 'headings')

	tree.heading('#1', text = 'idd', anchor = CENTER)
	tree.heading('#2', text = 'ВРЕМЯ', anchor = CENTER)
	tree.heading('#3', text = 'ПАРАМЕТР', anchor = CENTER)
	tree.heading('#4', text = 'ЗНАЧЕНИЕ', anchor = CENTER)

	tree.column('#1', width = 50, anchor = CENTER)
	tree.column('#2', width = 172, anchor = CENTER)
	tree.column('#3', width = 150, anchor = CENTER)
	tree.column('#4', width = 100, anchor = CENTER)

	tree.place(x = 5, y = 5)

	tree.insert('', 'end', value = ('0', '1', '2', '3'))

	tree.insert('', 'end', value = ('10', '231', '42', '33'))

	bt_test = Button(frame_event, width = 10, text = 'write', font = "Arial 8 bold",
		command = wr_msg)
	bt_test.place(x = 200, y = 350)

	w_event.mainloop()

# проверяем флаг-аларм и в случае если True выдаем аварию
def get_test():
	tmp = flag_alarm.get()
	if tmp == 1:
		lb_alarm_lamp.configure(image = image_red_light)
		pygame.mixer.music.play(-1)
	else:
		lb_alarm_lamp.configure(image = image_green_light)
		pygame.mixer.music.stop()
	root.after(500, lambda: get_test())

# функция отрисовки текущего времени
def get_time():
	lb_time.config(text = datetime.datetime.now().strftime('%d-%m-%Y\n%H:%M:%S'))
	root.after(500, lambda: get_time())

def read_value_1():
	gep_100.set_ua_gep(serial_port.get_analog_4(3, 13))
	gep_100.set_ub_gep(serial_port.get_analog_4(3, 14))
	gep_100.set_uc_gep(serial_port.get_analog_4(3, 34))
	

	root.after(500, lambda: read_value_1())


# создаем главное окно программы
root = tk.Tk()
root.iconbitmap('image/icon.ico')
root.title('АСУ ДЭС РГЦ ЕС ОрВД Иркутск')
root.geometry('1200x850')
root.resizable(0, 0)

# инициализируем микшер и подгружаем звук аларма
pygame.mixer.init()
sound_alarm = pygame.mixer.music.load('sound/alarm.wav')

# объявляем глобальный флаг-аларм
global flag_alarm
flag_alarm = tk.BooleanVar()

# загружаем картинку GEP
image_gep = PhotoImage(file = 'image/gep.png')

# загружаем картинку UPS
image_ups = PhotoImage(file = 'image/ups.png')
image_ups = image_ups.subsample(2, 2)

# загружаем зеленую картинку сигнальной лампы
image_green_light = PhotoImage(file = 'image/green_light.png')
image_green_light = image_green_light.subsample(2, 2)

# загружаем красную картинку сигнальной лампы
image_red_light = PhotoImage(file = 'image/red_light.png')
image_red_light = image_red_light.subsample(2, 2)

# подключаемся к базе
con = sq.connect("temp.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS voltage")
cur.execute("""CREATE TABLE IF NOT EXISTS voltage (
	idd INTEGER PRIMARY KEY,
	tim TEXT,
	name TEXT,
	val REAL
	)""")

cur.execute("""INSERT INTO voltage VALUES(?, ?, ?, ?)""",
	('50',	datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'Ua', 27))
con.commit()

# создаем правый фрейм с часами и кнопками
frame_clock_button = Frame(root, width = 170, height = 840, relief = GROOVE, borderwidth = 2)
frame_clock_button.place(x = 1025, y = 5)

# создаем часы
frame_clock = Frame(frame_clock_button, width = 150, height = 67, relief = GROOVE, borderwidth = 2)
frame_clock.place(x = 8, y = 15)
lb_city = Label(frame_clock_button, text = 'ИРКУТСК', width = 10, font = "Arial 8 bold",
	relief = RIDGE, borderwidth = 2)
lb_city.place(x = 45, y = 5)
lb_time = Label(frame_clock, width = 15, font = "Courier 10 bold",
	relief = RIDGE, borderwidth = 2)
lb_time.place(x = 9, y = 15)

# создаем кнопку Описание
bt_about = Button(frame_clock_button, text = 'ОПИСАНИЕ', width = 10, font = "Arial 8 bold",
	command = window_about)
bt_about.place(x = 40, y = 100)

# создаем кнопку Журнал
bt_event = Button(frame_clock_button, text = 'ЖУРНАЛ', width = 10, font = "Arial 8 bold",
	command = window_event)
bt_event.place(x = 40, y = 130)

# создаем кнопку ВЫХОД
bt_exit = Button(frame_clock_button, text = 'ВЫХОД', width = 10, font = "Arial 8 bold",
	command = root.destroy)
bt_exit.place(x = 40, y = 160)

# создаем аларм-фрейм
frame_alarm = Frame(frame_clock_button, width = 150, height = 80, relief = GROOVE, borderwidth = 2)
frame_alarm.place(x = 8, y = 750)
lb_alarm_lamp = Label(frame_alarm, image = image_green_light)
lb_alarm_lamp.place(x=70, y=5)
ch_sound = Checkbutton(frame_alarm, text = 'ЗВУК', font = "Arial 10 bold",
	variable = flag_alarm, onvalue = 1,	offvalue = 0)
ch_sound.place(x=5, y=25)

# запускаем функцию отрисовки текущего времени
#get_time()

# запускаем функцию проверки текущего значения флага-аларм
#get_test()

# создаем фрейм главного окна
frame_root = Frame(root, width = 1014, height = 840, relief = GROOVE, borderwidth = 2)
frame_root.place(x = 5, y = 5)


serial_port = Comport('com2', 9600)
serial_port.up()

gep_100 = Gep(name = 'GEP 100', x = 5, y = 5)
gep_100.creat()


gep_110 = Gep(name = 'GEP 110', x = 5, y = 210)
gep_110.creat()


gep_33 = Gep(name = 'GEP 33', x = 5, y = 415)
gep_33.creat()

thread_1 = Thread(target = read_value_1)
thread_2 = Thread(target = get_test)
thread_3 = Thread(target = get_time)

thread_1.start()
thread_2.start()
thread_3.start()


ups_1 = Ups(name = 'UPS 1', x = 560, y = 5)
ups_1.creat()
ups_1.set_level(90)
ups_1.set_temp(20)
ups_1.set_involtage(273)
ups_1.set_outvoltage(220.8)

ups_2 = Ups(name = 'UPS 2', x = 785, y = 5)
ups_2.creat()


ups_3 = Ups(name = 'UPS 3', x = 560, y = 210)
ups_3.creat()


ups_4 = Ups(name = 'UPS 4', x = 785, y = 210)
ups_4.creat()


root.mainloop()
con.close()
serial_port.down()

