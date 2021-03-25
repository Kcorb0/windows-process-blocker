import os
import time
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font


class AppBlocker:

	def __init__(self, root):

		root.title("Distraction Knight")
		root.resizable(False, False)
		root.minsize(500, 200)


		basic_font = Font(
			family='roboto',
			size=12,
			weight='normal',
			slant='roman',
			underline=0,
			overstrike=0)

		master_frame = Frame(root, padding='.3i')
		master_frame.grid(row=0, column=0)

		newprocess_lbl = Label(master_frame, text="Enter process to block:", font=basic_font, width=26)
		self.newprocess_inp = Entry(master_frame, width=30)
		add_btn = Button(master_frame, text='Add', command=self.add_process)

		remprocess_lbl = Label(master_frame, text="Remove process from blocked:", font=basic_font, width=26)
		self.remprocess_inp = Entry(master_frame, width=30)
		del_btn = Button(master_frame, text='Remove')

		show_btn = Button(master_frame, text='View List')
		run_btn = Button(master_frame, text='Run Blocker', command=self.run_blocker)


		newprocess_lbl.grid(row=0, column=0, pady=(0, 20))
		self.newprocess_inp.grid(row=0, column=1, pady=(0, 20))
		add_btn.grid(row=0, column=2, pady=(0, 20), padx=(20,0))
		remprocess_lbl.grid(row=1, column=0, pady=(0, 20))
		self.remprocess_inp.grid(row=1, column=1, pady=(0, 20))
		del_btn.grid(row=1, column=2, pady=(0, 20), padx=(20,0))

		show_btn.grid(row=2, column=0, columnspan=3)
		run_btn.grid(row=3, column=0, columnspan=3)


	def add_process(self):
		"""Append user entry to blocked_apps.txt file and clear entry field"""
		entry_txt = self.newprocess_inp.get()

		with open('blocked_apps.txt', 'w') as apps:
			apps.write(f"\n{entry_txt}")
		self.newprocess_inp.delete(0, 'end')


	def run_blocker(self):
		"""Kills all task processes specified within the blocked_apps.txt file"""

		with open('blocked_apps.txt', 'r') as apps:
			app_list = [i.replace('\n', "") for i in apps.readlines()]

		if app_list == []:
			print("You have not specified a process to block.")
		else:
			while True:
				for app in app_list:
					os.system(f"taskkill /IM {app} /F")
				time.sleep(5)



root = Tk()
AppBlocker(root)
root.mainloop()