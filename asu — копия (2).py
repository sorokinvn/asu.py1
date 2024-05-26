#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import*

class Field():
	def __init__(self, name, x, y, text):
		self.name = neme
		self.x = x
		self.y = y
		self.text = text

	def creat(self):

		lb = Label(frame_gep, text = self.text, width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_ua_gep.place(x = self.x, y = self.y)
		self.lb = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb.place(x = (self.x + 45), y = self.y)



class Gep():
	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y
	
	def creat(self):
		
		# создаем фрейм gep
		frame_gep = Frame(frame_root, width = 550, height = 200, relief = GROOVE, borderwidth = 2)
		frame_gep.place(x = self.x, y = self.y)
		
		# рисуем картинку gep
		lb_image_gep = Label(frame_gep, image = image_gep, relief = RIDGE, borderwidth = 2)
		lb_image_gep.place(x=5, y=5)
		
		# рисуем имя gep
		lb_name_gep = Label(frame_gep, width = 9, text = self.name, font = "Arial 12 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_name_gep.place(x=57, y=153)
		
		# рисуем поле статуса gep
		self.lb_status_gep = Label(frame_gep, width = 12, font = "Arial 12 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_status_gep.place(x=160, y=153)
		
		# рисуем поля параметров gep
		lb_ua_gep = Label(frame_gep, text = 'Ua, В', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_ua_gep.place(x=320, y=5)
		self.lb_ua_gep = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_ua_gep.place(x=365, y=5)

		lb_ub_gep = Label(frame_gep, text = 'Ub, В', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_ub_gep.place(x=320, y=27)
		self.lb_ub_gep = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_ub_gep.place(x=365, y=27)

		lb_uc_gep = Label(frame_gep, text = 'Uc, В', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_uc_gep.place(x=320, y=49)
		self.lb_uc_gep = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_uc_gep.place(x=365, y=49)

		lb_f_gep = Label(frame_gep, text = 'F, Гц', width = 5, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_f_gep.place(x=320, y=71)
		self.lb_f_gep = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_f_gep.place(x=365, y=71)

		lb_mode_gep = Label(frame_gep, text = 'РЕЖИМ', width = 10, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_mode_gep.place(x=320, y=144)
		self.lb_mode_gep = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_mode_gep.place(x=400, y=144)

		lb_pos_gep = Label(frame_gep, text = 'ПОЛОЖ', width = 10, font = "Arial 8 bold",
			bg = 'orange', relief = RIDGE, borderwidth = 2)
		lb_pos_gep.place(x=320, y=168)
		self.lb_pos_gep = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_pos_gep.place(x=400, y=168)

		# рисуем поля параметров вру
		lb_ua_vru = Label(frame_gep, text = 'Ua, В', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_ua_vru.place(x=450, y=5)
		self.lb_ua_vru = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_ua_vru.place(x=495, y=5)

		lb_ub_vru = Label(frame_gep, text = 'Ub, В', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_ub_vru.place(x=450, y=27)
		self.lb_ub_vru = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_ub_vru.place(x=495, y=27)

		lb_uc_vru = Label(frame_gep, text = 'Uc, В', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_uc_vru.place(x=450, y=49)
		self.lb_uc_vru = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_uc_vru.place(x=495, y=49)

		lb_f_vru = Label(frame_gep, text = 'F, Гц', width = 5, font = "Arial 8 bold",
			bg = 'sky blue', relief = RIDGE, borderwidth = 2)
		lb_f_vru.place(x=450, y=71)
		self.lb_f_vru = Label(frame_gep, width = 5, font = "Arial 8 bold",
			bg = 'spring green', relief = RIDGE, borderwidth = 2)
		self.lb_f_vru.place(x=495, y=71)

	def set_status(self, status):
		self.status = status
		self.lb_status_gep.config(text = self.status)

	def set_ua_gep(self, ua_gep):
		self.ua_gep = ua_gep
		self.lb_ua_gep.config(text = self.ua_gep)

	def set_ub_gep(self, ub_gep):
		self.ub_gep = ub_gep
		self.lb_ub_gep.config(text = self.ub_gep)

	def set_uc_gep(self, uc_gep):
		self.uc_gep = uc_gep
		self.lb_uc_gep.config(text = self.uc_gep)

	def set_f_gep(self, f_gep):
		self.f_gep = f_gep
		self.lb_f_gep.config(text = self.f_gep)




# создаем главное окно программы
root = tk.Tk()
root.iconbitmap('image/icon.ico')
root.title('АСУ ДЭС РГЦ ЕС ОрВД Иркутск')
root.geometry('1024x768')
root.resizable(0, 0)

# загружаем картинку GEP
image_gep = PhotoImage(file = 'image/gep.png')

# создаем фрейм главного окна
frame_root = Frame(root, width = 1014, height = 758, relief = GROOVE, borderwidth = 2)
frame_root.place(x = 5, y = 5)

gep_100 = Gep(name = 'GEP 100', x = 5, y = 5)
gep_100.creat()

gep_100.set_status('ОСТАНОВЛЕН')
gep_100.set_ua_gep(230.0)
gep_100.set_ub_gep(235.0)
gep_100.set_uc_gep(232.0)
gep_100.set_f_gep(49.9)

root.mainloop()
