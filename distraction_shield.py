import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk


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

        # TTK Style elements
        fstyle = ttk.Style()
        fstyle.configure('Frame.TFrame', background='#4E4449')
        lstyle = ttk.Style()
        lstyle.configure('Label.TLabel', foreground='white',
                         background='#4E4449')

        master_frame = ttk.Frame(root, padding='.2i', style='Frame.TFrame')
        master_frame.grid(row=0, column=0)
        btn_frame = ttk.Frame(master_frame, style='Frame.TFrame')
        btn_frame.grid(row=3, column=0, columnspan=3)

        newprocess_lbl = ttk.Label(
            master_frame, text="Enter process to block:", font=basic_font, width=26, style='Label.TLabel')
        self.newprocess_inp = ttk.Entry(master_frame, width=30)
        add_btn = ttk.Button(master_frame, text='Add',
                             command=self.add_process)
        remprocess_lbl = ttk.Label(
            master_frame, text="Remove process from blocked:", font=basic_font, width=26, style='Label.TLabel')
        self.remprocess_inp = ttk.Entry(master_frame, width=30)
        del_btn = ttk.Button(master_frame, text='Remove',
                             command=self.remove_process)
        empty_btn = ttk.Button(
            btn_frame, text='Empty List', command=self.clear_list)
        show_btn = ttk.Button(btn_frame, text='View List')
        run_btn = ttk.Button(btn_frame, text='Run Blocker', command=lambda: [
                             self.set_true(), self.run_blocker()])
        stop_btn = ttk.Button(
            btn_frame, text='Stop Blocker', command=self.stop_blocker)
        self.status_lbl = ttk.Label(
            master_frame, text="", width=70, font=alert_font, foreground='#15DB00', style='Label.TLabel')

        newprocess_lbl.grid(row=1, column=0, pady=(0, 20))
        self.newprocess_inp.grid(row=1, column=1, pady=(0, 20))
        add_btn.grid(row=1, column=2, pady=(0, 20), padx=(20, 0))
        remprocess_lbl.grid(row=2, column=0, pady=(0, 20))
        self.remprocess_inp.grid(row=2, column=1, pady=(0, 20))
        del_btn.grid(row=2, column=2, pady=(0, 20), padx=(20, 0))

        show_btn.grid(row=0, column=0, padx=(0, 10), pady=(0, 10))
        run_btn.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))
        empty_btn.grid(row=1, column=0, padx=(0, 10))
        stop_btn.grid(row=1, column=1, padx=(10, 0))

        self.status_lbl.grid(row=5, column=0, columnspan=3,
                             pady=(20, 0), sticky='W')

    def add_process(self):
        """Append user entry to blocked_apps.txt file and clear entry field"""
        entry_txt = self.newprocess_inp.get()

        if len(entry_txt) == 0:
            self.status_lbl['text'] = ""
            self.status_lbl['text'] = "Input an application or process you want to block and click add. eg: 'steam.exe'"
        else:
            with open('blocked_apps.txt', 'a') as file:
                file.write(f"{entry_txt}\n")
                self.status_lbl['text'] = ""
                self.status_lbl['text'] = f"Added {entry_txt} to block list."
            self.newprocess_inp.delete(0, 'end')

    def remove_process(self):
        """Removes a process or app from the block list"""
        remove_txt = self.remprocess_inp.get()

        if len(remove_txt) == 0:
            self.status_lbl['text'] = ""
            self.status_lbl['text'] = f"Please enter an application or process that is in the block list."
        else:
            with open('blocked_apps.txt', 'r') as file:
                apps = file.readlines()

            with open('blocked_apps.txt', 'w') as new_file:
                for app in apps:
                    if app.strip("\n") != remove_txt:
                        new_file.write(app)

            self.status_lbl['text'] = ""
            self.status_lbl['text'] = f"{remove_txt} removed from block list."
        self.remprocess_inp.delete(0, 'end')

    def clear_list(self):
        with open('blocked_apps.txt', 'w'):
            pass
        self.status_lbl['text'] = ""
        self.status_lbl['text'] = f"All items in block list have been deleted."

    def set_true(self):
        """Sets run to true so that run_blocker does not infinite loop"""
        self.run = True

    def run_blocker(self):
        """Kills all task processes specified within the blocked_apps.txt file"""
        with open('blocked_apps.txt', 'r') as apps:
            app_list = [i.replace('\n', "") for i in apps.readlines()]

        if app_list == []:
            self.status_lbl['text'] = ""
            self.status_lbl['text'] = "Please add an application or process to block."

        elif self.run:
            for app in app_list:
                os.system(f"taskkill /IM {app} /F")
            root.after(5000, self.run_blocker)

    def stop_blocker(self):
        """Stops the blocker from completing another loop"""
        if self.run == True:
            self.run = False
            self.status_lbl['text'] = ""
            self.status_lbl['text'] = "Process blocker deactivated."


root = tk.Tk()
AppBlocker(root)
root.mainloop()
