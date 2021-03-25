import os
import time
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font


class AppBlocker:

	def __init__(self, root):

		root.title("Distraction Shield")
		root.iconbitmap('assets/logo.ico')
		root.resizable(False, False)
		root.minsize(500, 200)
		self.run = True

		basic_font = Font(
			family='roboto',
			size=12,
			weight='normal',
			slant='roman',
			underline=0,
			overstrike=0)

		alert_font = Font(
			family='roboto',
			size=10,
			weight='normal',
			slant='roman',
			underline=0,
			overstrike=0)

		master_frame = Frame(root, padding='.2i')
		master_frame.grid(row=0, column=0)

		newprocess_lbl = Label(master_frame, text="Enter process to block:", font=basic_font, width=26)
		self.newprocess_inp = Entry(master_frame, width=30)
		add_btn = Button(master_frame, text='Add', command=self.add_process)

		remprocess_lbl = Label(master_frame, text="Remove process from blocked:", font=basic_font, width=26)
		self.remprocess_inp = Entry(master_frame, width=30)
		del_btn = Button(master_frame, text='Remove', command=self.remove_process)

		show_btn = Button(master_frame, text='View List')
		run_btn = Button(master_frame, text='Run Blocker', command=self.run_blocker)

		self.status_lbl = Label(master_frame, text="", width=70, font=alert_font, foreground='green')


		newprocess_lbl.grid(row=1, column=0, pady=(0, 20))
		self.newprocess_inp.grid(row=1, column=1, pady=(0, 20))
		add_btn.grid(row=1, column=2, pady=(0, 20), padx=(20,0))
		remprocess_lbl.grid(row=2, column=0, pady=(0, 20))
		self.remprocess_inp.grid(row=2, column=1, pady=(0, 20))
		del_btn.grid(row=2, column=2, pady=(0, 20), padx=(20,0))

		show_btn.grid(row=3, column=0, columnspan=3)
		run_btn.grid(row=4, column=0, columnspan=3)

		self.status_lbl.grid(row=5, column=0, columnspan=3, pady=(20,0), sticky='W')


	def add_process(self):
		"""Append user entry to blocked_apps.txt file and clear entry field"""
		entry_txt = self.newprocess_inp.get()

		if len(entry_txt) == 0:
			self.status_lbl['text'] = ""
			self.status_lbl['text'] = "Input an application or process you want to block and click add. eg: 'steam.exe'"
		else:
			with open('blocked_apps.txt', 'w') as file:
				file.write(f"{entry_txt}\n")
				self.status_lbl['text'] = ""
				self.status_lbl['text'] = f"Added {entry_txt} to block list."
			self.newprocess_inp.delete(0, 'end')


	def remove_process(self):
		remove_txt = self.remprocess_inp.get()

		with open('blocked_apps.txt', 'r') as file:
			prev_apps = file.readlines()
			apps = file.readlines()

		with open('blocked_apps.txt', 'w') as file:
			for app in apps:
				if app.strip("\n") != remove_txt:
					file.write(f"{app}\n")

		if prev_apps == apps:
			self.status_lbl['text'] = ""
			self.status_lbl['text'] = f"Could not locate {remove_txt} in block list, please check the list and try again."

		self.remprocess_inp.delete(0, 'end')



	def run_blocker(self):
		"""Kills all task processes specified within the blocked_apps.txt file"""

		with open('blocked_apps.txt', 'r') as apps:
			app_list = [i.replace('\n', "") for i in apps.readlines()]

		if app_list == []:
			self.status_lbl['text'] = ""
			self.status_lbl['text'] = "Please add an application or process to block."
		else:
			while self.run:
				for app in app_list:
					os.system(f"taskkill /IM {app} /F")
				time.sleep(5)





root = Tk()
AppBlocker(root)
root.mainloop()