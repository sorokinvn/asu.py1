
#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import com
import tkinter as tk
from tkinter import*
import threading
import datetime
import time

def window_about():
	wa = tk.Toplevel()
	wa.geometry('500x500')
	wa.resizable(0, 0)
	wa.grab_set()

	wa.mainloop()

def get_temp(id, add):
	tmp = str(serial_port.get_analog_4(id, add))
	return tmp

def potok (my_func):
	def wapper(*args, **kwargs):
		my_thread = threading.Thread(target = my_func, args = args,
			kwargs = kwargs)
		my_thread.start()
	return wapper

@potok
def gt():
	n = threading.get_ident()
	print("Старт " + str(n))
	try:
		while True:
			temp1_lb.config(text = get_temp(3, 13))
			temp2_lb.config(text = get_temp(3, 14))
			temp3_lb.config(text = get_temp(3, 13))
			temp4_lb.config(text = get_temp(3, 14))
			temp5_lb.config(text = get_temp(3, 13))
			temp6_lb.config(text = get_temp(3, 14))
	except:
		print("Финиш " + str(n))
		pass

@potok
def gtime():
	n = threading.get_ident()
	print("Старт " + str(n))
	try:
		while True:
			time_lb.config(text = datetime.datetime.now().strftime('%d-%m-%Y\n%H:%M:%S'))
			time.sleep(1)
	except:
		print("Финиш " + str(n))
		pass

serial_port = com.Comport('com4', 9600)
serial_port.up()

root = tk.Tk()
root.geometry('500x500')
root.resizable(0, 0)

time_lb = Label(root, width = 10, height = 2, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
time_lb.place(x = 50, y = 30)


temp1_lb = Label(root, width = 5, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
temp1_lb.place(x = 50, y = 80)

temp2_lb = Label(root, width = 5, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
temp2_lb.place(x = 50, y = 110)

temp3_lb = Label(root, width = 5, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
temp3_lb.place(x = 50, y = 140)

temp4_lb = Label(root, width = 5, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
temp4_lb.place(x = 50, y = 170)

temp5_lb = Label(root, width = 5, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
temp5_lb.place(x = 50, y = 200)

temp6_lb = Label(root, width = 5, font = "Arial 10 bold",
	bg = 'black', fg = 'spring green', relief = RIDGE, borderwidth = 2)
temp6_lb.place(x = 50, y = 230)

bt_about = Button(root, width = 10, text = 'OK', font = "Arial 8 bold",
		command = window_about)
bt_about.place(x = 300, y = 100)


gtime()
gt()

root.mainloop()

serial_port.down()
